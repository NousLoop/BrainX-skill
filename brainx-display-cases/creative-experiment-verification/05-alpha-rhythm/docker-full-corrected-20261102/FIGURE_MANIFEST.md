# Figure manifest

## `/workspace/figures/iteration-1-diagnostic.png`
- Work type, evidence mode, scientific role, and question: create; `diagnostic`; unaccepted iteration-1 evidence; asks what pattern the invalid run produced and which numerical-validity comparison failed.
- Source run IDs, artifacts, hashes, and acceptance status: `alpha-production-20261102-i1`; `/workspace/runs/alpha-production-20261102-i1/results.npz` (`e7345685422e5343aae773286b81d9e7ab306b9157262698bfff36a690a0e171`), `metrics.json` (`910abc38569ca23c68facac023bf944c3e99ee4174ea4a3ae938881e68887459`), and `convergence.json` (`14000acb11129a7d1668a1308e7c2422c1c5f1b5d2f7f4c9bd081da2b2caf086`); run status `done`, scientific status `invalid`, review pending.
- Variables, axes, ordering, and units: cortical Jansen-Rit EEG proxy in mV over seconds; Welch PSD in mV²/Hz over Hz; retained RMS in mV by ordered inhibitory-gain fraction and initial condition; half-step RMS relative difference in percent by tested gain fraction. Numeric arrays use time × condition × initial-condition ordering.
- Transformations, smoothing, aggregation, and exclusions: panel A shows the final 4–6 s for the prespecified first initial state and subtracts each displayed trace's own window mean; panel B shows the locked Welch PSD for the same state and all conditions, without smoothing; panel C shows all eight raw paired RMS paths plus their median on a log scale and the locked 0.01 mV peak-validity floor; panel D shows the two prespecified half-step relative RMS discrepancies and locked 5% limit. No lane is excluded and no interpolation is used.
- Sample size and uncertainty: eight deterministic initial conditions per production condition; raw paired lines and median shown. These are nuisance initial states, not stochastic samples or a confidence interval. Half-step checks use the first initial condition only, as prespecified.
- Controls and fixed comparison settings: all four requested inhibition levels; shared 220 Hz drive and model defaults; common axes within each panel; 8–13 Hz band shaded; fixed panel-A limits of ±3.5 mV; 4–30 Hz spectral window; diagnostic status displayed in the title.
- Plotting source, output path, size, format, and resolution: `/workspace/plot_diagnostic.py` (`c75b9ed3ca03728100e58aa3c762bd03d6ee757e467ad2cf49602820abecb75a`); `/workspace/figures/iteration-1-diagnostic.png` (`df14aa687053935e942353768f0273009ff4ecb0731a2b0e9c657a1eab0fc5c8`); 10.5 × 7.0 inches, PNG, 220 dpi.
- Render and source-value checks: inspected at original and resized resolution; all panels are nonblank, unclipped, legible, and labeled. Panel A shows the 11 Hz baseline trace and near-zero weakened traces; panel B preserves the orders-of-magnitude PSD differences; panel C matches the saved RMS medians (1.2453 mV, 6.29e-6 mV, 4.50e-9 mV, 4.26e-9 mV); panel D matches convergence discrepancies (8.37% and 99.31%) and visibly exceeds the 5% limit. This figure is unaccepted diagnostic evidence, not a final result figure.


## figures/iteration-3-diagnostic.png (and PDF)
- Work type: adapt; evidence mode: diagnostic, independent acceptance pending.
- Question: how does fixed inhibitory-gain reduction change the cortical EEG proxy and do all lanes pass numerical checks?
- Source: runs/alpha-production-20261102-i3-dt005/results.npz and convergence.json; hashes in its artifact_manifest.json.
- Axes: raw time/condition/initial-state; mV, seconds, Hz; 4 gain conditions x 8 paired deterministic ICs.
- Transformations: 2 s transient, physically aligned 1 ms analysis, demean full retained window; first IC and final 2 s displayed as originally specified.
- PSD: saved BrainTools Welch; no recomputation or smoothing; below-floor frequency is undefined.
- RMS panel: all 8 raw values and black median per condition; small fixed horizontal jitter separates IC markers. No confidence interval.
- Convergence panel: all 32 errors divided by max(0.05*reference RMS,1e-6 mV), boundary 1; full raw fields preserved.
- Sources and plotting: plot_refined.py; one 11 x 7.5 inch subplots composition; PNG 300 dpi and vector PDF.
- Render audit: inspected PNG; nonblank, unclipped, readable axes, no overlaps, explicit diagnostic/unaccepted title. Source values independently verified by verify_saved_evidence.py.
