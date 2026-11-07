"""Create immutable local run snapshot then execute its exact recorded command."""
import argparse
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def launch(run_id, config):
    run=ROOT/'runs'/run_id;run.mkdir(exist_ok=False)
    for d in ['raw','metrics','src']: (run/d).mkdir()
    for name in ['model.py','analysis.py','experiment.py','test_checks.py','plot_results.py','launch.py','NeuroSpecification.md','brainx-study-record.md']:
        shutil.copy2(ROOT/name,run/'src'/name)
    command=[sys.executable,str(run/'src/experiment.py'),'--config',str(run/'config.json')]
    env=os.environ.copy();env['JAX_PLATFORMS']='cpu'
    probe=subprocess.check_output([sys.executable,'-c',"import BrainX,jax; print(jax.default_backend());print(jax.devices())"],env=env,text=True)
    assert probe.startswith('cpu')
    environment=dict(python=sys.executable,python_version=sys.version,backend='cpu',device_probe=probe,precision=64,
         packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()},JAX_PLATFORMS='cpu')
    for name,value in [('config.json',config),('environment.json',environment)]:
        (run/name).write_text(json.dumps(value,indent=2))
    (run/'command.txt').write_text(' '.join(command)+'\n')
    (run/'code.diff').write_text('No git repository: exact source snapshots and SHA256 are authoritative.\n')
    identity={str(p.relative_to(run)):digest(p) for p in sorted((run/'src').iterdir())}
    identity.update({p:digest(run/p) for p in ['config.json','environment.json','command.txt','code.diff']})
    (run/'provenance.json').write_text(json.dumps(identity,indent=2))
    (run/'RUN_SPEC.md').write_text(f'''# Run {run_id}
- Entry: new; level: {config['stage']}; no checkpoint continuation.
- Working directory: {ROOT}
- Command: command.txt; interpreter: {sys.executable}; backend: CPU; precision: float64.
- Model: BrainMass WilsonCowanStep; RK4 dt=0.1 ms; refinement dt=0.05 ms.
- Data: synthetic only. Immutable source/config/environment hashes: provenance.json.
- Seeds and initial conditions: config.json; deterministic dynamics, paired observation noise.
- Expected artifacts: raw/*.npz, metrics/*; calibration selection.json, production summary.json.
- Resource estimate: <1 GB retained/intermediate arrays, <5 minutes per stage, local CPU only.
- Stop conditions: nonfinite output, invariant failure, timeout 300 s, insufficient review quota; preserve all failures.
- Retry budget: zero for deterministic failures; no scientific retuning after calibration.
''')
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (run/'status.json').write_text(json.dumps(dict(status='running',start=started)))
    with (run/'run.log').open('a') as log:
        try: code=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=300).returncode
        except subprocess.TimeoutExpired: code=124
    (run/'exit_code').write_text(str(code)+'\n')
    (run/'status.json').write_text(json.dumps(dict(status='done' if code==0 else 'failed',start=started,end=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=code)))
    files={str(p.relative_to(run)):dict(sha256=digest(p),bytes=p.stat().st_size) for p in sorted(run.rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
    (run/'artifact_manifest.json').write_text(json.dumps(files,indent=2))
    print(run_id,'exit',code,flush=True)
    if code: raise SystemExit(code)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run_id');p.add_argument('config');a=p.parse_args()
    launch(a.run_id,json.loads(Path(a.config).read_text()))
