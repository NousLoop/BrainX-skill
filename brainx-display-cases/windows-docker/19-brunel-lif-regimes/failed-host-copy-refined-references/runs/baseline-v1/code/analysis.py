"""Frozen descriptive statistics and regime predicates; host analysis only."""
import json
from pathlib import Path
import numpy as np
import scipy.signal
import model

TARGETS=['SR','fast SI','AI','slow SI']
PAIRS=[(3.,2.),(6.,4.),(5.,2.),(4.5,.9)]


def synchrony(counts,dt_ms):
    size=int(round(5/dt_ms))
    k=np.asarray(counts).reshape(-1,size).sum(axis=1).astype(float)
    return float(np.sqrt(max(k.var()-k.mean(),0.))/k.mean()) if k.mean() else 0.


def sync_category(s):
    return 'synchronous' if s>=.10 else ('asynchronous' if s<=.05 else 'inconclusive')


def summarize(raw_path,out_dir,burn_ms=1000.):
    raw=np.load(raw_path)
    dt=float(raw['dt_ms']);steps=int(raw['steps']);ne=int(raw['ne']);ni=int(raw['ni']);n=ne+ni
    burn=int(round(burn_ms/dt));duration=(steps-burn)*dt/1000
    counts=raw['counts'][burn:].astype(np.int64)
    total=counts.sum(axis=1)
    rates=counts.sum(axis=0)/np.array([ne,ni])/duration
    allrate=float(total.sum()/n/duration)
    halves=np.stack([counts[:len(counts)//2].sum(axis=0),counts[len(counts)//2:].sum(axis=0)])/(duration/2)/np.array([ne,ni])
    drift=np.abs(halves[1]-halves[0])/np.maximum(rates,1e-12)
    s=synchrony(total,dt)
    hs=[synchrony(x,dt) for x in np.array_split(total,2)]
    sync=sync_category(s)
    stable_sync=all(sync_category(x)==sync for x in hs)
    stationarity=bool(np.all(drift<=.20) and stable_sync)

    # All-neuron ISI CV, requiring at least 20 complete post-burn intervals.
    cvs=np.full(n,np.nan)
    spike_counts=np.zeros(n,np.int32)
    min_isi=np.inf
    packed=raw['packed']
    # Chunk neurons at a packed byte boundary to keep memory bounded.
    for left in range(0,n,256):
        right=min(left+256,n)
        sp=np.unpackbits(packed[burn:,left//8:(right+7)//8],axis=1,
                         bitorder='little',count=right-left).T.copy()
        for local,events in enumerate(sp):
            times=np.flatnonzero(events)
            spike_counts[left+local]=len(times)
            intervals=np.diff(times)*dt
            if len(intervals):min_isi=min(min_isi,float(intervals.min()))
            if len(intervals)>=20:cvs[left+local]=intervals.std()/intervals.mean()
    assert np.array_equal([spike_counts[:ne].sum(),spike_counts[ne:].sum()],counts.sum(axis=0))
    assert min_isi>=2.-1e-7
    eligible=float(np.mean(np.isfinite(cvs)))
    median=float(np.nanmedian(cvs)) if eligible else None
    regularity='inconclusive'
    if eligible>=.5:
        regularity='regular' if median<=.5 else ('irregular' if median>=.7 else 'inconclusive')

    factor=int(round(.1/dt))
    globalrate=total.reshape(-1,factor).sum(axis=1)/(n*.0001)
    f,p=scipy.signal.welch(globalrate-globalrate.mean(),fs=10000.,window='hann',nperseg=10000,
                            noverlap=5000,detrend='constant',scaling='density')
    full_f,full_p=scipy.signal.periodogram(globalrate,fs=10000.,window='boxcar',detrend='constant',scaling='density')
    band=(f>=1)&(f<=500)
    peak=int(np.flatnonzero(band)[np.argmax(p[band])]);freq=float(f[peak])
    background=float(np.median(p[band & (np.abs(f-freq)>5)]))
    peak_ratio=float(p[peak]/max(background,np.finfo(float).tiny))
    concentration=float(p[band & (np.abs(f-freq)<=2)].sum()/p[band].sum()) if p[band].sum() else 0.
    oscillation=bool(peak_ratio>=5 and concentration>=.1)
    requested=TARGETS[int(raw['condition'])]
    predicates={'stationary':stationarity,'synchronous':sync=='synchronous',
                'asynchronous':sync=='asynchronous','regular':regularity=='regular',
                'irregular':regularity=='irregular','oscillatory':oscillation,
                'fast':freq>=50,'slow':freq<50}
    required={'SR':['stationary','synchronous','regular'],
              'fast SI':['stationary','synchronous','irregular','oscillatory','fast'],
              'AI':['stationary','asynchronous','irregular'],
              'slow SI':['stationary','synchronous','irregular','oscillatory','slow']}[requested]
    match=all(predicates[k] for k in required)
    uncertain=(not stationarity or sync=='inconclusive' or regularity=='inconclusive')
    outcome='supported' if match else ('inconclusive' if uncertain else 'unsupported')
    measured=f'{sync}, {regularity}'
    if sync=='synchronous' and regularity=='irregular':
        measured=('fast SI' if freq>=50 else 'slow SI') if oscillation else 'synchronous irregular; no concentrated oscillation'
    elif sync=='synchronous' and regularity=='regular':measured='SR'
    elif sync=='asynchronous' and regularity=='irregular':measured='AI'
    summary=dict(condition=int(raw['condition']),g=float(raw['g']),eta=float(raw['eta']),seed=int(raw['seed']),
        dt_ms=dt,analysis_s=duration,E_rate_Hz=float(rates[0]),I_rate_Hz=float(rates[1]),global_rate_Hz=allrate,
        synchrony_S=s,synchrony_category=sync,half_synchrony_S=hs,half_rates_Hz=halves.tolist(),
        E_I_fractional_drift=drift.tolist(),stationary=stationarity,CV_median=median,
        E_CV_median=float(np.nanmedian(cvs[:ne])) if np.isfinite(cvs[:ne]).any() else None,
        I_CV_median=float(np.nanmedian(cvs[ne:])) if np.isfinite(cvs[ne:]).any() else None,
        CV_eligible_fraction=eligible,E_CV_eligible_fraction=float(np.mean(np.isfinite(cvs[:ne]))),
        I_CV_eligible_fraction=float(np.mean(np.isfinite(cvs[ne:]))),regularity=regularity,
        dominant_frequency_Hz=freq,peak_background_ratio=peak_ratio,peak_concentration=concentration,
        oscillation_supported=oscillation,requested=requested,required_predicates=required,
        predicates=predicates,failed_predicates=[k for k in required if not predicates[k]],
        measured_regime=measured,baseline_outcome=outcome,
        min_postburn_ISI_ms=float(min_isi) if np.isfinite(min_isi) else None,
        max_neuron_rate_Hz=float(spike_counts.max()/duration),raw_file=str(raw_path))
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    stem=Path(raw_path).stem
    np.savez_compressed(out/(stem+'.npz'),CV=cvs,neuron_spike_count=spike_counts,
        welch_frequency_Hz=f,welch_PSD_Hz2_per_Hz=p,periodogram_frequency_Hz=full_f,
        periodogram_PSD_Hz2_per_Hz=full_p,analysis_global_rate_Hz=globalrate)
    (out/(stem+'.json')).write_text(json.dumps(summary,indent=2,allow_nan=False))
    return summary


def assess(run_dir):
    root=Path(run_dir)
    summaries=[json.loads(p.read_text()) for p in sorted((root/'metrics').glob('condition*.json'))]
    results=[]
    for c,target in enumerate(TARGETS):
        base=sorted([s for s in summaries if s['condition']==c and s['dt_ms']==.1],key=lambda s:s['seed'])
        control=next(s for s in summaries if s['condition']==c and s['dt_ms']==.05)
        ref=next(s for s in base if s['seed']==101)
        rate_diff={k:abs(control[k]-ref[k])/max(ref[k],1e-12) for k in ['E_rate_Hz','I_rate_Hz']}
        category_changes=[k for k in ['synchrony_category','regularity','oscillation_supported'] if ref[k]!=control[k]]
        f_diff=abs(control['dominant_frequency_Hz']-ref['dominant_frequency_Hz'])
        frequency_flag=bool(ref['oscillation_supported'] and control['oscillation_supported'] and
                            f_diff>max(5.,.1*ref['dominant_frequency_Hz']))
        sensitive=any(d>.1 for d in rate_diff.values()) or bool(category_changes) or frequency_flag
        outcomes=[s['baseline_outcome'] for s in base]
        decision='supported' if all(x=='supported' for x in outcomes) else (
            'unsupported' if all(x=='unsupported' for x in outcomes) else 'inconclusive')
        if sensitive:decision='inconclusive'
        results.append(dict(condition=c,g=PAIRS[c][0],eta=PAIRS[c][1],requested=target,
            baseline_seed_outcomes=outcomes,numerical_sensitivity=sensitive,
            relative_rate_changes=rate_diff,changed_categories=category_changes,
            dominant_frequency_change_Hz=f_diff,frequency_flag=frequency_flag,
            decision=decision,baseline=base,control=control))
    (root/'assessment.json').write_text(json.dumps(results,indent=2,allow_nan=False))
    rows=['# Deterministic assessment and claim-evidence matrix','',
          'Frozen rules: NeuroSpecification.md. No thresholds or display seeds changed after simulation.','',
          '| (g, eta) | Requested | Seed outcomes | Numerical sensitivity | Decision |',
          '|---|---|---|---|---|']
    for r in results:
        rows.append(f"| ({r['g']}, {r['eta']}) | {r['requested']} | {', '.join(r['baseline_seed_outcomes'])} | {r['numerical_sensitivity']} | {r['decision']} |")
    rows+=['','Every baseline/control metric is in `metrics/condition*_seed*_dt*.json`; all-neuron CV and exact spectral reductions are in the corresponding NPZ. All native-grid spikes, E/I counts, final State and RNG key are in `raw/`. Graphs are in `graphs/`. Unsupported labels are retained.','',
           'The requested SR/AI/SI claims are supported only by their complete frozen predicate sets, including stationarity and numerical controls. These are operational finite-window categories, not assertions of universal phases.']
    (root/'assessment.md').write_text('\n'.join(rows)+'\n')
    return results
