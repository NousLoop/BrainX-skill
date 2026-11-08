import hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
source=Path('/evidence');work=Path('/workspace');out=Path('/audit')
manifest=json.loads((source/'.harness-archive/manifest.json').read_text())
work.mkdir(exist_ok=True)
for entry in manifest['entries']:
 dest=work/entry['path']
 assert dest.resolve().is_relative_to(work)
 if entry['type']=='directory':dest.mkdir(parents=True,exist_ok=True)
 elif entry['type']=='file':
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/entry['path'],dest)
  assert hashlib.sha256(dest.read_bytes()).hexdigest()==entry['sha256']
for entry in manifest['entries']:
 if entry['type']=='symlink':
  target=Path(entry['target'])
  assert target.is_absolute() and target.is_relative_to(work)
  (work/entry['path']).symlink_to(target,target_is_directory=True)
env=os.environ.copy();env.update(MPLCONFIGDIR='/tmp/mpl',MPLBACKEND='Agg',JAX_PLATFORMS='cpu')
# Replay only in a disposable canonical reconstruction. No model service call.
commands=[('components',['checks.py']),('temporal-input',['check_temporal_input.py']),('fixture',['check_metric_fixture.py']),('raw-audit',['audit_evidence.py']),('spectral-reanalysis',['reanalyze.py'])]
results=[]
for name,args in commands:
 if name=='raw-audit':(work/'checks/evidence_audit.json').unlink()
 if name=='spectral-reanalysis':(work/'runs/iteration-2').rename(work/'runs/reviewed-iteration-2')
 start=time.monotonic()
 with (out/(name+'.log')).open('w') as log:r=subprocess.run([sys.executable,*args],cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT)
 results.append(dict(check=name,exit_code=r.returncode,elapsed_seconds=time.monotonic()-start))
 (out/'replay.json').write_text(json.dumps(results,indent=2)+'\n');print(name,r.returncode,flush=True)
 if r.returncode:sys.exit(r.returncode)
import numpy as np
comparisons=[]
for old in sorted((work/'runs/reviewed-iteration-2/metrics').glob('*.npz')):
 new=work/'runs/iteration-2/metrics'/old.name
 with np.load(old) as a,np.load(new) as b:
  assert a.files==b.files
  for key in a.files:np.testing.assert_allclose(a[key],b[key],rtol=1e-12,atol=1e-12,equal_nan=True)
 comparisons.append(old.name)
a=json.loads((work/'runs/reviewed-iteration-2/assessment.json').read_text());b=json.loads((work/'runs/iteration-2/assessment.json').read_text())
assert [x['decision'] for x in a]==[x['decision'] for x in b]
(out/'native-parity.json').write_text(json.dumps(dict(compared_runs=len(comparisons),all_saved_arrays_match=True,decisions=[x['decision'] for x in b],canonical_links_restored=True,network='none'),indent=2)+'\n')
for name in ['checks/components.json','checks/evidence_audit.json','checks/temporal_poisson.json','checks/metrics_fixture_v2/test_result.json','runs/iteration-2/spectral_parity.json']:
 shutil.copy2(work/name,out/Path(name).name)
