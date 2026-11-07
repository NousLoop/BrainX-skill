# BrainX acceleration audit

| File/area | Pattern | Evidence | Axis | Impact | Risk | Rewrite | Confidence |
|---|---|---|---|---|---|---|---|
| model.simulate | already-fused | BrainMass Simulator.run(jit=True) owns State-aware loop | time | high | low | unchanged | high |
| parameter grid | native condition arrays | in_size=49, independent E/I per condition | conditions | high | low | native vectorization | high |
| sensitivity lanes | native batched State | batch_size=3, fixed initial values | batch | medium | low | unchanged | high |
| observation/metrics | host analysis boundary | NumPy statistics and file output after simulation | host | low | low | unchanged | high |

## Patch / rewrite plan
No custom simulation rewrite is warranted. The highest-level runner already compiles time and vectorizes independent conditions. No raw JAX transform encloses State. No speedup or warm-runtime claim is made, because Simulator owns/reconstructs its internal callable; per-run elapsed values include compilation and execution. This is an explicit unchanged decision, not a fabricated optimization.

## Validation plan and evidence
`tests.json`: JIT and non-JIT histories, time, final E/I agree to 1e−12; vector condition/initial lane agrees with scalar execution; exact reset replay. The model has no runtime RNG. Observation noise is independent between seeds and shared between matched conditions, as specified. Training/gradients not applicable. Shapes are fixed per run. Full trajectories are necessary for spectral/phase analysis; Simulator keeps every tenth post-update point. Estimated full step output before decimation: 140000×3×49×2×8≈329 MB plus compiler/analysis intermediates. Retained E/I≈28 MB; actual peak RSS will be recorded.

## Remaining risks
Performance is CPU-scale, and production/refinement use separate compilations. Numerical refinement and physical-time alignment are validated in the experiment. No multi-device execution or invented vmap requirement. Exact API routes: simulator-input-monitor-api.md, batch-transform-acceleration.md; no lower-level State transform introduced.
