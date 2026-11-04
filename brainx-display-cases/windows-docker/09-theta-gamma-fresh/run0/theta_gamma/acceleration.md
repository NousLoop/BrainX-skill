# BrainX acceleration audit

| File/area | Pattern | Evidence | Axis | Impact | Risk | Rewrite | Confidence |
|---|---|---|---|---|---|---|---|
| model.py run_model | already-fused | Simulator JIT + state-aware loop | T | high | low | retain | high |
| IllustrativeWC states | native batched State | (IC=3,condition=25), parameters broadcast per condition | B/E | high | medium | retain; no added vmap | high |
| analysis.py | host offline statistics | signal arrays serialized/converted with explicit seconds | none | low at this scale | low | no State transform | high |

## Patch / rewrite plan

Explicit unchanged decision: use the owning Simulator and native batch axes from
the start. No custom control flow, multi-device transform or memory checkpointing
is justified. Each lane has independent rE/rI and applied_P State; only read-only
parameters and prescribed protocol are shared. No dynamics RNG. The native loop
has no host interaction. Inputs/outputs have fixed shape and float64 dtype.

## Validation evidence

`checks/verification.json`: exact batch/scalar trajectories and final State,
exact reset/replay, same-model Simulator default reset, JIT/unjitted small-run
parity; equation/input/bounds witnesses. All errors for these parity checks are
zero except input roundoff (~2.2e−16). Synthetic R and native MI parity are also saved.

No cached steady speedup is claimed: Simulator owns/rebuilds its internal callable,
so reported timings are synchronized end-to-end, including compilation, execution,
and host serialization. The first 20 ms six-lane rollout took ~0.13 s on CPU.
Production and convergence runtime/RSS are saved in each run's metrics/runtime.json.

## Memory and remaining risks

Full retained E/I/input histories are required for the proxy/filter/phase analysis.
Simulator may stack full integration-resolution monitors before sampling (~216 MB
for 120k × 75 × 3 float64 values); final retained raw arrays are ~18 MB uncompressed.
No dense connectivity is created. CPU avoids accelerator dispatch and costs.
Float64 and fixed shape selected before production. No training/gradient coverage.
Euler's phase error remains a scientific risk addressed by the locked dt-halving
comparison; performance choices cannot override that result.
