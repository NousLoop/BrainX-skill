# BrainX study record — iteration 2

Completed after REFUSE and before any iteration-2 implementation changes.

| Finding | Owning skills and restudied references | Design consequence |
|---|---|---|
| BX-001 | Full general guard and BrainMass root; model library; full WC canonical script; simulator input/monitor; visualization/analysis PSD; modeling-loop steps 1–6 | Keep WC derivative extension/Simulator. Joint tau scaling 2.5/5→1.25/2.5 ms; baseline carrier must pass E/I cycle timing + native PSD checks. Fresh full driven-pair/scan/dt-half evidence. |
| BX-002 | Modeling loop review/report/diagnostic closure and general guard claim validation | Regenerate matrix; distinguish original band-only predicates from new carrier validity. Archive every original artifact. |
| BX-003 | Full BrainState root; prebuilt-activation-library functional catalog | Use brainstate.nn.sigmoid(x) directly in both derivatives; verify equation/parity and native activation equality. |

## Reaffirmed API decisions

Existing BrainTools 0.3 spectral namespace gap remains execution-verified; native
metric PSD and native single-signal PAC retained. Host SciPy filter/Hilbert and
peak timing are the smallest offline observation/statistics boundaries, not new
simulation infrastructure. No package installation or installed-source inspection.
State lifecycles, independent (IC,condition) lanes, unit-aware simulation,
actual-input ShortTermState, CPU float64 and native Simulator JIT remain.
No training/fitting coverage.

## Revised and locked experiment

User's explicit choice/lock delegation still applies. Revision 2 in NeuroSpecification
preserves initial partial failure and discloses outcome calibration of the common
population timescale. Halve numerical dt as well (0.05 ms; convergence 0.025 ms),
keeping normalized Euler step. The m/g grid, ICs, theta input, matched observation
controls, metrics, thresholds and fixed pair otherwise remain as planned.

Before production freeze new carrier checks: autonomy requires E/I cycle rate and
dominant native Welch peak in 25–100 Hz, agreement≤2 Hz, interval CV<0.2,
≥20 peaks and p2p>0.05; prominence 0.2/distance4 ms. Driven evidence requires
≥50% E/I interpeak intervals 10–40 ms plus original band criterion. All continuous
margins and counts retained; scan point causal interpretation also requires its
matched autonomous control. No expected category will be forced.

Frozen diagnostics/final display settings from iteration 1 remain, but show 3–3.5 s
for readable faster oscillations. All new figure paths end in iteration-2. New
run IDs *-02; old immutable *-01 runs are not changed. Study complete; proceed step 2.
