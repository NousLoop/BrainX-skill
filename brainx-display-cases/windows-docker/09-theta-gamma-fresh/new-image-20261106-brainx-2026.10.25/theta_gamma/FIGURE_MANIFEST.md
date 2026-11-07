# Figure manifest

- Evidence mode: final; work type: create. Run: production-02.
- Figures: illustrative model results, not experimental EEG.
- Statistical unit: three deterministic initial-State/paired observation-seed lanes; figures show prespecified lane 0 (seed 11), no population uncertainty inferred.
- Display cases fixed before production. After the first diagnostic render exposed clipping at R=0.5, R/ΔR color limits were expanded to their full theoretical ranges [0,1]/[−1,1], before review. First renders retained in figures/first-render. No interpolation between sweep samples.
- PNG 220 dpi and PDF vector exports. Plotting source: plot_results.py. Source-value bundle: figures/final_plotted_values.npz.
- Source SHA256: trajectories 593051cfcf79b435cada88c7d03b207ec4a77a8fca0e804ef3be551f1f15e38e
- Source SHA256: analysis 575ba7b07fad8f195e1094c4df39a422350746e472850423a464e9d02cb4089e
- Acceptance: PASS scope in reviews/gate.json
- Render inspection: completed; see final export inspection and evidence/final-figure-checks.json.

## final_traces
- Question / scientific role: Aligned E/I, executed drive, synthetic EEG and gamma envelope at 3–3.8 s. 1 ms point sampling. Proxy E−0.5I is post-burn mean-centered, plus supplied theta and paired noise. Theta guide is scaled for visibility, not data.
- Axes and units: labeled in plot; E/I/input dimensionless, proxy a.u., phase rad, time s, frequency Hz.
- Reductions: lane 0 only; no smoothing beyond stated bandpass/envelope and Welch analysis, no failed samples excluded.
- Fixed controls: m=0 at identical gain and initial State; paired observation noise.
- Outputs: figures/final_traces.png, figures/final_traces.pdf

## final_phase_and_spectra
- Question / scientific role: 3–13 s, 60 theta cycles. 18 phase-bin mean gamma envelopes, normalized by each profile mean only in the labeled panel. Welch PSD 2 s windows/1 s overlap; no condition-specific PSD normalization.
- Axes and units: labeled in plot; E/I/input dimensionless, proxy a.u., phase rad, time s, frequency Hz.
- Reductions: lane 0 only; no smoothing beyond stated bandpass/envelope and Welch analysis, no failed samples excluded.
- Fixed controls: m=0 at identical gain and initial State; paired observation noise.
- Outputs: figures/final_phase_and_spectra.png, figures/final_phase_and_spectra.pdf

## final_parameter_sweep
- Question / scientific role: Exact 7×7 sampled grid for lane 0, gain columns and nonuniform depth rows. X marks a matched unmodulated baseline lacking gamma. Values are retained even in marked cells; categorical panel uses full fixed predicate and does not force any category.
- Axes and units: labeled in plot; E/I/input dimensionless, proxy a.u., phase rad, time s, frequency Hz.
- Reductions: lane 0 only; no smoothing beyond stated bandpass/envelope and Welch analysis, no failed samples excluded.
- Fixed controls: m=0 at identical gain and initial State; paired observation noise.
- Outputs: figures/final_parameter_sweep.png, figures/final_parameter_sweep.pdf

## Final export inspection and provenance
- All three final PNGs visually rendered and inspected after PASS: nonblank, readable, no clipping or overlaps affecting interpretation; consistent pair scales, units, 18 phase bins and sampled grid order.
- Exact displayed numeric arrays equal the diagnostic bundle field-by-field: evidence/final-figure-checks.json. R=(0.001998,0.076167) at the displayed pair; red-X masks and continuous maps match the saved decisions.
- PDF files are vector exports of the same inspected Matplotlib figures; PDF signatures, pages, MediaBox and EOF verified. No separate PDF rasterizer is installed; direct independent PDF raster inspection was unavailable. The visually inspected PNGs are the report's display artifacts.
- Plot source SHA256: 0d793d2e0e5b4726cab51b769b87d4c573c9bd702d73c768f4c839ca97e5839a
- Original diagnostic metadata retained: figures/DIAGNOSTIC_FIGURE_MANIFEST.md. First saturated renders retained in figures/first-render/.
- Acceptance: reviews/iteration-1.md PASS; thread 01a1ae86-d767-74a2-9de3-9206de1fc7d0; accepted production-02; no science or data changes after review.
