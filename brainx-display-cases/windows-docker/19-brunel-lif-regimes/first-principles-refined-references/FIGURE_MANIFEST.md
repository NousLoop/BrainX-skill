# Figure manifest

Evidence mode: final. Run: `/workspace/runs/iteration-2`. Independent review PASS; final figures use the accepted scope.

Exact run/config/source hashes: `runs/iteration-2/manifest.json`, `runs/iteration-2/environment.json`. Figure contract: `FIGURE_CONTRACT.md`. Plot source: `plot_results.py` (SHA256 816b398e60e63971a7f9a99328cc9409602c152ff4a11a0169fc4a9dc8d96409).

Exact plotted arrays: `figures/final/figure_data.npz`. Complete population spike evidence and statistics remain in raw/metrics.

## /workspace/figures/diagnostic/ei_rates.png
- Question: E/I rates | all three seeds and numerical control | analysis 1000–4000 ms
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/baseline-v1`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 111592 bytes; SHA256 `1d5661428a8f37f7b6525f9a3478882b25843b452d83699c643367134165dcd0`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/diagnostic/four_conditions.png
- Question: Global rate (0.1-ms bins; independent rate scales) and fixed 50-neuron raster | seed 101
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/baseline-v1`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 358928 bytes; SHA256 `c1d3cc9f2ee11d10d356611dcb7dc5110b16263e7099eb1daf5a3c25283b6b6d`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/diagnostic/global_rate_spectra.png
- Question: Global-rate spectra | Welch 1-s Hann windows, 50% overlap | maxima need not imply oscillations
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/baseline-v1`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 534558 bytes; SHA256 `97c1e3d909f7f7fefc46acfa39ea6e385830aec387b22ee215e42b985322d360`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/diagnostic/isi_cv.png
- Question: ISI CV | all eligible neurons across three seeds | dotted 0.50 / dashed 0.70 cutoffs
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/baseline-v1`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 107267 bytes; SHA256 `06c6f9fa6f5e42e2070b37e8a7d68a86ba5f677869e932a1964939f17e1b34cc`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/diagnostic/regime_tests.png
- Question: Frozen regime predicates | dots: full windows; synchrony crosses: halves | dashed: fixed thresholds
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/baseline-v1`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 579067 bytes; SHA256 `8fa71aa51001cfc17b873fdfecbafb78beb4c08037aba9b352769aeea7d17340`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/diagnostic-baseline/four_conditions.png
- Question: Global rate (0.1-ms bins; independent rate scales) and fixed 50-neuron raster | seed 101
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/baseline-v1`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 356200 bytes; SHA256 `f10e84e9dce79bd0d9f2e30e9626ea1f3349e94ddabaabd35fa442bac1a4869c`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/final/ei_rates.png
- Question: E/I rates | all three seeds and numerical control | analysis 1000–4000 ms
- Evidence mode: final; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 103526 bytes; SHA256 `3c2716db46623db3d600ea8a2fec06ed8acabcaca425c5a267023e5c47acffc6`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/final/four_conditions.png
- Question: Global rate (0.1-ms bins; independent rate scales) and fixed 50-neuron raster | seed 101
- Evidence mode: final; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 353169 bytes; SHA256 `684d041ef19e4bad8a0b8587aab2a8e0a71be37bdec46630817a25dafd3ebcd9`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/final/global_rate_spectra.png
- Question: Global-rate spectra | Welch 1-s Hann windows, 50% overlap | maxima need not imply oscillations
- Evidence mode: final; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 527672 bytes; SHA256 `6495c5e0a7001d55d0e7dc1bbfba1a93ff6a67a99287511c841e7955d92bc431`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/final/isi_cv.png
- Question: ISI CV | all eligible neurons across three seeds | dotted 0.50 / dashed 0.70 cutoffs
- Evidence mode: final; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 101344 bytes; SHA256 `ec913a9650d166ee24fd4db789b8f512af30dbff263eb27f2b2d4325b320c477`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/final/regime_tests.png
- Question: Frozen regime predicates | dots: full windows; synchrony crosses: halves | dashed: fixed thresholds
- Evidence mode: final; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 569570 bytes; SHA256 `49626bc665f4b42394fe525900421d415ab1a171df4bb958f366c26f32d19b62`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/iteration-2-diagnostic/ei_rates.png
- Question: E/I rates | all three seeds and numerical control | analysis 1000–4000 ms
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 111592 bytes; SHA256 `1d5661428a8f37f7b6525f9a3478882b25843b452d83699c643367134165dcd0`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/iteration-2-diagnostic/four_conditions.png
- Question: Global rate (0.1-ms bins; independent rate scales) and fixed 50-neuron raster | seed 101
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 358928 bytes; SHA256 `c1d3cc9f2ee11d10d356611dcb7dc5110b16263e7099eb1daf5a3c25283b6b6d`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/iteration-2-diagnostic/global_rate_spectra.png
- Question: Global-rate spectra | Welch 1-s Hann windows, 50% overlap | maxima need not imply oscillations
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 534558 bytes; SHA256 `97c1e3d909f7f7fefc46acfa39ea6e385830aec387b22ee215e42b985322d360`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/iteration-2-diagnostic/isi_cv.png
- Question: ISI CV | all eligible neurons across three seeds | dotted 0.50 / dashed 0.70 cutoffs
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 107267 bytes; SHA256 `06c6f9fa6f5e42e2070b37e8a7d68a86ba5f677869e932a1964939f17e1b34cc`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.

## /workspace/figures/iteration-2-diagnostic/regime_tests.png
- Question: Frozen regime predicates | dots: full windows; synchrony crosses: halves | dashed: fixed thresholds
- Evidence mode: diagnostic; earlier diagnostic exports are preserved and remain labeled unaccepted.
- Source: `/workspace/runs/iteration-2`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.
- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.
- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.
- Export: PNG, 200 dpi; 579067 bytes; SHA256 `8fa71aa51001cfc17b873fdfecbafb78beb4c08037aba9b352769aeea7d17340`.
- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.
