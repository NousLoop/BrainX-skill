"""Target CPU smoke at the full supplied neuron and edge counts."""
import json
import time
from pathlib import Path
import jax
import jax.numpy as jnp
import numpy as np
import brainstate
import brainunit as u
import model

brainstate.environ.set_platform('cpu')
start = time.perf_counter()
graphs, graph_checks = model.make_graph(11)
with brainstate.environ.context(dt=.1 * u.ms):
    net = model.Network(graphs, model.initial_state(11), 11, .1 * u.ms)
    brainstate.nn.init_all_states(net)
    reset_snapshot = model.snapshot_states(net)
    run = brainstate.transform.jit(net.rollout, static_argnums=(1, 2))
    indices = jnp.arange(1000, dtype=jnp.int32)
    t0 = time.perf_counter()
    run.compile(indices, 3.0, 2.0)
    compile_s = time.perf_counter() - t0
    model.restore_states(reset_snapshot)
    t0 = time.perf_counter()
    spikes = np.asarray(run(indices, 3.0, 2.0))
    warm_s = time.perf_counter() - t0
    assert spikes.shape == (1000, (model.N + 7) // 8)
    assert np.all(np.isfinite(net.pop.V.value.to_decimal(u.mV)))
    np.savez_compressed('smoke/raw.npz', spikes_packed=spikes,
                        final_V_mV=np.asarray(net.pop.V.value.to_decimal(u.mV)))
    evidence = dict(backend=jax.default_backend(),devices=[str(d) for d in jax.devices()],
                    graph_checks=graph_checks,compile_seconds=compile_s,
                    warm_100ms_seconds=warm_s,total_seconds=time.perf_counter()-start,
                    shape=list(spikes.shape),finite=True)
    Path('smoke/result.json').write_text(json.dumps(evidence, indent=2))
    print(json.dumps(evidence, indent=2), flush=True)
