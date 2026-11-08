import json,os,shutil,subprocess,sys,time
from pathlib import Path
source=Path('/evidence');work=Path('/tmp/brunel-audit');out=Path('/audit')
shutil.copytree(source,work)
env=os.environ.copy();env.update(MPLCONFIGDIR='/tmp/mpl',MPLBACKEND='Agg',JAX_PLATFORMS='cpu',OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1')
commands=[('components',['checks.py']),('analysis',['analysis_checks.py']),('raw-audit',['audit_results.py','--run','runs/locked-baseline-v2']),('spectra',['recompute_spectra.py'])]
results=[]
for name,args in commands:
 start=time.monotonic()
 with (out/(name+'.log')).open('w') as log:
  r=subprocess.run([sys.executable,*args],cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT)
 results.append(dict(check=name,exit_code=r.returncode,elapsed_seconds=time.monotonic()-start))
 (out/'replay.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,r.returncode,flush=True)
 if r.returncode:sys.exit(r.returncode)
for name in ['checks.json','analysis_checks.json','runs/locked-baseline-v2/raw_audit.json','analysis-iteration-2/braintools-final/parity.json']:
 shutil.copy2(work/name,out/Path(name).name)
