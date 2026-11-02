import time
from pathlib import Path
import brainunit as u
import jax
import numpy as np
import alpha_rhythm as experiment

kwargs = dict(dt=0.05*u.ms, duration=20*u.ms)
start=time.perf_counter(); baseline=experiment.run_grid(**kwargs, jit=False)
jax.block_until_ready(baseline["eeg"]); baseline_s=time.perf_counter()-start
start=time.perf_counter(); accelerated=experiment.run_grid(**kwargs, jit=True)
jax.block_until_ready(accelerated["eeg"]); accelerated_s=time.perf_counter()-start
checks={}
for field in ["eeg", "excitatory_psp", "inhibitory_psp"]:
    delta=float(np.max(np.abs(np.asarray((accelerated[field]-baseline[field]).to_decimal(u.mV)))))
    assert delta <= 1e-6, (field,delta)
    checks[field]={"max_absolute_difference_mv":delta,"pass":True,"shape":list(accelerated[field].shape)}
experiment.write_json(Path("acceleration-evidence-iteration-3.json"),
    {"candidate_dt_ms":0.05,"duration_ms":20,"all_32_lanes":True,"checks":checks,
     "baseline_compile_and_execute_s":baseline_s,"accelerated_compile_and_execute_s":accelerated_s,
     "optimization":"unchanged whole-rollout BrainState jit; no new optimization claim"})
print("PASS: refined-step full-grid stateful JIT parity")
