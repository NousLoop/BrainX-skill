# BrainX acceleration audit — iteration 2

The iteration-1 audit at `/workspace/brainx-acceleration-audit.md` remains authoritative because no implementation or workload changed. Iteration 2 repeated its representative 100 ms, 4×8, float64 CPU comparison after the access-only refusal.

| File/area | Pattern | Evidence | Axis | Impact | Risk | Decision | Confidence |
|---|---|---|---|---|---|---|---|
| `alpha_rhythm.py:run_lane` | transformed | one State-aware `for_loop` owns 1,000 benchmark timesteps | T | high | low | retain | high |
| `alpha_rhythm.py:build_mapped_rollout` | transformed + whole-rollout JIT | one stateful `vmap` owns 32 independent lanes; one stable BrainState JIT owns the mapped rollout | E×T | high | medium | retain | high |
| analysis/serialization | host boundary | NumPy occurs after explicit unit extraction and completed simulation | host | low | low | retain | high |

The repeat produced the same maximum numerical differences as iteration 1: `8.90e-8 mV` EEG, `6.97e-8 mV` excitatory PSP, and `5.90e-8 mV` inhibitory PSP, all below the fixed `1e-6 mV` tolerance. Shape `[1000, 4, 8]`, float64 dtype, finite/bounded values, and exact `EEG = E - I` identity were preserved. First-call time was 0.1193 s, warm time 0.002265 s, and unaccelerated time 0.6376 s. No optimization or source change is justified.

