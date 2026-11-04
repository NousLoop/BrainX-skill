# BrainX acceleration audit — iteration 2

| File/area | Pattern | Evidence | Axis | Impact | Risk | Rewrite | Confidence |
|---|---|---|---|---|---|---|---|
| model.py | already-fused native Simulator | inherited JIT/time loop, (3,25) State | T/B/E | high | low | unchanged | high |
| activation | native stateless sigmoid | explicit parity witness | population | low | low | replaces manual expression | high |
| carrier analysis | host offline observation/statistics | native PSD plus SciPy peak timing, no stateful writes | none | modest | low | no transform needed | high |

## Decision and evidence

Restudied acceleration inventory/correctness/State/timing requirements. No performance
rewrite warranted. `checks/verification.json` proves equation, native sigmoid, batch/scalar
outputs and final State, same-object reset, JIT parity, synthetic PAC and harmonic-negative
carrier checks. No dynamics RNG. Native batching retains separate rE/rI/applied_P lanes.
Run timings include compile/dispatch/synchronization/host conversion, with no cached
steady speedup claim. Full integration-resolution intermediate monitor estimate is
~432 MB (240k × 75 × 3 × 8 bytes); retained 1 kHz raw is ~18 MB.
Production and dt-half RSS/end-to-end timings will be in immutable run artifacts.
Numerical acceptance remains a separate gate; no optimization can override its outcome.
