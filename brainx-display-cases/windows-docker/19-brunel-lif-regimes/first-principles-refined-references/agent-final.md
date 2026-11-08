Completed **16 full-size runs** with all supplied parameters preserved: seeds 101/202/303, 4 s per run, 1 s burn-in, plus four finer-grid controls. Independent Codex review: **PASS**.

| (g, eta) | Requested regime | Frozen-test result | Dominant peak |
|---|---|---|---|
| (3, 2) | Synchronous regular | Supported | 333 Hz |
| (6, 4) | Fast synchronous irregular | Supported | 182–185 Hz |
| (5, 2) | Asynchronous irregular | Unsupported | 135–139 Hz |
| (4.5, 0.9) | Slow synchronous irregular | Inconclusive | 17–23 Hz |

At `(5,2)`, synchrony and CV measurements contradict AI. Slow SI remains inconclusive because CV eligibility is low and the oscillation test changes on the finer grid.

Saved PNGs:

- [Four-condition rate/raster figure](/workspace/figures/final/four_conditions.png)
- [E/I rates](/workspace/figures/final/ei_rates.png)
- [ISI CV](/workspace/figures/final/isi_cv.png)
- [Global-rate spectra](/workspace/figures/final/global_rate_spectra.png)
- [Regime tests](/workspace/figures/final/regime_tests.png)

[Full report](/workspace/report.md) · [Model code](/workspace/model.py) · [Raw evidence index](/workspace/RAW_EVIDENCE.md) · [Verbatim independent review](/workspace/reviews/iteration-2.md)

No papers, scientific example implementations, or remembered protocols were used.