"""Component and compiled-path checks, independent of regime outcomes."""
import json
import time
from pathlib import Path
import numpy as np
import jax
import jax.numpy as jnp
import brainstate
import brainunit as u
import model


def run_checks(destination):
    results = {}
    with brainstate.environ.context(dt=0.1 * u.ms):
        nu = model.THETA / (model.JE * model.CE * model.TAU)
        assert np.isclose(float(nu.to_decimal(u.Hz)), 10)
        results['threshold_source_Hz'] = float(nu.to_decimal(u.Hz))
        cell = model.DeltaLIF(jnp.array([15.0]) * u.mV, 0.1 * u.ms)
        brainstate.nn.init_all_states(cell)
        def quiet_step(i):
            s = cell(i, jnp.zeros(1) * u.mV)
            return cell.V.value.to_decimal(u.mV), s
        voltage, spikes = brainstate.transform.for_loop(quiet_step, jnp.arange(100))
        assert np.allclose(np.asarray(voltage[:, 0]),
                           15 * np.exp(-np.arange(1, 101) * .1 / 20), rtol=2e-5)
        assert not np.any(spikes)
        results['analytic_exponential_leak'] = True
        brainstate.nn.init_all_states(cell)
        def jump_step(i):
            spike = cell(i, jnp.array([100.0]) * u.mV)
            return spike, cell.V.value.to_decimal(u.mV)
        spikes, voltage = brainstate.transform.for_loop(jump_step, jnp.arange(65))
        fired = np.flatnonzero(np.asarray(spikes[:, 0]))
        assert np.array_equal(fired, [0, 20, 40, 60])
        assert np.allclose(voltage, 10)
        results['refractory_spike_steps'] = fired.tolist()

        brainstate.nn.init_all_states(cell)
        spikes = brainstate.transform.for_loop(
            lambda i: cell(i, jnp.array([.2]) * u.mV), jnp.arange(5000))
        periods = np.diff(np.flatnonzero(np.asarray(spikes[:, 0]))) * .1
        analytic_period = 2 + 20 * np.log((40 - 10) / (40 - 20))
        assert abs(np.median(periods) - analytic_period) <= .2
        results['mean_external_drive_period'] = dict(
            measured_ms=float(np.median(periods)),analytic_ms=float(analytic_period),
            tolerance_ms=.2)

        # Production delay/communication path, using exact one-edge E and I graphs.
        graphs = [(np.array([1], np.int32), np.array([0, 1], np.int32)),
                  (np.array([0], np.int32), np.array([0, 1], np.int32))]
        net = model.Network(graphs, jnp.zeros(2) * u.mV, 7, .1 * u.ms, ne=1, ni=1)
        brainstate.nn.init_all_states(net)
        def impulse(i):
            previous = jnp.array([i == 1, i == 31])
            net.delay.update(previous)
            delayed = net.delay.retrieve_at_step(jnp.asarray(net.delay_steps - 1))
            net.comm.gain.value = jnp.array(5.0)
            net.proj(delayed)
            return net.pop.sum_delta_inputs(jnp.zeros(2) * u.mV).to_decimal(u.mV)
        arrivals = np.asarray(brainstate.transform.for_loop(impulse, jnp.arange(60)))
        assert np.array_equal(np.flatnonzero(arrivals[:, 1]), [15])
        assert np.array_equal(np.flatnonzero(arrivals[:, 0]), [45])
        assert np.isclose(arrivals[15, 1], .1)
        assert np.isclose(arrivals[45, 0], -.5)
        results['delay'] = dict(emission_steps=[0,30], arrival_steps=[15,45],
                                jump_mV=[float(arrivals[15,1]),float(arrivals[45,0])])

        # True Poisson counts: allow repeated arrivals and check covariance.
        drive = model.PoissonDrive(256, 101, .1 * u.ms)
        samples = brainstate.transform.for_loop(
            lambda _: drive(jnp.array(4.0)).to_decimal(u.mV) / .1, jnp.arange(2000))
        samples = np.asarray(samples)
        mean, var = samples.mean(), samples.var()
        corr = np.corrcoef(samples.T)
        off = corr[np.triu_indices(256, 1)]
        assert abs(mean - 4) < .025 and abs(var - 4) < .06
        assert abs(off.mean()) < .005 and samples.max() > 1
        results['poisson'] = dict(mean=float(mean),variance=float(var),
                                 mean_pair_correlation=float(off.mean()),max_count=int(samples.max()))

        graphs, graph_checks = model.make_graph(17, ne=16, ni=8, ce=5, ci=3)
        results['tiny_graph'] = graph_checks
        init = model.initial_state(17, 24)
        baseline = model.Network(graphs, init, 17, .1 * u.ms, ne=16, ni=8)
        compiled = model.Network(graphs, init, 17, .1 * u.ms, ne=16, ni=8)
        brainstate.nn.init_all_states(baseline)
        brainstate.nn.init_all_states(compiled)
        reset_snapshot = model.snapshot_states(compiled)
        indices = jnp.arange(1000)
        t0 = time.perf_counter()
        a = baseline.rollout(indices, jnp.array(5.0), jnp.array(2.0))
        np.asarray(a)
        baseline_seconds = time.perf_counter() - t0
        run = brainstate.transform.jit(compiled.rollout, static_argnums=(1, 2))
        t0 = time.perf_counter()
        run.compile(indices, 5.0, 2.0)
        compile_seconds = time.perf_counter() - t0
        t0 = time.perf_counter()
        b = run(indices, 5.0, 2.0)
        np.asarray(b)
        warm_seconds = time.perf_counter() - t0
        assert np.array_equal(a, b)
        assert np.allclose(baseline.pop.V.value.to_decimal(u.mV),
                           compiled.pop.V.value.to_decimal(u.mV), atol=1e-6)
        assert np.array_equal(baseline.pop.last.value, compiled.pop.last.value)
        baseline_key = np.asarray(jax.random.key_data(baseline.drive.rng.value)).tolist()
        compiled_key = np.asarray(jax.random.key_data(compiled.drive.rng.value)).tolist()
        assert baseline_key == compiled_key
        model.restore_states(reset_snapshot)
        replay = run(indices, 5.0, 2.0)
        replay = np.asarray(replay)
        print('REPLAY diagnostic', int(np.count_nonzero(np.asarray(b) != replay)),
              np.asarray(jax.random.key_data(compiled.drive.rng.value)).tolist(),
              'previous key', compiled_key, flush=True)
        assert np.array_equal(b, replay)
        results['compilation_parity'] = dict(exact_spikes=True,final_voltage=True,
                                             refractory=True,seeded_replay=True,
                                             baseline_boundary_rng_key=baseline_key,
                                             compiled_boundary_rng_key=compiled_key,
                                             rng_boundary_keys_equal=baseline_key==compiled_key,
                                             baseline_seconds=baseline_seconds,
                                             compile_seconds=compile_seconds,warm_seconds=warm_seconds)
    Path(destination).write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2), flush=True)


if __name__ == '__main__':
    brainstate.environ.set_platform('cpu')
    run_checks('checks.json')
