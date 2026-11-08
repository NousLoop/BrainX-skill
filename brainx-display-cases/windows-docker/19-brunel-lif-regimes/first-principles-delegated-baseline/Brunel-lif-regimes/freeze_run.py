"""Create an immutable scientific execution snapshot before launching."""
import hashlib
import importlib.metadata
import json
import platform
import shutil
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
run = root / 'runs' / 'locked-baseline-v2'
run.mkdir(parents=True, exist_ok=False)
config = dict(seeds=[11,29,47],dt_by_seed={'11':[.1,.05],'29':[.1],'47':[.1]},
              duration_ms=4000,burn_in_ms=1000,
              conditions=[[3,2],[6,4],[5,2],[4.5,.9]],
              expected=['synchronous regular','fast synchronous irregular',
                        'asynchronous irregular','slow synchronous irregular'],
              NE=10000,NI=2500,CE=1000,CI=250,Cext=1000,
              tau_m_ms=20,t_ref_ms=2,threshold_mV=20,reset_mV=10,
              JE_mV=.1,delay_ms=1.5,backend='cpu',precision='float32',
              figure_seed=11,figure_window_ms=[1000,1500],sample_seed=20261108)
(run/'config.json').write_text(json.dumps(config,indent=2))
sources=['model.py','experiment.py','analysis_spectrum.py','checks.py','smoke.py','NeuroSpecification.md']
(run/'code').mkdir()
for source in sources:
    shutil.copy2(root/source,run/'code'/source)
hashes={source:hashlib.sha256((root/source).read_bytes()).hexdigest() for source in sources}
versions={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}
env=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),
         packages=versions,source_sha256=hashes,
         environment={'JAX_PLATFORMS':'cpu','OMP_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'1'},
         cpu='AMD Ryzen 9 8945HX, 16 cores / 32 threads; existing Windows WSL2 Docker environment')
(run/'environment.json').write_text(json.dumps(env,indent=2))
command=f'JAX_PLATFORMS=cpu OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 {sys.executable} -u {run}/code/experiment.py --config {run}/config.json'
(run/'command.txt').write_text(command+'\n')
(run/'code.diff').write_text('Fresh project. Complete source snapshot in code/; no preexisting Git history.\n')
(run/'RUN_SPEC.md').write_text('''# Immutable full-size production and replication run

Run ID: locked-baseline-v2. Corrected implementation, forward-simulation, CPU, float32. Parent run: locked-baseline (one completed condition followed by a deterministic sparse-workspace tracer failure; preserved). Eager initialization of the public sparse operator before tracing corrects the execution error; scientific protocol unchanged. No input data beyond the user prompt. Existing BrainX environment; no installations. Code and specification identities are in environment.json. config.json is immutable and the entry point consumes it; supplied model constants are asserted in the source.

The exact command is command.txt. Seeds 11,29,47 have separate graphs/initialization/drive streams and are paired across conditions. Seed 11 additionally uses dt=0.05 ms. Twelve primary and four sensitivity runs are required. Each rollout is one compiled BrainState for_loop, with complete neural/delay State reset and explicit RNG reseeding after compilation and before every condition. No mid-rollout continuation is used.

Expected: exact saved graphs, graph checks, lossless bit-packed spikes for burn-in and observation, final voltage/refractory/RNG diagnostics, E/I counts, per-neuron counts and ISI CV/eligibility, Welch spectra, JSON/CSV metrics, frozen assessments, status and log, later PNG figures and manifest. Padded packbits bits outside the 12500 neurons are excluded from decoding.

Resources: based on smoke/result.json, estimated linear scale from the warm full-size 100 ms smoke. Primary rollouts contain 40000 steps; fine rollouts 80000. Estimated working memory under 4 GB and saved evidence under 3 GB. Stop only on nonfinite values, count/refractory inconsistency, out-of-memory/disk failure or process failure; no stopping for unfavorable scientific outcomes. No unchanged retries for deterministic failures. Preserve all failures in distinct paths. No paid compute. Expected scientific non-claims are in the locked specification.
''')
print(command)
