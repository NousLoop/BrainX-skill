"""Iteration-2 analysis-only execution; preserve the original immutable run."""
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path
import numpy as np
import analysis


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):h.update(part)
    return h.hexdigest()


def main():
    parent=Path('runs/baseline-v1').resolve();root=Path('runs/iteration-2').resolve()
    root.mkdir(exist_ok=False);(root/'metrics').mkdir();(root/'code').mkdir()
    for name in ['raw','graphs']:(root/name).symlink_to(parent/name,target_is_directory=True)
    for name in ['config.json','sample_neuron_ids.npy']:
        shutil.copy2(parent/name,root/name)
    files=['model.py','analysis.py','reanalyze.py','experiment.py','check_metric_fixture.py',
           'checks.py','check_temporal_input.py','NeuroSpecification.md',
           'brainx-study-record.md','brainx-study-record-iteration-2.md']
    for name in files:shutil.copy2(name,root/'code'/name)
    env=json.loads((parent/'environment.json').read_text())
    env['parent_run']=str(parent)
    env['parent_manifest_sha256']=sha(parent/'manifest.json')
    env['scope']='analysis-only; original float32 dynamical simulation unchanged; physical spectra float64'
    env['code_sha256']={name:sha(root/'code'/name) for name in files}
    env['config_sha256']=sha(root/'config.json')
    (root/'environment.json').write_text(json.dumps(env,indent=2))
    (root/'command.txt').write_text(f'{sys.executable} reanalyze.py\n')
    (root/'RUN_SPEC.md').write_text('# Immutable iteration-2 analysis contract\n\n'+
        'No new simulation. Parent baseline-v1 raw spikes/graphs are referenced via symlinks, with parent manifest and every raw hash verified. Original production and its manifest remain intact. Scientific configuration/specification/seeds/time windows/decision thresholds are unchanged.\n\n'+
        'Use documented BrainTools spectrogram, dt=0.1 ms, Hann/10000 samples/5000 overlap/constant segment detrend; average the segment axis. Full-window boxcar/zero-overlap/constant detrend gives the periodogram. Quantities preserve Hz input and Hz²/Hz PSD; scoped float64 analysis matches the original float64 host analysis, independently of the float32 dynamics.\n\n'+
        'Compare all frequencies and PSDs against original saved arrays (rtol=1e-9, atol=1e-11), all scalar metrics (rtol=1e-9, atol=1e-10), every categorical predicate and every final condition decision. Preserve differences and reject changed decisions. Save new metrics, assessment, parity, timing, code/environment/config identity, logs and hashes. No model optimization or new scientific execution is justified by this analysis-only correction.\n')
    parent_manifest=json.loads((parent/'manifest.json').read_text())
    comparisons=[];started=time.perf_counter()
    log=(root/'run.log').open('a',buffering=1)
    try:
        for path in sorted((root/'raw').glob('*.npz')):
            t0=time.perf_counter()
            raw_hash=sha(path)
            assert raw_hash==parent_manifest['raw/'+path.name]['sha256']
            original=np.load(parent/'metrics'/path.name)
            new=analysis.summarize(path,root/'metrics')
            corrected=np.load(root/'metrics'/path.name)
            checks={}
            for key in ['welch_frequency_Hz','welch_PSD_Hz2_per_Hz','periodogram_frequency_Hz','periodogram_PSD_Hz2_per_Hz']:
                a,b=original[key],corrected[key]
                assert a.shape==b.shape and np.allclose(a,b,rtol=1e-9,atol=1e-11),key
                checks[key]=dict(shape=list(a.shape),max_absolute_error=float(np.max(np.abs(a-b))),
                    relative_L2_error=float(np.linalg.norm(a-b)/max(np.linalg.norm(a),1e-300)))
            old=json.loads((parent/'metrics'/(path.stem+'.json')).read_text())
            for key,value in old.items():
                if key=='raw_file':continue
                if isinstance(value,(int,float)) and not isinstance(value,bool):
                    assert np.isclose(value,new[key],rtol=1e-9,atol=1e-10),key
                elif isinstance(value,list) and value and isinstance(value[0],(float,list)):
                    assert np.allclose(value,new[key],rtol=1e-9,atol=1e-10),key
                else:assert value==new[key],key
            record=dict(run=path.stem,raw_sha256=raw_hash,spectra=checks,
                all_metrics_and_predicates_preserved=True,seconds=time.perf_counter()-t0)
            comparisons.append(record);log.write(json.dumps(record)+'\n');print(path.stem,'PARITY PASS',flush=True)
        new_assessment=analysis.assess(root)
        original_assessment=json.loads((parent/'assessment.json').read_text())
        for old,new in zip(original_assessment,new_assessment):
            for key in ['decision','numerical_sensitivity','changed_categories','baseline_seed_outcomes','frequency_flag']:
                assert old[key]==new[key],key
        parity=dict(pass_=True,compared_runs=len(comparisons),all_raw_hashes_match_parent=True,
            unchanged_decisions=[r['decision'] for r in new_assessment],
            unchanged_model_sha256=sha('model.py'),original_model_sha256=sha(parent/'code/model.py'),
            analysis_precision='float64; Hz signal, Hz²/Hz PSD, dt=0.1 ms',
            elapsed_seconds=time.perf_counter()-started,comparisons=comparisons)
        assert parity['unchanged_model_sha256']==parity['original_model_sha256']
        (root/'spectral_parity.json').write_text(json.dumps(parity,indent=2))
        (root/'status.json').write_text(json.dumps(dict(status='done',exit_code=0,scope='analysis-only',elapsed_seconds=parity['elapsed_seconds']),indent=2))
        (root/'exit_code').write_text('0\n')
    except BaseException:
        import traceback
        log.write(traceback.format_exc());(root/'exit_code').write_text('1\n')
        (root/'status.json').write_text(json.dumps(dict(status='failed',exit_code=1)))
        raise
    finally:log.close()
    paths=set(p for p in root.rglob('*') if p.is_file())
    paths.update((root/'raw').glob('*.npz'));paths.update((root/'graphs').glob('*'))
    (root/'manifest.json').write_text(json.dumps({str(p.relative_to(root)):dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(paths)},indent=2))


if __name__=='__main__':main()
