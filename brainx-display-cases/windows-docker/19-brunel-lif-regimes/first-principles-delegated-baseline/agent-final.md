Completed 16 simulations: seeds **11, 29, 47** across all four conditions, plus four timestep checks. Each run used 1 s burn-in and 3 s observation. Independent Codex review **[PASSED](/workspace/Brunel-lif-regimes/reviews/iteration-2.md)**.

| (g, η) | Requested regime verdict | Dominant global frequency |
|---|---|---:|
| (3, 2) | Synchronous regular: supported | 667 Hz |
| (6, 4) | Fast synchronous irregular: inconclusive | 181–183 Hz |
| (5, 2) | Asynchronous irregular: unsupported; classified synchronous regular | 137–142 Hz |
| (4.5, 0.9) | Slow synchronous irregular: inconclusive | 22–23 Hz |

These verdicts follow the locked tests. The fast case’s irregularity is timestep sensitive; thresholds were not retuned.

Saved and visually inspected PNGs:

- [Four conditions: 0.1 ms rates above fixed 50-neuron rasters](/workspace/Brunel-lif-regimes/figures/four_conditions.png)
- [E/I rates](/workspace/Brunel-lif-regimes/figures/ei_rates.png)
- [ISI CV distributions](/workspace/Brunel-lif-regimes/figures/isi_cv.png)
- [Global-rate spectra](/workspace/Brunel-lif-regimes/figures/global_rate_spectrum.png)
- [Timestep sensitivity](/workspace/Brunel-lif-regimes/figures/step_halving.png)

[Final report](/workspace/Brunel-lif-regimes/report.md), [locked specification](/workspace/Brunel-lif-regimes/NeuroSpecification.md), [model code](/workspace/Brunel-lif-regimes/model.py), and [raw evidence](/workspace/Brunel-lif-regimes/runs/locked-baseline-v2/raw) are preserved.