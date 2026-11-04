# Claim–evidence matrix (accepted illustrative scope; review iteration 2 PASS)

| User question / claim | Observable | Evidence | Boundary |
|---|---|---|---|
| E/I gamma circuit, iteration 2 | E/I cycle rate + dominant native Welch peak, agreement, interval CV, p2p and count | metrics.json E_cycle/I_cycle and autonomous_gamma_predicate at m=0; assessment.json | initial iteration failed; revised tau scale is outcome-calibrated and illustrative |
| theta phase nesting | known-drive phase vs gamma envelope R, MI and bins | raw/derived.npz phase_curves, phase_counts, surrogates_R; fixed-pair assessment | imposed 6 Hz source; no claim of intrinsic theta |
| removal of modulation | matched m=0 at each g and IC, same constant mean drive and observation | raw P, metrics for every control, assessment control_input_exact | only the periodic input term is removed; theta mixture stays by design |
| simulated EEG proxy | y=E−0.5I+0.2cosφ, y without theta, E, E−I | raw derived proxy/base; all four readout metrics and native MI | no physical EEG units or measurement model; nonsinusoidal harmonics may contribute |
| depth × gain scan | R, ΔR, MI, validity margins and peak frequency at all 25×3 points | config axes, metrics.csv/JSON, scan figure | discrete descriptive samples; no inferred continuous phase boundary or multiplicity-corrected map |
| observation robustness | signs/magnitudes of paired effect across 4 mappings | assessment comparison rows | these four linear readouts only; source mixing remains non-identifiable |
| numerical reliability | equation witness, independent adaptive solver, batch/scalar/final State parity, reset, dt half | checks/verification.json and logs; convergence run; assessment | Euler transient phase error retained; full scan not dt certified |
| no scientific selectivity | null/invalid settings and failed checks | failure-log.md, iterations/iteration-1, both iterations' full raw/metrics/manifests, reviews/iteration-1.md | revised tau/carrier criteria disclosed before iteration-2 production; no original evidence removed |
