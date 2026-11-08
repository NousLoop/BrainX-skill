"""Public BrainTools PSD capability assessment using immutable saved rates."""
import json
import time
import argparse
from pathlib import Path
import numpy as np
import scipy.signal
import braintools
import brainunit as u

root=Path(__file__).resolve().parent
run=root/'runs/locked-baseline-v2'
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='analysis-iteration-2')
args=parser.parse_args()
out=root/args.output
out.mkdir(parents=True,exist_ok=True)
rows=json.loads((run/'metrics.json').read_text())
rates=[]
for row in rows:
    name=f"seed-{row['seed']}_dt-{row['dt_ms']:g}_condition-{row['condition']}"
    with np.load(run/'metrics'/f'{name}.npz') as data:
        counts=data['counts_EI'].sum(axis=1)
    rebin=round(.1/row['dt_ms'])
    counts=counts.reshape(-1,rebin).sum(axis=1)
    rates.append(counts/(12500*.0001))
signals=np.stack(rates,axis=1)
t0=time.perf_counter()
freq,native=braintools.analysis.spectral.power_spectral_density(
    signals*u.Hz,dt=.1*u.ms,nperseg=10000,noverlap=5000)
freq,native=np.asarray(freq),np.asarray(native)
elapsed=time.perf_counter()-t0
assert freq.shape==(5001,) and native.shape==(5001,16)
assert np.all(np.isfinite(native)) and np.all(native>=0)
freq_seconds,psd_seconds=braintools.analysis.spectral.power_spectral_density(
    signals,dt=.0001,nperseg=10000,noverlap=5000)
assert np.allclose(freq,freq_seconds,rtol=1e-6,atol=.001)
assert np.allclose(native,psd_seconds,rtol=2e-6,atol=1e-9)

t0=time.perf_counter()
frozen=[];symmetric=[];symmetric_no_detrend=[]
for rate in rates:
    f,p=scipy.signal.welch(rate,fs=10000,window='hann',nperseg=10000,
                            noverlap=5000,detrend='constant',scaling='density')
    _,s=scipy.signal.welch(rate,fs=10000,window=np.hanning(10000),nperseg=10000,
                            noverlap=5000,detrend='constant',scaling='density')
    _,s0=scipy.signal.welch(rate,fs=10000,window=np.hanning(10000),nperseg=10000,
                             noverlap=5000,detrend=False,scaling='density')
    frozen.append(p);symmetric.append(s);symmetric_no_detrend.append(s0)
frozen=np.stack(frozen,axis=1);symmetric=np.stack(symmetric,axis=1)
symmetric_no_detrend=np.stack(symmetric_no_detrend,axis=1)
reference_seconds=time.perf_counter()-t0
assert np.allclose(freq,f,rtol=1e-6,atol=.001)
# Use the exact physical 1 Hz bin centers after checking the returned grid.
# This avoids a float32 rounding artifact at the 1/1000 Hz band boundaries.
band=(f>=1)&(f<=1000)
low=(f>=1)&(f<=50)

def stats(psd):
    peak=np.flatnonzero(band)[np.argmax(psd[band])]
    return dict(dominant_Hz=float(f[peak]),P=float(psd[peak]/np.median(psd[band])),
                Q=float(psd[low].sum()/psd[band].sum()))

def label(row,s):
    synchronous=row['F1']>=5 and row['c1']>=.15 and s['P']>=10
    asynchronous=row['F1']<5 and row['c1']<.15
    if synchronous and row['regularity']=='regular':return 'synchronous regular'
    if synchronous and row['regularity']=='irregular':
        return ('fast' if s['dominant_Hz']>=50 else 'slow')+' synchronous irregular'
    if asynchronous and row['regularity']=='irregular':return 'asynchronous irregular'
    return 'inconclusive'

evidence=[]
for j,row in enumerate(rows):
    locked,native_stats=stats(frozen[:,j]),stats(native[:,j])
    assert locked['dominant_Hz']==row['dominant_Hz']
    assert np.isclose(locked['P'],row['P'],rtol=1e-12)
    assert np.isclose(locked['Q'],row['Q'],rtol=1e-12)
    assert label(row,locked)==row['label']
    error=np.linalg.norm(native[:,j]-frozen[:,j])/np.linalg.norm(frozen[:,j])
    sym_error=np.linalg.norm(native[:,j]-symmetric[:,j])/np.linalg.norm(symmetric[:,j])
    sym0_error=np.linalg.norm(native[:,j]-symmetric_no_detrend[:,j])/np.linalg.norm(symmetric_no_detrend[:,j])
    evidence.append(dict(seed=row['seed'],dt_ms=row['dt_ms'],condition=row['condition'],
                         locked=locked,native=native_stats,locked_label=row['label'],
                         native_label=label(row,native_stats),relative_L2_error=float(error),
                         relative_error_to_symmetric_detrended=float(sym_error),
                         relative_error_to_symmetric_not_detrended=float(sym0_error),
                         peak_same=locked['dominant_Hz']==native_stats['dominant_Hz'],
                         label_same=row['label']==label(row,native_stats)))

# Public contract has no detrend control: characterize constant-offset behavior.
t=(np.arange(30000)+1)*.0001
fixture=100+40*np.sin(2*np.pi*23*t)
fixture_f,fixture_p=braintools.analysis.spectral.power_spectral_density(
    fixture,dt=.1*u.ms,nperseg=10000,noverlap=5000)
_,fixture_ref=scipy.signal.welch(fixture,fs=10000,window='hann',nperseg=10000,
                                noverlap=5000,detrend='constant',scaling='density')
fixture_p=np.asarray(fixture_p)
np.savez_compressed(out/'PSD_comparison.npz',frequency_Hz=f,
                    native_frequency_Hz=freq,native_PSD=native,frozen_PSD=frozen,
                    symmetric_detrended_PSD=symmetric,
                    symmetric_not_detrended_PSD=symmetric_no_detrend,
                    known_fixture_native=fixture_p,known_fixture_frozen=fixture_ref)
summary=dict(api='braintools.analysis.spectral.power_spectral_density',
             contract='api-docs/power_spectral_density.txt',
             model_or_state_changes=False,runs_compared=len(evidence),
             input_shape=list(signals.shape),output_shape=list(native.shape),
             time_unit_parity=True,canonical_signal_magnitude_unit='Hz/neuron',
             frequency_unit='Hz',PSD_unit='(Hz/neuron)^2/Hz',
             native_seconds=elapsed,
             reference_three_estimators_seconds=reference_seconds,
             known_fixture_native_DC=float(fixture_p[0]),
             known_fixture_frozen_DC=float(fixture_ref[0]),
             all_peaks_same=all(r['peak_same'] for r in evidence),
             all_labels_same=all(r['label_same'] for r in evidence),
             results=evidence)
(out/'spectral_api_check.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
