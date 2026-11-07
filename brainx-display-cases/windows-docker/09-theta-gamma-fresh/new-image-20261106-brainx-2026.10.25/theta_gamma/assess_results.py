"""Audit saved evidence and emit a deterministic, reviewable result assessment."""
import hashlib
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

run=ROOT/'runs/production-02'
r=np.load(run/'raw/trajectories.npz');o=np.load(run/'raw/observations.npz');m=np.load(run/'metrics/analysis.npz');d=np.load(run/'metrics/decision.npz')
s=json.loads((run/'metrics/summary.json').read_text());c=json.loads((run/'config.json').read_text())
assert r['rE'].shape==(12000,3,49) and m['profile'].shape==(18,3,49,5)
assert m['bin_counts'].min()>0 and m['cycle_counts'].size==60
reconstructed=np.tile(d['baseline_valid'],(1,7))&(m['gamma_rms'][...,0]>.005)&(d['delta_R']>.05)&(m['R'][...,2]>m['null95'][...,2])
assert np.array_equal(reconstructed,d['nested'])
assert np.allclose(o['eeg']-o['latent'],np.broadcast_to(o['theta']+o['noise'],o['eeg'].shape))
assert np.isfinite(r['input_E_left']).all()
assert np.allclose(r['input_E_left'][:,r['depth']==0],c['drive'])
assert np.isfinite(m['R']).all()
# Reconstruct every claim-relevant statistic from the retained envelope and phase.
k=m['window_mask'];ph=2*np.pi*6*r['t_s'][k]
env=m['envelope'][k]
R=np.abs(np.mean(env*np.exp(1j*ph)[:,None,None,None],axis=0))/np.maximum(env.mean(axis=0),1e-15)
assert np.allclose(R,m['R'],atol=1e-12)
comparison=np.load(ROOT/'runs/production-01/raw/trajectories.npz')
assert np.array_equal(comparison['rE'],r['rE']) and np.array_equal(comparison['rI'],r['rI'])
checks={}
for rid in ['smoke-01','calibration-01','production-01','production-02']:
    base=ROOT/'runs'/rid
    manifest=json.loads((base/'artifact_manifest.json').read_text())
    mismatches=[name for name,v in manifest.items() if sha(base/name)!=v['sha256']]
    # status is explicitly mutable; first smoke launcher recorded its earlier version.
    immutable_mismatches=[x for x in mismatches if x!='status.json']
    assert not immutable_mismatches,(rid,immutable_mismatches)
    checks[rid]={'all_immutable_hashes_match':True,'mutable_status_hash_mismatch':mismatches==['status.json'],'exit_code':int((base/'exit_code').read_text())}
checks.update(statistic_reconstruction=True,exact_old_new_dynamics=True,paired_noise=True,nonempty_phase_bins=True,complete_cycles=60)
(ROOT/'evidence/integrity.json').write_text(json.dumps(checks,indent=2))
# Simple CSVs expose every continuous sweep quantity without loading the binary arrays.
headers=['lane','initial_E','initial_I','observation_seed','depth','relative_gain','absolute_gain','gamma_rms_E','gamma_peak_Hz','baseline_gamma_valid','R_eeg','delta_R','null95_eeg','MI_eeg','R_latent','R_eonly','R_leakage','null95_leakage','nested']
rows=[]
for lane in range(3):
    for j in range(49):
        rows.append([lane,*r['initial'][lane],c['observation_seeds'][lane],r['depth'][j],r['relative_gain'][j],r['absolute_gain'][j],m['gamma_rms'][lane,j,0],m['gamma_peak_Hz'][lane,j],int(d['baseline_valid'][lane,j%7]),m['R'][lane,j,2],d['delta_R'][lane,j],m['null95'][lane,j,2],m['MI'][lane,j,2],m['R'][lane,j,1],m['R'][lane,j,3],m['R'][lane,j,4],m['null95'][lane,j,4],int(d['nested'][lane,j])])
np.savetxt(ROOT/'evidence/sweep.csv',np.asarray(rows),delimiter=',',header=','.join(headers),comments='')
np.savetxt(ROOT/'evidence/R_map_lane0.csv',m['R'][0,:,2].reshape(7,7),delimiter=',')
idx=s['display_index'];ctrl=s['control_index']
text=f'''# Deterministic result assessment

- Run: production-02; scientific outcome: {s['scientific_outcome']}; review pending.
- All results provisional until independent Codex PASS. Proposed next action: step 5 independent read-only MCP review; after PASS final rendering/report only.
- Exact decision reconstructed from saved arrays in assess_results.py; all 147 conditions retained.
- Display case: relative gain 1, depth .6; indices control={ctrl}, intervention={idx}. Gamma peak 29.5→27.5 Hz (operational band 25–90 Hz).
- R values: {s['control_R']} → {s['display_R']}; paired deltas {s['display_delta_R']}; exact cycle-rotation null95 {s['display_null95']}.
- All 3 lanes pass full fixed predicate. These are deterministic initial-State/observation-seed sensitivities, not 3 independent biological replicates.
- MI_eeg: {m['MI'][:,idx,2].tolist()}; E-only R: {s['display_eonly_R']}; latent E−0.5I R: {s['display_latent_R']}.
- Theta+noise-only R: {s['leakage_R']}; corresponding null95: {m['null95'][:,idx,4].tolist()}. Each is below its own null95; noise can still yield nonzero sample PAC.
- Phase pattern: envelope is *suppressed near maximum E drive* (phase zero); the phase profile has two broad flanks, so its first-moment phase is not a unique burst location. Do not claim drive maxima maximize gamma.
- Sweep: 18/49 samples per lane satisfy the full predicate. 14/49 samples per lane have ineligible matched baselines: relative gain .7 is nearly stationary, gain 1.3 has dominant 24.5 Hz below the declared gamma band despite finite gamma-band power. Red X indicates these cannot establish modulation of an existing gamma baseline. Of 35 eligible sampled conditions, 17 fail the declared nesting rule; all retained.
- Nonmonotonic counterexample: gain 1.1, m=.6→.8: R={m['R'][0,32,2]:.6f}→{m['R'][0,39,2]:.6f}. At gain .8, R peaks at sampled m=.4 and declines thereafter. No monotonic law or continuous region is supported.
- Numerical convergence: {s['convergence']}. Baseline and intervention are both tested for all 7 gains at m=0,.6,1 (lane 0); this is bounded validation, not a proof for all unsampled conditions.
- Invariant-domain checks pass; negative abstract E down to {s['domains'][0]['min']:.6f} is allowed by the offset sigmoid, not a physiological negative firing-rate claim.
- Fixed parameters are illustrative, and baseline was outcome-calibrated by the separately locked unmodulated-only rule. There is no empirical or biological parameter inference.
- Scope: the imposed theta input is conditionally sufficient for known-phase gamma-envelope dependence in this model and measurement construction. Broad-band PAC does not isolate pure amplitude modulation from waveform changes, harmonics, frequency modulation or mixtures. No endogenous theta or unique biological mechanism is inferred.

| Claim | Decisive evidence | Allowed interpretation / limitation |
|---|---|---|
| Unmodulated gamma exists at display gain | calibration.npz; metrics/analysis.npz psd_E; decision.npz broad_peak_Hz | Oscillatory synthetic baseline, 29.5 Hz under operational band |
| External theta modulation changes phase nesting | saved envelope, known input phase, exact null rotations, delta_R and full predicate | Conditional input intervention effect only |
| Withdrawal removes most nesting but retains gamma | paired m=0 at each same gain; display R≈0 and gamma 29.5 Hz | Separate matched runs from identical t=0 State; no within-run switch claim |
| EEG proxy reflects the pattern | observations.npz, proxy PSD and R, E-only sensitivity, theta+noise leakage check | Synthetic arbitrary-unit observation; theta remains present in proxy under both conditions |
| Depth and gain matter nonmonotonically | evidence/sweep.csv; R_map_lane0.csv; raw grid axes and validity masks | Sampled points only; ineligible and failed cases included |
| Numerical and execution contracts hold | tests.json, integrity.json, convergence.npz, source/provenance hashes | Explicit tested resolution and State/control contracts |
| No mechanism uniqueness | construction and observation limitations | This is an illustrative sufficiency demonstration, not mechanism identification |

Raw binaries: runs/production-02/raw/trajectories.npz, observations.npz, refinement.npz. Analysis binaries: runs/production-02/metrics/analysis.npz, decision.npz, convergence.npz, refinement.npz. Full lineage and superseded run: evidence/run-lineage.md. No exclusions or failed hypotheses hidden.
'''
(ROOT/'evidence/result-assessment.md').write_text(text)
print('Assessment reconstructed; immutable hashes verified.')
