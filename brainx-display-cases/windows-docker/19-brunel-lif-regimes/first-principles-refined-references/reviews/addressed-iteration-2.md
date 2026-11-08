# Addressed findings, iteration 2

Prior verdict is preserved verbatim in iteration-1.md. Scientific choices and production evidence are unchanged.

- BX-001: replaced the SciPy spectral bypass in analysis.py with documented braintools.analysis.spectral.spectrogram and u.math.mean(axis=1). Fixed Hann/window/overlap/detrending settings and full-window boxcar estimator are unchanged. Physical Hz input, 0.1-ms interval and Hz²/Hz PSD remain quantities until serialization. Scoped float64 analysis preserves original precision. All 16 raw-based reanalyses match original frequency axes, PSDs, metrics, predicates and decisions; see runs/iteration-2/spectral_parity.json. Original baseline-v1/code/analysis.py and outputs remain intact.
- BX-002: new runnable check_metric_fixture.py retains packed periodic spikes and configuration in checks/metrics_fixture_v2/input/periodic_spikes.npz, with outputs under output/. Hash before/after is identical. Assertions verify expected rate, CV, synchrony, spectral peak and supported SR. analysis.summarize rejects resolved input/output path collisions before writing. Original overwritten fixture and prior review are preserved as failure evidence.

No production rerun: reviewer 1 explicitly permits this when corrected analysis preserves evidence. All 16 raw files and all three graphs are referenced from a separate immutable analysis-only snapshot with parent hashes. No external scientific source or example was consulted. Independent review 2 must retain the same source restriction.
