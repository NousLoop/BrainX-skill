"""Recompute every saved spectrum through BrainTools, preserving raw simulations."""
import jax
jax.config.update('jax_enable_x64',True)  # Offline analysis only; no simulation.
import hashlib
import json
import time
from pathlib import Path
import numpy as np
import experiment

root=Path(__file__).resolve().parent
parent=root/'runs/locked-baseline-v2'
out=root/'analysis-iteration-2/braintools-final'
config=json.loads((out/'config.json').read_text())
for name,digest in config['input_sha256'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
(out/'metrics').mkdir(exist_ok=True)
rows=json.loads((parent/'metrics.json').read_text())
new_rows=[];checks=[]
start=time.perf_counter()
for row in rows:
    name=f"seed-{row['seed']}_dt-{row['dt_ms']:g}_condition-{row['condition']}"
    with np.load(parent/'metrics'/f'{name}.npz') as data:
        counts=data['counts_EI']
        rebin=round(.1/row['dt_ms'])
        counts=counts.reshape(-1,rebin,2).sum(axis=1)
        measured,freq,psd=experiment.assess(counts,data['ISI_CV'],.1)
        original=data['PSD_Hz2_per_Hz']
        assert np.array_equal(freq,data['frequency_Hz'])
        assert np.allclose(psd,original,rtol=1e-8,atol=1e-12)
        for metric in ['E_Hz','I_Hz','global_Hz','median_ISI_CV','F1','c1','P','Q']:
            assert np.isclose(measured[metric],row[metric],rtol=1e-8,atol=1e-12), (name,metric)
        assert measured['dominant_Hz']==row['dominant_Hz']
        assert measured['label']==row['label']
        checks.append(dict(name=name,frequency_exact=True,label_exact=True,
                           relative_P_error=abs(measured['P']/row['P']-1),
                           absolute_Q_error=abs(measured['Q']-row['Q']),
                           PSD_max_absolute_error=float(np.max(abs(psd-original))),
                           PSD_relative_L2_error=float(np.linalg.norm(psd-original)/np.linalg.norm(original))))
        new=dict(row);new.update(measured);new['spectral_backend']='BrainTools spectrogram, float64 offline'
        new_rows.append(new)
        np.savez_compressed(out/'metrics'/f'{name}.npz',frequency_Hz=freq,PSD_Hz2_per_Hz=psd)
(out/'metrics.json').write_text(json.dumps(new_rows,indent=2))
(out/'assessment.json').write_bytes((parent/'assessment.json').read_bytes())
summary=dict(all_16_PSDs_pass=True,all_labels_exact=True,all_peak_frequencies_exact=True,
             no_raw_or_model_changes=True,offline_precision='float64',
             model_precision='unchanged float32',execution_seconds=time.perf_counter()-start,
             maximum_relative_P_error=max(c['relative_P_error'] for c in checks),
             maximum_absolute_Q_error=max(c['absolute_Q_error'] for c in checks),
             results=checks)
(out/'parity.json').write_text(json.dumps(summary,indent=2))
for name,digest in config['input_sha256'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
print(json.dumps(summary,indent=2),flush=True)
