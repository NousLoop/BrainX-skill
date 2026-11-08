"""Independent serialization/graph/observation audit (no new simulation)."""
import hashlib
import json
from pathlib import Path
import numpy as np


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):h.update(part)
    return h.hexdigest()


def main():
    root=Path('runs/baseline-v1')
    previous=Path('checks/evidence_audit.json')
    audit=json.loads(previous.read_text()) if previous.exists() else dict(graphs={},runs={})
    for path in sorted((root/'graphs').glob('*.npz')):
        digest=sha(path)
        if audit['graphs'].get(path.stem,{}).get('sha256')==digest:continue
        z=np.load(path);checks=[]
        for prefix,ns,degree,offset in [('e',10000,1000,0),('i',2500,250,10000)]:
            indices,indptr=z[prefix+'_indices'],z[prefix+'_indptr']
            sources=np.repeat(np.arange(ns,dtype=np.int32),np.diff(indptr))
            assert len(indices)==12500*degree and indptr[-1]==len(indices)
            assert np.all(np.bincount(indices,minlength=12500)==degree)
            assert not np.any(indices==sources+offset)
            assert np.all((np.diff(indices)>0)|(np.diff(sources)>0))
            checks.append(dict(source=prefix,degree=degree,edges=len(indices),
                exact_indegree=True,no_autapses=True,no_duplicates=True))
        assert z['initial_mV'].shape==(12500,)
        assert np.all((z['initial_mV']>=10)&(z['initial_mV']<20))
        audit['graphs'][path.stem]=dict(sha256=digest,checks=checks)
    lookup=np.array([int(i).bit_count() for i in range(256)],np.uint8)
    for path in sorted((root/'raw').glob('*.npz')):
        digest=sha(path)
        if audit['runs'].get(path.stem,{}).get('sha256')==digest:continue
        z=np.load(path);p=z['packed'];counts=z['counts'];dt=float(z['dt_ms'])
        assert p.shape==(int(round(4000/dt)),1563) and counts.shape==(len(p),2)
        assert np.all((p[:,-1]&240)==0)
        assert np.array_equal(lookup[p[:,:1250]].sum(axis=1),counts[:,0])
        assert np.array_equal(lookup[p[:,1250:]].sum(axis=1),counts[:,1])
        assert np.isfinite(z['final_mV']).all() and np.all(z['final_mV']<20)
        graph_path=root/'graphs'/f"seed{int(z['seed'])}.npz"
        assert str(z['graph_sha256'])==audit['graphs'][graph_path.stem]['sha256']
        s=json.loads((root/'metrics'/(path.stem+'.json')).read_text())
        burn=int(round(1000/dt));rates=counts[burn:].sum(axis=0)/[10000,2500]/3
        assert np.allclose(rates,[s['E_rate_Hz'],s['I_rate_Hz']],rtol=0,atol=1e-12)
        assert s['max_neuron_rate_Hz']<=500+1/3
        assert s['min_postburn_ISI_ms']>=2-1e-7
        audit['runs'][path.stem]=dict(sha256=digest,per_bin_E_I_counts_exact=True,
            rate_normalization_exact=True,finite_final_voltage=True,refractory_bound_pass=True,
            graph_hash_exact=True,spikes=int(counts.sum()),dt_ms=dt)
        print('Audited',path.stem,flush=True)
    env=json.loads((root/'environment.json').read_text())
    for name,digest in env['code_sha256'].items():assert sha(root/'code'/name)==digest
    assert sha(root/'config.json')==env['config_sha256']
    key_checks={}
    for seed in [101,202,303]:
        files=[root/'raw'/f'condition{c}_seed{seed}_dt0.1.npz' for c in range(4)]
        if all(p.exists() for p in files):
            keys=[np.load(p)['final_rng_key'] for p in files]
            assert all(np.array_equal(keys[0],key) for key in keys[1:])
            key_checks[str(seed)]=dict(matched_key_consumption_across_conditions=True)
    audit['matched_rng_policy']=key_checks
    audit['immutable_snapshot_verified']=True
    audit['completed_raw_files']=len(audit['runs'])
    audit['full_experiment_complete']=len(audit['runs'])==16
    previous.write_text(json.dumps(audit,indent=2))
    rows=['# Raw evidence index','',
        'All native-grid binary spikes and per-bin E/I counts are preserved, with initial states, exact graphs, final voltage/last-spike step, RNG keys and configuration. Endpoint i has time (i+1)*dt_ms; packed neuron bits use little-endian order. No unfavorable run is omitted.','',
        '| Raw spikes/counts/final State | Scalar metrics | Individual CV and spectra |',
        '|---|---|---|']
    for path in sorted((root/'raw').glob('*.npz')):
        metric=root/'metrics'/path.name
        rows.append(f'| [{path.stem}]({path}) | [JSON]({metric.with_suffix(".json")}) | [NPZ]({metric}) |')
    rows+=['','Graphs and initial states: '+', '.join(f'[{p.stem}]({p})' for p in sorted((root/'graphs').glob('*.npz')))+'.',
        '', 'Independent serialized-evidence/graph audit: [checks/evidence_audit.json](checks/evidence_audit.json). Code/config/environment identities: [environment.json](runs/baseline-v1/environment.json). Raw run hashes: [manifest.json](runs/baseline-v1/manifest.json).',
        '',f'Currently audited raw files: {len(audit["runs"])}/16. Independent review remains a separate gate.']
    Path('RAW_EVIDENCE.md').write_text('\n'.join(rows)+'\n')


if __name__=='__main__':main()
