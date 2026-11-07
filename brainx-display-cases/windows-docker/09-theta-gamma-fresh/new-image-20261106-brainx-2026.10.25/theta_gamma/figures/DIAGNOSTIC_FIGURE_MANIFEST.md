# Figure manifest

- Evidence mode: diagnostic; work type: create. Run: production-02.
- Figures: illustrative model results, not experimental EEG.
- Statistical unit: three deterministic initial-State/paired observation-seed lanes; figures show prespecified lane 0 (seed 11), no population uncertainty inferred.
- Display cases fixed before production. After the first diagnostic render exposed clipping at R=0.5, R/ΔR color limits were expanded to their full theoretical ranges [0,1]/[−1,1], before review. First renders retained in figures/first-render. No interpolation between sweep samples.
- PNG 220 dpi and PDF vector exports. Plotting source: plot_results.py. Source-value bundle: figures/diagnostic_plotted_values.npz.
- Source SHA256: trajectories 593051cfcf79b435cada88c7d03b207ec4a77a8fca0e804ef3be551f1f15e38e
- Source SHA256: analysis 575ba7b07fad8f195e1094c4df39a422350746e472850423a464e9d02cb4089e
- Acceptance: unaccepted, diagnostic only
- Render inspection: pending; to be appended after image inspection.

## diagnostic_traces
- Question / scientific role: Aligned E/I, executed drive, synthetic EEG and gamma envelope at 3–3.8 s. 1 ms point sampling. Proxy E−0.5I is post-burn mean-centered, plus supplied theta and paired noise. Theta guide is scaled for visibility, not data.
- Axes and units: labeled in plot; E/I/input dimensionless, proxy a.u., phase rad, time s, frequency Hz.
- Reductions: lane 0 only; no smoothing beyond stated bandpass/envelope and Welch analysis, no failed samples excluded.
- Fixed controls: m=0 at identical gain and initial State; paired observation noise.
- Outputs: figures/diagnostic_traces.png, figures/diagnostic_traces.pdf

## diagnostic_phase_and_spectra
- Question / scientific role: 3–13 s, 60 theta cycles. 18 phase-bin mean gamma envelopes, normalized by each profile mean only in the labeled panel. Welch PSD 2 s windows/1 s overlap; no condition-specific PSD normalization.
- Axes and units: labeled in plot; E/I/input dimensionless, proxy a.u., phase rad, time s, frequency Hz.
- Reductions: lane 0 only; no smoothing beyond stated bandpass/envelope and Welch analysis, no failed samples excluded.
- Fixed controls: m=0 at identical gain and initial State; paired observation noise.
- Outputs: figures/diagnostic_phase_and_spectra.png, figures/diagnostic_phase_and_spectra.pdf

## diagnostic_parameter_sweep
- Question / scientific role: Exact 7×7 sampled grid for lane 0, gain columns and nonuniform depth rows. X marks a matched unmodulated baseline lacking gamma. Values are retained even in marked cells; categorical panel uses full fixed predicate and does not force any category.
- Axes and units: labeled in plot; E/I/input dimensionless, proxy a.u., phase rad, time s, frequency Hz.
- Reductions: lane 0 only; no smoothing beyond stated bandpass/envelope and Welch analysis, no failed samples excluded.
- Fixed controls: m=0 at identical gain and initial State; paired observation noise.
- Outputs: figures/diagnostic_parameter_sweep.png, figures/diagnostic_parameter_sweep.pdf

## Diagnostic verification completed
- Rendered PNGs visually inspected: traces, phase/spectra, and corrected sweep map are nonblank, legible, and unclipped; the first saturated color maps remain in first-render/.
- Source checks: display indices [3,31], R=(0.001998,0.076167), gamma peaks=(29.5,27.5) Hz, exact 7×7 axis order, 18 bins, 60 cycles, 1 ms recorded spacing; saved plotted matrices agree with source metrics.
- Current R color range [0,1] includes maximum ≈0.620; ΔR [−1,1] includes all samples. Low/high-gain baseline red-X masks agree with decision.npz.
- These figures are diagnostic and unaccepted until review PASS.
