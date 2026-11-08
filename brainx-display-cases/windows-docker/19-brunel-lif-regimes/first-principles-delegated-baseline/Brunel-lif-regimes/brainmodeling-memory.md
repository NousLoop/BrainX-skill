# Brain modeling memory

## Checkpoint
- Iteration: 1
- Step: 0
- Resume at: 1/1

### Artifacts
- `NeuroSpecification.md`: locked initial protocol, before simulation.
- `report.md`: draft; scientific outcome and review pending.

### Important milestones
- Fresh-new project, no preexisting model/data.
- All unspecified decisions explicitly delegated in the user request; clarification gate complete using existing authorization.
- Literature gate skipped: model fixed by user; scientific reference searches and example implementations expressly forbidden.
- Seeds, durations, metrics, thresholds, display windows and dt sensitivity locked before any simulation.

## Checkpoint
- Iteration: 1
- Step: 1
- Resume at: 1/2

### Artifacts
- `brainx-study-record.md`: completed mechanics study and implementation decisions.
- `api-docs/`: saved public API contract excerpts only.

### Important milestones
- All four requested package layers are available in the existing CPU environment.
- Scientific example scripts explicitly skipped under the user's overriding restriction.
- No literature, scientific source, or remembered model protocol used. Forward simulation only.

## Checkpoint
- Iteration: 1
- Step: 2
- Resume at: 1/3

### Artifacts
- `model.py`, `experiment.py`, `checks.py`, `smoke.py`, `freeze_run.py`, `plot_results.py`: first-principles implementation.
- `checks.json`, `checks-attempt-8.log`: passing component checks, exact compiled spike/State/RNG parity and exact replay.
- `checks.log`, `checks-attempt-2.log` through `checks-attempt-7.log`: preserved implementation failures, not production evidence.
- `smoke/result.json`, `smoke/raw.npz`, `smoke/run.log`: passing full-scale CPU smoke.

### Important milestones
- Native BrainEvent CSR and BrainPy DeltaProj preserve source sign and exact arrival timing.
- Corrected dimensionless Quantity unwrapping and typed JAX RNG-key serialization using public APIs.
- Reset values in place from registered State snapshot: recreating State objects invalidates a previously compiled callable. Production reuses stable State identities and restores every neural, delay and RNG value before a condition.
- Poisson mean 4.00336, variance 3.99594 at expected mean 4; mean pair correlation -0.000221; multiple arrivals retained.
- Full-scale graph: 12.5M E and 3.125M I edges; no duplicates/autapses and exact indegrees. Warm 100 ms smoke: 3.51 s; compile 1.33 s.
- Forward simulation only; no fitting/training coverage.

## Checkpoint
- Iteration: 1
- Step: 3
- Resume at: 1/4

### Artifacts
- `acceleration.json`, `acceleration.md`: exact full-size dynamic/static parity, measured speedup.
- `checks-static.log`, `checks.json`: passing accelerated path and seeded replay.
- `smoke/`: static-condition CPU smoke, finite and full-size.
- `smoke-dynamic/`: preserved baseline smoke.
- `benchmark.log`, `benchmark-affinity.log`: supporting workload measurements.

### Important milestones
- Static specialization of the fixed condition scalars avoids an expensive runtime Poisson branch; exact full-size spike and final voltage parity verified.
- State snapshots preserve identity; every condition restores all recorded neural, delay and RNG State values.
- Fine-dt global spectra and assessment counts are explicitly rebinned to the supplied 0.1 ms observation bins; native dt timestamps remain available for ISIs.
- Ready for immutable production launch with unchanged locked protocol.

## Checkpoint
- Iteration: 1
- Step: 4
- Resume at: 1/4

### Artifacts
- `runs/locked-baseline/`: preserved deterministic failed run, exit code 1; condition 0 raw evidence complete, second condition failed during compiled invocation.
- `partial-run-diagnostic.png`, `FIGURE_MANIFEST.md`, `report.md`: diagnostic closure for partial unaccepted evidence.
- `checks-workspace.log`, `checks.json`: corrected eager public-operator initialization passes exact replay and a second static-condition compile.

### Important milestones
- BrainEvent CSR lazily allocated workspace captured a tracer when first invoked under compilation, then failed at another static condition. No package source inspected; runtime traceback identified execution error.
- Initialize the public sparse communication operator eagerly before any transformation. Scientific equations, graphs, seeds, order, protocol and frozen decision rules unchanged.
- Corrected immutable execution will use run ID locked-baseline-v2; parent run remains available. No scientific interpretation used to tune any rule.

## Checkpoint
- Iteration: 1
- Step: 4
- Resume at: 1/5

### Artifacts
- `runs/locked-baseline-v2/config.json`, `RUN_SPEC.md`, `environment.json`, `command.txt`, `code/`: immutable contract/provenance.
- `runs/locked-baseline-v2/run.log`, `status.json`, `exit_code`: done, exit 0, 16/16 runs, 561.85 s wall.
- `runs/locked-baseline-v2/graphs/`, `raw/`, `metrics/`, `metrics.json`, `metrics.csv`, `assessment.json`: complete raw and derived evidence.
- `runs/locked-baseline-v2/raw_audit.json`, `numerical_sensitivity.json`, `artifact_manifest.json`: passing independent host-side count/sample-CV audit and complete identity records.
- `result-assessment.md`, `report.md`: frozen claim-evidence matrix and provisional report.
- `diagnostic-figures/`, `FIGURE_MANIFEST.md`: five diagnostic PNGs; main figure inspected.

### Important milestones
- All 12 primary and four predeclared fine-dt simulations completed with supplied data unchanged.
- Frozen outcomes: synchronous regular supported; fast synchronous irregular inconclusive; asynchronous irregular unsupported; slow synchronous irregular inconclusive.
- Main primary frequencies: 667 Hz; 181–183 Hz; 137–142 Hz; 22–23 Hz. These are global spectral peaks, not per-neuron firing rates.
- Fast irregularity crosses the frozen CV threshold in one primary seed and changes substantially under dt halving. No threshold retuning or forced labels.
- No literature or scientific example/source consultation. Ready for independent Codex review with the same restriction.

## Checkpoint
- Iteration: 1
- Step: 5
- Resume at: 2/1

### Artifacts
- `reviews/iteration-1.md`: verbatim independent Codex review, REFUSE.
- `reviews/iteration-1-response.json`: raw response; thread 01a1b9ab-257b-7951-be38-c8c519c23ed0.
- `report.md`, `FIGURE_MANIFEST.md`, `diagnostic-figures/`: diagnostic closure; claims remain unaccepted, scientific outcome partially_supported.

### Important milestones
- Reviewer independently decoded all 16 raw archives and reproduced counts, per-neuron CVs, spectra and all four deterministic verdicts; graph invariants, provenance, execution parity and figure sources checked.
- BX-001 (major): assess BrainTools power_spectral_density against locked Welch settings before retaining SciPy; document capability gap/parity or use BrainTools if suitable. Existing simulations do not require rerunning.
- Return to iteration-2 mechanics study of general guard, BrainPy-State metric routing and the BrainTools spectral API. No scientific parameter, threshold or output selection changes.

## Checkpoint
- Iteration: 2
- Step: 1
- Resume at: 2/2

### Artifacts
- `brainx-study-record-iteration-2.md`: finding-to-owner map, completed mechanics restudy and correction design.
- `api-docs/power_spectral_density.txt`: public API contract, including symmetric-versus-periodic Hann distinction.

### Important milestones
- Native BrainTools PSD supports the segment and overlap controls but exposes neither window selection nor detrend selection. The public contract identifies a symmetric window; the executed frozen estimator uses periodic Hann.
- Compare saved rate series, exact spectral statistics and classifications before choosing native use or documenting the smallest necessary SciPy boundary. No raw simulation rerun is needed or scientifically warranted.
- User's no-reference restriction remains active. No example solutions or installed scientific source inspected.

## Checkpoint
- Iteration: 2
- Step: 2
- Resume at: 2/3

### Artifacts
- `spectral_api_check.py`, `analysis-iteration-2.log`, `analysis-iteration-2/spectral_api_check.json`, `analysis-iteration-2/PSD_comparison.npz`: public-API capability check on saved data.
- `BrainTools-spectral-api-gap.md`: complete BX-001 capability-gap and boundary justification.

### Important milestones
- Native PSD uses symmetric Hann without the required per-segment detrending; public signature has no controls for either.
- Native behavior matches the symmetric/non-detrended reference to ~1e-7 relative L2, while exact frozen SciPy re-evaluation reproduces all archived P, Q, peak frequencies and labels.
- Preserve native/frozen differences, including altered alternative labels. Retain the exact frozen estimator through the smallest one-call SciPy boundary. No simulation/code/scientific contract changes.

## Checkpoint
- Iteration: 2
- Step: 3
- Resume at: 2/4

### Artifacts
- `analysis-iteration-2/acceleration.md`: unchanged execution decision for the read-only analysis correction.
- `acceleration.json`, `corrected_execution_parity.json`: prior model acceleration/parity, still applicable.

### Important milestones
- No simulation or State-aware rewrite; existing exact trajectory evidence remains valid.
- Use the native batched spectral API only for the capability comparison; keep frozen SciPy estimator for final scientific results.

## Checkpoint
- Iteration: 2
- Step: 1
- Resume at: 2/2

### Artifacts
- `brainx-study-record-iteration-2.md`: additional routed-API study and revised decision, superseding the preliminary retention decision above.
- `api-docs/spectrogram.txt`, `api-docs/multitaper_psd.txt`, `api-docs/band_power.txt`: public contracts only.

### Important milestones
- BrainTools spectrogram provides all exact locked Welch controls; average its documented segment axis. This removes the SciPy spectral boundary.
- The earlier direct-PSD gap comparison remains preserved, but is not a valid reason to bypass another suitable routed API. No scientific rule or estimator change.

## Checkpoint
- Iteration: 2
- Step: 2
- Resume at: 2/3

### Artifacts
- `analysis_spectrum.py`, updated `experiment.py`: BrainTools spectrogram + segment mean implements the exact frozen Welch estimator.
- `recompute_spectra.py`, `analysis-iteration-2/braintools-final/`: successful native reanalysis of all 16 saved runs; input hashes unchanged; full PSD/P/Q/peak/label parity.
- `BrainTools-spectral-api-gap.md`: resolved capability assessment superseding the preliminary general-gap proposal.
- `analysis_checks-native.log`, `analysis_checks.json`: known-signal checks pass with native analysis.

### Important milestones
- No SciPy spectral operation remains in the current production analysis path; the archived execution snapshot retains the original estimator for provenance.
- All native frequencies and labels exactly match; PSD/P/Q agree within stated floating-point tolerances. Offline float64 alone improves parity precision; neural simulation State stays archived float32.
- Earlier direct-PSD API differences and unsuccessful general-gap proposal remain preserved as historical evidence. The spectrogram API is suitable, so it is used.

## Checkpoint
- Iteration: 2
- Step: 3
- Resume at: 2/4

### Artifacts
- `analysis-iteration-2/braintools-final/parity.json`, `manifest.json`: full native-analysis parity and timing evidence.

### Important milestones
- No further acceleration: 16 saved spectral analyses are inexpensive; preserve the exact estimator and source evidence. Simulation acceleration remains unchanged.

## Checkpoint
- Iteration: 2
- Step: 4
- Resume at: 2/5

### Artifacts
- `analysis-iteration-2/braintools-final/RUN_SPEC.md`, `config.json`, `command.txt`, source snapshots, `run.log`, `exit_code`, `manifest.json`: immutable successful offline native reanalysis.
- `analysis-iteration-2/braintools-final/metrics/`, `metrics.json`, `assessment.json`, `parity.json`: all sixteen spectra reproduced through BrainTools; labels/frequencies exact, P relative difference <=1.06e-12, Q absolute difference <=1.12e-16.
- `analysis_spectrum.py`, `recompute_spectra.py`, `plot_results.py`: current analysis and plotting use native spectral evidence.
- `report.md`, `result-assessment.md`, `diagnostic-figures/`: updated provisional report and native-source diagnostic figures.
- `analysis-iteration-2/verification/`: preserved direct-PSD capability comparison, including unfavorable differences.

### Important milestones
- BX-001 resolved by a suitable native API, not an asserted general gap. No remaining SciPy spectral boundary in the current analysis path.
- Entire locked simulation dataset reused unchanged, as explicitly allowed by the review. No extra scientific runs, selection or threshold changes.
- Forward-only native postprocessing, with original host float64 analysis precision; neural State remains float32.

## Checkpoint
- Iteration: 2
- Step: 5
- Resume at: 2/6

### Artifacts
- `reviews/iteration-2.md`: verbatim independent Codex review, PASS, no findings.
- `reviews/iteration-2-response.json`: raw response; thread 01a1b9c0-29ec-7240-b14b-eefa54b70eae.

### Important milestones
- Reviewer independently executed the native spectral reanalysis, reproduced all 16 native spectra exactly and confirmed parity by independent FFT.
- Raw counts, all per-neuron CVs, refractory timing, final State consistency, graph invariants, execution parity, provenance and figure sources independently verified.
- Accepted finite-protocol scientific outcome: partially supported. Requested labels remain supported / inconclusive / unsupported / inconclusive.
- BX-001 resolved; advance to final visualization without new scientific changes.

## Checkpoint
- Iteration: 2
- Step: 6
- Resume at: complete

### Artifacts
- `report.md`: final; scientific outcome partially_supported; independent review PASS.
- `figures/four_conditions.png`, `ei_rates.png`, `isi_cv.png`, `global_rate_spectrum.png`, `step_halving.png`: five accepted final PNGs, all rendered and visually inspected.
- `FIGURE_MANIFEST.md`, `figures/FIGURE_MANIFEST.md`: exact source contracts, hashes, dimensions, transformations and inspection for each PNG.
- `figures/source_checks.json`, `figures/finalization_checks.json`: source values, all sixteen rate/CV/peak summary checks, report-link verification, unchanged specification and model identity.
- `README.md`, `write_report.py`, `plot-final.log`: final output locations and reproducible report/figure assembly.

### Important milestones
- Completed all requested outputs with the supplied network and four conditions unchanged. No papers, scientific examples, existing scientific source or remembered protocol used.
- Final verdicts under locked tests: supported / inconclusive / unsupported / inconclusive. Global primary spectral peaks: 667 / 181–183 / 137–142 / 22–23 Hz.
- Final report explains every figure beside its image, distinguishes population peaks from individual firing frequency, and preserves fast-case timestep sensitivity and all unfavorable results.
- Independent iteration-2 review passed without findings; its verbatim verdict and all raw evidence remain preserved. No further simulation or scientific change was made after acceptance. Loop complete.
