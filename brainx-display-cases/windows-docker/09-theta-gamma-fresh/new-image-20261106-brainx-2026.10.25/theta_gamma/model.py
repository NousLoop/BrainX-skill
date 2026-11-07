"""BrainMass Wilson–Cowan circuit; raw arrays only at the host boundary."""
import os
os.environ.setdefault('JAX_PLATFORMS', 'cpu')
import time
import brainmass
import brainstate
import brainunit as u
import braintools
import jax
import numpy as np

jax.config.update('jax_enable_x64', True)
brainstate.environ.set(precision=64, platform='cpu', fit=False)


def build(gains, initial=((0.1, 0.1),)):
    gains = u.math.asarray(gains)
    initial = u.math.asarray(initial)
    return brainmass.WilsonCowanStep(
        in_size=gains.size, tau_E=4*u.ms, tau_I=8*u.ms,
        a_E=1.2, theta_E=2.8, a_I=1.0, theta_I=4.0, r=1.0,
        # Compatibility adapter: runtime derivative probes establish that this
        # environment uses wIE for I-to-E and wEI for E-to-I.
        wEE=16*gains, wIE=12*gains, wEI=15*gains, wII=3*gains,
        rE_init=braintools.init.Constant(initial[:, 0, None]),
        rI_init=braintools.init.Constant(initial[:, 1, None]), method='rk4')


def simulate(gains, depths, drive, *, dt_ms=0.1, duration_s=14,
             burn_s=2, initial=((0.1, 0.1),), jit=True):
    node = build(gains, initial)
    depths = u.math.asarray(depths)
    def inputs(_i, t):
        return (drive + depths*u.math.cos(2*u.math.pi*6*u.Hz*t), 0.0)
    started = time.perf_counter()
    result = brainmass.Simulator(node, dt=dt_ms*u.ms).run(
        duration_s*u.second, inputs=inputs, monitors=['rE', 'rI'],
        transient=burn_s*u.second, sample_every=round(1/dt_ms),
        batch_size=len(initial), jit=jit)
    jax.block_until_ready(result)
    elapsed = time.perf_counter()-started
    # Explicit host boundary: time to seconds, dimensionless population arrays.
    out = {key: np.asarray(u.get_magnitude(result[key])) for key in ['rE','rI']}
    out['t_s'] = np.asarray(result['ts'].to_decimal(u.second))
    out['final_E'] = np.asarray(u.get_magnitude(node.rE.value))
    out['final_I'] = np.asarray(u.get_magnitude(node.rI.value))
    out['input_E_left'] = drive + np.cos(2*np.pi*6*(out['t_s']-dt_ms/1000))[:,None]*np.asarray(depths)
    out['input_E_monitor'] = drive + np.cos(2*np.pi*6*out['t_s'])[:,None]*np.asarray(depths)
    out['elapsed_s'] = elapsed
    return out
