"""Immutable run snapshot, complete fixed-seed experiment, raw evidence."""
import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
import time
import traceback
from pathlib import Path
import importlib.metadata
# Worker processes bind disjoint CPU subsets before importing BrainX/JAX.
if '--cpu-lane' in sys.argv and hasattr(os,'sched_setaffinity'):
    lane=int(sys.argv[sys.argv.index('--cpu-lane')+1])
    available=sorted(os.sched_getaffinity(0))
    os.sched_setaffinity(0,available[lane*len(available)//3:(lane+1)*len(available)//3])
import numpy as np
import jax
import brainstate
import brainunit as u
import model
import analysis


def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def run_group(run_dir,seed,dt):
    root=Path(run_dir);config=json.loads((root/'config.json').read_text())
    z=np.load(root/'graphs'/f'seed{seed}.npz')
    graph=[(z['e_indices'],z['e_indptr']),(z['i_indices'],z['i_indptr'])]
    graph_path=root/'graphs'/f'seed{seed}.npz'
    log=(root/f'group_seed{seed}_dt{dt}.log').open('a',buffering=1)
    def message(record):
        line=json.dumps(dict(wall_time=time.time(),**record));log.write(line+'\n');print(line,flush=True)
    message(dict(event='worker_ready',seed=seed,dt_ms=dt,backend=jax.default_backend(),
        cpu_affinity=sorted(os.sched_getaffinity(0)) if hasattr(os,'sched_getaffinity') else None))
    with brainstate.environ.context(dt=dt*u.ms):
        steps=int(round(config['duration_ms']/dt))
        net=model.Network(graph,z['initial_mV'],dt)
        brainstate.nn.init_all_states(net)
        initial_state={path:state.value for path,state in net.states().items()}
        runner=model.make_runner(net,steps)
        for c,(g,eta) in enumerate(analysis.PAIRS):
            stem=f'condition{c}_seed{seed}_dt{dt}'
            message(dict(event='begin',run=stem))
            unexpected,missing=brainstate.nn.assign_state_values(net,initial_state)
            assert not unexpected and not missing
            brainstate.random.seed(seed)
            t0=time.perf_counter();output=runner(g,eta);jax.block_until_ready(output)
            seconds=time.perf_counter()-t0
            packed,counts=map(np.asarray,output)
            voltage=np.asarray(net.pop.V.value.to_decimal(u.mV))
            assert np.isfinite(voltage).all()
            raw_path=root/'raw'/(stem+'.npz')
            np.savez_compressed(raw_path,packed=packed,counts=counts,final_mV=voltage,
                final_last_spike_step=np.asarray(net.pop.last_step.value),
                final_rng_key=np.asarray(brainstate.random.get_key_data()),
                seed=seed,condition=c,g=g,eta=eta,dt_ms=dt,steps=steps,ne=model.NE,ni=model.NI,
                graph_sha256=digest(graph_path),simulation_seconds=seconds)
            stats=analysis.summarize(raw_path,root/'metrics')
            message(dict(event='saved',run=stem,simulation_seconds=seconds,
                E_Hz=stats['E_rate_Hz'],I_Hz=stats['I_rate_Hz'],CV=stats['CV_median'],
                S=stats['synchrony_S'],peak_Hz=stats['dominant_frequency_Hz'],
                outcome=stats['baseline_outcome']))
            del output,packed,counts
    log.close()


def launch_group(arguments):
    import subprocess
    root,seed,dt,lane=arguments
    cmd=[sys.executable,'experiment.py','--run-dir',str(root),'--group',str(seed),str(dt),'--cpu-lane',str(lane)]
    with (root/f'worker_seed{seed}_dt{dt}.log').open('a') as log:
        result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:raise RuntimeError(f'group {seed}, dt={dt} exited {result.returncode}')
    return dict(seed=seed,dt_ms=dt,exit_code=result.returncode)


def main(run_dir):
    root=Path(run_dir)
    root.mkdir(parents=True,exist_ok=False)
    for name in ['raw','metrics','graphs','code']:(root/name).mkdir()
    config=dict(seeds=[101,202,303],conditions=[list(x) for x in analysis.PAIRS],
        ne=model.NE,ni=model.NI,ce=model.CE,ci=model.CI,cext=model.CEXT,
        tau_ms=20.,refractory_ms=2.,threshold_mV=20.,reset_mV=10.,JE_mV=.1,delay_ms=1.5,
        dt_ms=.1,control_dt_ms=.05,control_seed=101,duration_ms=4000.,burn_ms=1000.,
        sample_seed=20261108,raster_sample_size=50,display_seed=101,display_ms=[3500.,4000.],
        backend='cpu',precision='float32',max_worker_processes=3,
        run_level='production+fixed-seed-replication+numerical-controls')
    (root/'config.json').write_text(json.dumps(config,indent=2))
    files=['model.py','analysis.py','experiment.py','checks.py','NeuroSpecification.md','brainx-study-record.md']
    for name in files:shutil.copy2(name,root/'code'/name)
    versions={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}
    env=dict(python=sys.executable,python_version=sys.version,os=platform.platform(),
        machine=platform.machine(),cpu_count=os.cpu_count(),backend=jax.default_backend(),
        devices=[str(x) for x in jax.devices()],packages=versions,
        environment={k:os.environ[k] for k in ['JAX_PLATFORMS','OMP_NUM_THREADS','NUMBA_NUM_THREADS','XLA_FLAGS'] if k in os.environ},
        code_sha256={name:digest(root/'code'/name) for name in files},
        config_sha256=digest(root/'config.json'),scientific_sources='task text only; no papers, scientific examples, existing model code or remembered protocols')
    assert env['backend']=='cpu'
    (root/'environment.json').write_text(json.dumps(env,indent=2))
    command=f'{sys.executable} experiment.py --run-dir {run_dir}'
    (root/'command.txt').write_text(command+'\n')
    (root/'RUN_SPEC.md').write_text('# Immutable run contract\n\n'+
        f'Command: `{command}`\n\nCPU, float32; 12 baseline and 4 dt controls. 4000 ms/run, 1000 ms burn-in. Seeds and every specified parameter are in config.json; scientific rules in code/NeuroSpecification.md. Code/config identity in environment.json. Expected: 16 native-grid packed spike NPZs, 16 metric JSON/NPZ pairs, 3 exact graphs, assessment, all logs, exit status and artifact SHA256 manifest. No raw experimental data. No checkpoint resume.\n\n'+
        'Stop only for nonfinite state, contract/assertion failure, corrupt output or an external execution failure. Never stop for unfavorable scientific evidence. No automatic retry; preserve any failed run directory. Resource estimate: 64 MB graph indices, about 63 MB baseline or 125 MB fine-grid packed spike monitor, plus compiled workspace; benchmark in ../../checks/acceleration.json.\n')
    sample=np.random.default_rng(config['sample_seed']).choice(model.N,50,replace=False)
    np.save(root/'sample_neuron_ids.npy',sample)
    started=time.time()
    log=(root/'run.log').open('a',buffering=1)
    def message(record):
        line=json.dumps(dict(wall_time=time.time(),**record))
        log.write(line+'\n');print(line,flush=True)
    try:
        for seed in config['seeds']:
            if seed==101 and Path('checks/graph_seed101.npz').exists():
                z=np.load('checks/graph_seed101.npz')
                graph=[(z['e_indices'],z['e_indptr']),(z['i_indices'],z['i_indptr'])]
                graph_checks=json.loads(Path('checks/acceleration.json').read_text())['graph_checks']
            else:graph,graph_checks=model.fixed_indegree_graph(seed)
            v0=model.initial_voltage(seed)
            graph_path=root/'graphs'/f'seed{seed}.npz'
            np.savez_compressed(graph_path,e_indices=graph[0][0],e_indptr=graph[0][1],
                i_indices=graph[1][0],i_indptr=graph[1][1],initial_mV=v0)
            (root/'graphs'/f'seed{seed}.json').write_text(json.dumps(graph_checks,indent=2))
        from concurrent.futures import ThreadPoolExecutor,as_completed
        groups=[(root,seed,.1,lane) for lane,seed in enumerate(config['seeds'])]
        (root/'status.json').write_text(json.dumps(dict(status='running',groups=[list(x[1:3]) for x in groups],started=started)))
        with ThreadPoolExecutor(max_workers=3) as pool:
            for completed in as_completed([pool.submit(launch_group,x) for x in groups]):message(dict(event='group_done',**completed.result()))
        # Fine-grid group follows the baseline pool, keeping memory bounded.
        message(dict(event='group_done',**launch_group((root,101,.05,0))))
        assessment=analysis.assess(root)
        (root/'status.json').write_text(json.dumps(dict(status='done',exit_code=0,
            elapsed_seconds=time.time()-started,decisions=[x['decision'] for x in assessment]),indent=2))
        (root/'exit_code').write_text('0\n')
        message(dict(event='complete',elapsed_seconds=time.time()-started))
    except BaseException:
        log.write(traceback.format_exc());log.flush()
        (root/'status.json').write_text(json.dumps(dict(status='failed-deterministic',exit_code=1)))
        (root/'exit_code').write_text('1\n')
        raise
    finally:log.close()
    manifest={str(p.relative_to(root)):dict(bytes=p.stat().st_size,sha256=digest(p))
              for p in sorted(root.rglob('*')) if p.is_file() and p.name!='manifest.json'}
    (root/'manifest.json').write_text(json.dumps(manifest,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-dir',default='runs/baseline-v1')
    parser.add_argument('--group',nargs=2)
    parser.add_argument('--cpu-lane',type=int)
    args=parser.parse_args()
    if args.group:run_group(args.run_dir,int(args.group[0]),float(args.group[1]))
    else:main(args.run_dir)
