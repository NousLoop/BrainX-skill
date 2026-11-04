# Deterministic result assessment (accepted illustrative scope)
Scientific outcome: supported; review PASS; see reviews/iteration-2.md.
Controls exact: True; State bounded/finite: True; tests PASS: True.
Numerical predicate: True; max ΔR=0.001347, max Δpeak=0.00 Hz.

| Readout | IC | off R | on R | ΔR | off/on valid gamma | on cycle-null q95 | strong predicate |
|---|---:|---:|---:|---:|---|---:|---|
| proxy | 0 | 0.000272 | 0.501625 | 0.501353 | True/True | 0.125484 | True |
| proxy | 1 | 0.000214 | 0.501625 | 0.501410 | True/True | 0.125484 | True |
| proxy | 2 | 0.000289 | 0.501625 | 0.501335 | True/True | 0.125484 | True |
| no_theta | 0 | 0.000272 | 0.501624 | 0.501353 | True/True | 0.125484 | True |
| no_theta | 1 | 0.000214 | 0.501624 | 0.501410 | True/True | 0.125484 | True |
| no_theta | 2 | 0.000289 | 0.501624 | 0.501335 | True/True | 0.125484 | True |
| E | 0 | 0.000223 | 0.486550 | 0.486327 | True/True | 0.121715 | True |
| E | 1 | 0.000169 | 0.486550 | 0.486381 | True/True | 0.121715 | True |
| E | 2 | 0.000243 | 0.486550 | 0.486307 | True/True | 0.121715 | True |
| E_minus_I | 0 | 0.000312 | 0.494341 | 0.494029 | True/True | 0.123713 | True |
| E_minus_I | 1 | 0.000275 | 0.494341 | 0.494066 | True/True | 0.123713 | True |
| E_minus_I | 2 | 0.000305 | 0.494341 | 0.494036 | True/True | 0.123713 | True |

No post-outcome tuning. The two failed implementation/verification witnesses are disclosed in failure-log.md.
Iteration 1 remains a partial failure (~22 Hz carrier with gamma harmonic), archived under iterations/iteration-1 and runs/*-01. Its original band-only predicates must not be interpreted as carrier certification.
Iteration 2 common tau scaling is outcome-calibrated and illustrative. Current strong_predicate requires a valid autonomous E/I gamma carrier, current band/timing validity, ΔR>0.05 and complete-cycle null exceedance. legacy_band_valid retains the original weaker predicate only.
All parameter points and native single-signal PAC values remain in metrics.json/CSV. Undefined gamma peak is null, not a detected oscillation.
Numerical certification is limited to the fixed g=1 pair; scan points are descriptive at dt=0.05 ms.
The imposed theta source and theta mixture are exogenous. PAC/surrogates are deterministic descriptive statistics, not animal-level inference.
No unique mechanism or real EEG correspondence follows from this model.
