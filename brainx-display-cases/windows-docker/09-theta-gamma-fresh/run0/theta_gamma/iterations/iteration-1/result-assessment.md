# Deterministic result assessment (provisional until independent review)
Scientific outcome: partially_supported; review pending.
Controls exact: True; State bounded/finite: True; tests PASS: True.
Numerical predicate: True; max ΔR=0.002044, max Δpeak=0.00 Hz.

| Readout | IC | off R | on R | ΔR | off/on valid gamma | on cycle-null q95 | strong predicate |
|---|---:|---:|---:|---:|---|---:|---|
| proxy | 0 | 0.000112 | 0.209661 | 0.209549 | True/True | 0.052125 | True |
| proxy | 1 | 0.000166 | 0.209661 | 0.209496 | True/True | 0.052125 | True |
| proxy | 2 | 0.000106 | 0.209661 | 0.209555 | True/True | 0.052125 | True |
| no_theta | 0 | 0.000112 | 0.209661 | 0.209549 | True/True | 0.052125 | True |
| no_theta | 1 | 0.000166 | 0.209661 | 0.209495 | True/True | 0.052125 | True |
| no_theta | 2 | 0.000106 | 0.209661 | 0.209555 | True/True | 0.052125 | True |
| E | 0 | 0.000162 | 0.217678 | 0.217516 | True/True | 0.054127 | True |
| E | 1 | 0.000251 | 0.217678 | 0.217427 | True/True | 0.054127 | True |
| E | 2 | 0.000116 | 0.217678 | 0.217561 | True/True | 0.054127 | True |
| E_minus_I | 0 | 0.000131 | 0.202113 | 0.201982 | True/True | 0.050228 | True |
| E_minus_I | 1 | 0.000101 | 0.202113 | 0.202011 | True/True | 0.050228 | True |
| E_minus_I | 2 | 0.000166 | 0.202113 | 0.201946 | True/True | 0.050228 | True |

No post-outcome tuning. The two failed implementation/verification witnesses are disclosed in failure-log.md.
Post-run checks/carrier-audit.json finds ~22 Hz autonomous E cycles: the 43.5 Hz band peak is a harmonic. The original gamma-band predicate passes but does NOT establish a gamma circuit. Scientific outcome is therefore partially_supported, not supported.
All parameter points and native single-signal PAC values remain in metrics.json/CSV. Undefined gamma peak is null, not a detected oscillation.
Numerical certification is limited to the fixed g=1 pair; scan points are descriptive at dt=0.1 ms.
The imposed theta source and theta mixture are exogenous. PAC/surrogates are deterministic descriptive statistics, not animal-level inference.
No unique mechanism or real EEG correspondence follows from this model.
