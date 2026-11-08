# Figure manifest

Evidence mode: final. Work type: create. Independent review: PASS ([verbatim verdict](reviews/iteration-2.md)). Scientific outcome: partially_supported.
All five PNGs were rendered from the accepted saved evidence and visually inspected on 2026-11-08. No new scientific simulation, threshold, displayed case or data selection was introduced.

## Shared provenance
- Source simulation run: `runs/locked-baseline-v2`, 16/16 complete, exit 0. Three primary graph seeds [11,29,47]; four additional seed-11 timestep checks.
- Spectral source: `analysis-iteration-2/braintools-final/metrics/*.npz`; exact peak/label parity and numerical PSD parity recorded in parity.json.
- Raw spikes, counts, per-neuron statistics, graph and environment identities remain in the immutable simulation run. The partial parent run is excluded from all final figures and preserved separately.
- Conditions, in supplied order: (g,eta)=(3,2),(6,4),(5,2),(4.5,0.9). Each rollout is 4 s; remove 1 s burn-in and analyze 3 s. No fitted normalization or confidence intervals.
- Source hashes:
  - `NeuroSpecification.md`: `20c7419c9ddce8492febff55ce50920bae77d710fdbcce440cca17d4d58f7271`
  - `plot_results.py`: `49d060a1a9dc70984bf2ed2c5706d52d3d7b0cb6201a692d7eb5d86026056dab`
  - `runs/locked-baseline-v2/config.json`: `86a31966b28bbe9175876eb23359df57fafb7b79a05c1e522efe880e0290447c`
  - `runs/locked-baseline-v2/artifact_manifest.json`: `82740a252189de0515389f392d57d282145558cf3ab00256e67adf6aa3cb31bc`
  - `runs/locked-baseline-v2/metrics.json`: `85ae2b6ee2aec8947f9b44282b5eee9e7fe5a918d333156d02d8035700c70277`
  - `runs/locked-baseline-v2/sample_neurons.npy`: `2e2f0207ff04c8f7a46e9611bc2ec24b5b013d89d260f491412652ce4c8a5fb8`
  - `analysis-iteration-2/braintools-final/manifest.json`: `67a2190b36f4af093b19d9de49f04f3466812b052a5f02bdbb449e68a84d50c2`
  - `analysis-iteration-2/braintools-final/parity.json`: `791083931cb140059b8ab5b4ee6d68228b3e098d9084c927f68002fbd1c475ce`
  - `reviews/iteration-2.md`: `f6678f55b80063d36c7df047468a527ee4a783a0f1b260a39e55f26ab4437076`
  - `figures/source_checks.json`: `d040b735b5a559eb0727abd61a57d9785db07b024fc65a9ea3e179ee5f397c97`
  - `figures/finalization_checks.json`: `0210a82abb547d6dc3d90d467cf820a47fcfab80b55d26cb24252304b870134d`

## figures/four_conditions.png
- Output: `/workspace/Brunel-lif-regimes/figures/four_conditions.png`; PNG, 220 dpi; SHA256 `0b2fe5ec0597fe5d434af1121c7152af08ff3436b61535d51496c75c56e8ccf7`.
- Scientific role/question: compare instantaneous global activity and individual spike timing across the four supplied conditions.
- Sources: seed-11 primary metrics NPZs and raw spike NPZs, conditions 0–3; fixed sample_neurons.npy. Raw spikes are losslessly packed time × neuron bits, E first.
- Variables/axes: global count/(12500 × 0.0001 s), Hz/neuron, versus endpoint time in ms; raster rows are the same 50 sampled identities sorted by original neuron ID, labeled 0–49. Count arrays have shape (30000,2), time × [E,I].
- Transformations: display first 5000 post-burn-in bins, 1000–1500 ms; no rate smoothing. Dashed mean is the full 3 s mean, not the display-window mean. No spike exclusions within the selected neurons/window.
- Sample size/controls: fixed random 50 of 12500 neurons, seed 20261108; display graph seed 11 for every condition. Same time limits and population normalization; rate y scales vary and are labeled.
- Size: 14 × 10 inches, 3080 × 2200 pixels.
- Render/source checks: all four rates plotted exactly from bin values; raster event counts 8329,1440,924,136 match raw sample evidence. All four dashed means match saved full-window rates. Visual inspection confirms aligned rate/raster windows and readable axes.
- Plotting source: plot_results.py; render command recorded in README.md and plot-final.log. Verification details: figures/finalization_checks.json.

## figures/ei_rates.png
- Output: `/workspace/Brunel-lif-regimes/figures/ei_rates.png`; PNG, 220 dpi; SHA256 `263d70e79a379d62fe275fc95cd7670bca8bba878b6eb10186d024cb6b723a27`.
- Scientific role/question: compare E and I mean firing rates and the spread across independent graph seeds.
- Sources: metrics.json primary rows; counts_EI arrays in the twelve primary metrics NPZs.
- Variables/axes: condition categories on x, E or I rate in Hz/neuron on y; separate E and I panels. Counts are normalized by 10000 or 2500 neurons and 3 s.
- Transformations: complete-observation mean, no smoothing. Lines join paired seeds descriptively across categories; they are not a sampled phase boundary.
- Sample size/controls: three independent network realizations per condition, same three paired seeds and condition order. Each seed has a distinct marker; no confidence intervals.
- Size: 11 × 4.2 inches, 2420 × 924 pixels.
- Render/source checks: all E/I means independently agree with stored counts. Visual inspection confirms almost overlapping seed means, labeled populations/units, and no clipping.
- Plotting source: plot_results.py; render command recorded in README.md and plot-final.log. Verification details: figures/finalization_checks.json.

## figures/isi_cv.png
- Output: `/workspace/Brunel-lif-regimes/figures/isi_cv.png`; PNG, 220 dpi; SHA256 `79e99e367a3f74f2f743ff0a908506eb89cf0e10f1e36ce1c13beafb924406d1`.
- Scientific role/question: show within-neuron firing irregularity and its relation to the frozen regular/irregular thresholds.
- Sources: ISI_CV and ISI_count arrays (12500 neuron entries, E first) in the twelve primary metrics NPZs.
- Variables/axes: per-neuron ISI CV (dimensionless) versus empirical cumulative fraction of eligible neurons, separately for E and I in each condition.
- Transformations/exclusions: sort each population CV distribution; retain neurons with at least ten complete observation-window ISIs. CV uses population SD/mean. No pooling of seeds, smoothing or confidence intervals.
- Sample size/controls: three graph seeds; eligible-neuron counts retained per run in metrics.json. Seed 11 bold, others faint; E solid and I dashed. Frozen CV=0.5 and 0.8 lines; shared 0–1 cumulative scale; x limits vary with displayed values.
- Size: 15 × 3.8 inches, 3300 × 836 pixels.
- Render/source checks: finite CV eligibility exactly matches ISI_count≥10; pooled medians match all summary rows. Visual inspection confirms near-zero first-condition CV, the fast borderline distribution, and the slow intermediate distribution.
- Plotting source: plot_results.py; render command recorded in README.md and plot-final.log. Verification details: figures/finalization_checks.json.

## figures/global_rate_spectrum.png
- Output: `/workspace/Brunel-lif-regimes/figures/global_rate_spectrum.png`; PNG, 220 dpi; SHA256 `3495244515b9d950ceb90867cb59822ce0733a1bb77cb2715aab35d8f891cf8d`.
- Scientific role/question: identify the dominant global-rate frequency without equating a spectral peak with a complete regime verdict.
- Sources: native BrainTools frequency_Hz and PSD_Hz2_per_Hz arrays (5001 bins each) in the twelve primary native spectral NPZs.
- Variables/axes: frequency (Hz) versus global-rate PSD ((Hz/neuron)^2/Hz); logarithmic PSD axis, linear frequency 0–1000 Hz, displayed bins 1–1000 Hz.
- Transformations: global rate in 0.1 ms bins, full 3 s observation, Welch with 1 s periodic Hann segments, 50% overlap, constant per-segment detrending, segment mean. No additional smoothing or fitted normalization.
- Sample size/controls: three network seeds per condition, each shown; fixed analysis and frequency limits, per-panel PSD scales. Legend lists strongest bin in the frozen 1–1000 Hz search band; no uncertainty interval.
- Size: 11 × 7 inches, 2420 × 1540 pixels.
- Render/source checks: all sixteen native spectral peaks equal saved summaries; all PSDs pass archived-estimator parity. Visual inspection confirms peaks at 667, 181–183, 137–142 and 22–23 Hz, correct legends and physical units.
- Plotting source: plot_results.py; render command recorded in README.md and plot-final.log. Verification details: figures/finalization_checks.json.

## figures/step_halving.png
- Output: `/workspace/Brunel-lif-regimes/figures/step_halving.png`; PNG, 220 dpi; SHA256 `4e05daca7c8e26d18bf7ba3e4fa71aed68921beacd7debc323bcb998ff53dc4e`.
- Scientific role/question: compare rate scales and temporal variability after halving the integration timestep.
- Sources: seed-11 counts_EI for all four conditions at dt=0.1 and 0.05 ms; shapes (30000,2) and (60000,2).
- Variables/axes: physical time 1000–4000 ms versus 10 ms mean global rate (Hz/neuron). Bin centers are shown.
- Transformations: sum exactly 100 or 200 native steps into each 10 ms rate bin. This explicit diagnostic aggregation does not replace the main 0.1 ms rates or classification metrics.
- Sample size/controls: one paired graph/initialization per condition, two timesteps. Poisson draw sequences differ with timestep; compare statistics, not pointwise trajectories. Same time limits; per-condition rate scales, zero lower bound; no confidence intervals.
- Size: 11 × 7 inches, 2420 × 1540 pixels.
- Render/source checks: all underlying mean rates agree with source counts. Visual inspection confirms full observation windows and labeled timestep curves; the report also preserves the fast-case CV sensitivity not visible from rate scales alone.
- Plotting source: plot_results.py; render command recorded in README.md and plot-final.log. Verification details: figures/finalization_checks.json.
