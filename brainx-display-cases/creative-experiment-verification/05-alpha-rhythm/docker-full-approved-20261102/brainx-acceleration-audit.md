# BrainX acceleration audit

| File/area | Pattern | Evidence | Axis | Impact | Risk | Rewrite | Confidence |
|---|---|---|---|---|---|---|---|
| `alpha_rhythm.py:run_lane` | transformed already | One `brainstate.transform.for_loop` owns every timestep; no Python timestep loop or dynamic history list | T | High | Low | Retain | High |
| `alpha_rhythm.py:build_mapped_rollout` | transformed already | `brainstate.transform.vmap(run_lane)` maps the complete model construction, initialization, State evolution, and outputs across all independent lanes | E | High | Medium | Retain; model State is local to each mapped lane and discarded after returned trajectories | High |
| `alpha_rhythm.py:build_mapped_rollout` | whole-rollout JIT | Optional `brainstate.transform.jit(mapped)` is the largest stable State-aware boundary | T×E | High | Medium | Use one stable jitted callable for production and reuse it after the first call | High |
| `alpha_rhythm.py:spectral_metrics` | host analysis | NumPy conversions occur only after explicit `to_decimal(mV)` and after transformed simulation completes | host | Low | Low | Retain; this is analysis/serialization, not the simulation hot path | High |
| `alpha_rhythm.py:assess_results` | small host loop | Three weakened conditions are reduced after simulation | host | Negligible | Low | Retain for readable deterministic assessment | High |
| `run_experiment.py` | immutable I/O/logging | Printing, JSON, NPZ, and source hashing occur outside compiled execution | host | Low | Low | Retain | High |

## Patch / rewrite plan

The implementation already follows the required time and ensemble transforms, so the only accepted acceleration is the optional whole-rollout `brainstate.transform.jit` already exposed by `build_mapped_rollout`. The production runner constructs that callable once, measures the first compilation-plus-execution call separately, and reuses it for the recorded execution. No multi-device path is warranted for a 32-lane, six-State local mass model, and no checkpointed loop is warranted because this forward-only experiment has no reverse-mode graph.

Exact transform behavior follows the package BrainState root skill, its `transformation-jit-expansion.md` and `transformation-vmap-expansion.md`, and the BrainMass `batch-transform-acceleration.md` reference. The acceleration skill's own advertised local reference directory was absent in the installed skill tree; the corresponding package-owned BrainState references were present and used.

## Validation plan and evidence

- Representative benchmark: 100 ms at the production 0.1 ms step, all four inhibition levels, all eight initial conditions, and all three mV trajectories. This exercises shape `[1000, 4, 8]` without running or analyzing the locked six-second production outcome.
- Unaccelerated call: 0.5726821690 s.
- Jitted first call: 0.1179156820 s, including compilation.
- Jitted warm call: 0.0022664530 s; observed warm speedup 252.68× for this short benchmark. This is environment-specific performance evidence, not a scientific claim.
- Units and dtype were unchanged: every trajectory remained mV and float64.
- Output and final-recorded-State parity tolerance: absolute difference no larger than `1e-6 mV`, zero relative tolerance. Maximum observed differences were `8.90e-8 mV` for EEG, `6.97e-8 mV` for excitatory PSP, and `5.90e-8 mV` for inhibitory PSP. The arrays were not bitwise equal but passed the declared numerical tolerance.
- Both paths retained shape `[1000, 4, 8]`; repeated compatible calls reused the same callable shape. `eeg() = E - I` error was exactly 0 mV and all outputs were finite/bounded.
- A focused `test_whole_rollout_jit_parity` check now covers unit, shape, and `1e-6 mV` trajectory parity on a smaller grid.
- RNG and gradient gates are not applicable: the locked experiment is deterministic and forward-only.

## Remaining risks

- Full trajectories are intentionally retained because time traces and per-lane spectra are required evidence. The production lower bound for three float64 trajectories is modest (about 46 MB at 60,000×4×8), though compiler intermediates add overhead.
- The large warm speedup is measured on a short CPU workload and includes unjitted transform dispatch; it should not be extrapolated to another device or duration. The production runner records its own cold and warm times.
- Each runner closure specializes `dt`, duration, and therefore step count. The production and half-step controls deliberately use separate stable callables.
