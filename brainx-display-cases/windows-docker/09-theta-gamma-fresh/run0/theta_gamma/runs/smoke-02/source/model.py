"""Locked illustrative WC dynamics, using BrainMass lifecycle and integration."""
import brainmass
import brainstate
import brainunit as u
import braintools
import numpy as np


class IllustrativeWC(brainmass.WilsonCowanStep):
    """Unshifted logistic WC; public derivative extension, no refractory term."""

    def __init__(self, gains, initial_e, initial_i, method="euler", tau_e_ms=1.25, tau_i_ms=2.5):
        self.loop_gain = u.math.asarray(gains)
        self.population_tau_E = tau_e_ms * u.ms
        self.population_tau_I = tau_i_ms * u.ms
        super().__init__(
            in_size=len(gains), tau_E=self.population_tau_E, tau_I=self.population_tau_I,
            a_E=1.3, theta_E=4.0, a_I=2.0, theta_I=3.7,
            wEE=16.0, wEI=12.0 * self.loop_gain,
            wIE=15.0 * self.loop_gain, wII=3.0, r=0.0,
            rE_init=braintools.init.Constant(u.math.asarray(initial_e)[:, None]),
            rI_init=braintools.init.Constant(u.math.asarray(initial_i)[:, None]),
            method=method,
        )
        self.applied_P = brainstate.ShortTermState(
            u.math.zeros((len(initial_e), len(gains))))

    def update(self, rE_inp=0.0, rI_inp=0.0):
        self.applied_P.value = u.math.ones_like(self.applied_P.value) * rE_inp
        return super().update(rE_inp, rI_inp)

    def drE(self, rE, rI, ext):
        activation = brainstate.nn.sigmoid(1.3 * (16*rE - 12*self.loop_gain*rI + ext - 4))
        return (-rE + activation) / self.population_tau_E

    def drI(self, rI, rE, ext):
        activation = brainstate.nn.sigmoid(2.0 * (15*self.loop_gain*rE - 3*rI + ext - 3.7))
        return (-rI + activation) / self.population_tau_I


def run_model(config, *, jit=True):
    """time × IC × condition; CPU and precision set before model construction."""
    brainstate.environ.set_platform("cpu")
    brainstate.environ.set(precision=64, fit=False)
    depths = u.math.asarray(config["depths_flat"])
    model = IllustrativeWC(config["gains_flat"], config["initial_e"], config["initial_i"],
                           config["method"], config["tau_e_ms"], config["tau_i_ms"])
    drive = lambda t: config["mean_drive"] + depths * u.math.cos(
        2 * u.math.pi * config["theta_hz"] * u.Hz * t)
    result = brainmass.Simulator(model, dt=config["dt_ms"] * u.ms).run(
        config["duration_s"] * u.second,
        inputs=lambda _i, t: (drive(t), 0.0),
        monitors={"E": "rE", "I": "rI", "P": "applied_P"},
        transient=config["transient_s"] * u.second,
        sample_every=config["sample_every"], batch_size=len(config["initial_e"]), jit=jit,
    )
    # Explicit host serialization boundary. ts contains post-update sample times.
    t_s = np.asarray(result["ts"].to_decimal(u.second))
    return {
        "t_s": t_s, "input_t_s": t_s - config["dt_ms"] / 1000,
        "E": np.asarray(result["E"]), "I": np.asarray(result["I"]),
        "P": np.asarray(result["P"]),
        "final_E": np.asarray(model.rE.value), "final_I": np.asarray(model.rI.value),
        "depths_flat": np.asarray(config["depths_flat"]),
        "gains_flat": np.asarray(config["gains_flat"]),
    }
