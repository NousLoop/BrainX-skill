"""Independent host-side checks of saved counts, sample ISIs, hashes and claims."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np


def audit(run):
    run=Path(run).resolve();root=run.parent.parent
    rows=json.loads((run/'metrics.json').read_text())
    sample=np.load(run/'sample_neurons.npy')
    table=np.array([i.bit_count() for i in range(256)],dtype=np.uint8)
    checks=[]
    for row in rows:
        name=f"seed-{row['seed']}_dt-{row['dt_ms']:g}_condition-{row['condition']}"
        with np.load(run/row['raw_file']) as raw,np.load(run/'metrics'/f'{name}.npz') as data:
            packed=raw['spikes_packed']
            assert np.all((packed[:,-1]>>4)==0)
            e=table[packed[:,:1250]].sum(axis=1)
            i=table[packed[:,1250:]].sum(axis=1)
            assert np.array_equal(e,data['counts_EI'][:,0])
            assert np.array_equal(i,data['counts_EI'][:,1])
            eligible=0
            for neuron in sample:
                bits=(packed[:,neuron//8]>>(neuron%8))&1
                isi=np.diff(np.flatnonzero(bits))*row['dt_ms']
                expected=isi.std()/isi.mean() if len(isi)>=10 else np.nan
                assert np.allclose(expected,data['ISI_CV'][neuron],equal_nan=True,atol=1e-10)
                assert len(isi)==data['ISI_count'][neuron]
                eligible+=len(isi)>=10
            checks.append(dict(name=name,count_match=True,sample_CV_match=True,
                               sample_neurons=50,sample_eligible=eligible,padding_zero=True))
    (run/'raw_audit.json').write_text(json.dumps(checks,indent=2))
    deltas=[]
    for ci in range(4):
        coarse=next(r for r in rows if r['seed']==11 and r['condition']==ci and r['dt_ms']==.1)
        fine=next(r for r in rows if r['seed']==11 and r['condition']==ci and r['dt_ms']==.05)
        delta=dict(condition=ci,coarse_label=coarse['label'],fine_label=fine['label'])
        for metric in ['E_Hz','I_Hz','median_ISI_CV','F1','c1','P','dominant_Hz']:
            delta[metric+'_coarse']=coarse[metric];delta[metric+'_fine']=fine[metric]
        deltas.append(delta)
    (run/'numerical_sensitivity.json').write_text(json.dumps(deltas,indent=2))
    manifest=[]
    for path in sorted(run.rglob('*')):
        if path.is_file() and path.name!='artifact_manifest.json':
            digest=hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda:stream.read(1<<20),b''):digest.update(block)
            manifest.append(dict(path=str(path.relative_to(run)),bytes=path.stat().st_size,
                                 sha256=digest.hexdigest()))
    (run/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2))
    assessment=json.loads((run/'assessment.json').read_text())
    lines=['# Deterministic result assessment and claim-evidence matrix',
           'No thresholds, seeds, model parameters, durations or display windows changed after outcomes. The operational definitions are in the locked NeuroSpecification.md.',
           '| Condition | Requested label | Primary labels (seeds 11,29,47) | Fine dt label (seed 11) | Frozen verdict |',
           '|---|---|---|---|---|']
    for a in assessment:
        lines.append(f"| {a['condition']} | {a['requested']} | {'; '.join(a['primary_labels'])} | {a['fine_label']} | {a['outcome']} |")
    lines.extend(['','Each result points to metrics/seed-SEED_dt-DT_condition-C.json and .npz, with the exact raw file in its raw_file field. raw_audit.json independently recovers E/I counts from raw bit-packed events and verifies CV/eligibility for the fixed sample. numerical_sensitivity.json retains every paired coarse/fine statistic. artifact_manifest.json records file identity.',
      '', '| Claim | Evidence | Scope / limitation |','|---|---|---|',
      '| Supplied network and drive implemented | code/model.py, config.json, graph_checks.json, checks.json at project root | Finite time grid, resting voltage/refractory choices delegated |',
      '| Exact graph indegrees/sign/delay | Saved graphs, full graph checks; impulse assertions in checks.py and checks.json | Scalar grid-aligned 1.5 ms delay |',
      '| Reproducible compiled simulation | checks.json exact spike/voltage/refractory/RNG parity and replay; acceleration.json full-size parity | CPU float32; no mid-rollout resume claimed |',
      '| Per-condition regimes | assessment.json, metrics.json and per-neuron/PSD evidence | Frozen operational predicates; no phase or reproduction claim |',
      '| Numerical sensitivity | numerical_sensitivity.json, all four fine-dt raw runs | One paired seed, not exact trajectory matching |',
      '| Saved figure data integrity | raw_audit.json and diagnostic-figures/source_checks.json | Fixed first 500 ms display; full 3 s for means/statistics |',
      '', 'Proposed next action: independent read-only Codex review under the user’s no-reference restriction; finalize figures only after PASS.'])
    (root/'result-assessment.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(audited_runs=len(checks),all_passed=True,artifact_count=len(manifest))))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--run',required=True)
    audit(parser.parse_args().run)
