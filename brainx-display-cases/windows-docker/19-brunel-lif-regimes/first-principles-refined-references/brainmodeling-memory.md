# Brain modeling memory

## Checkpoint
- Iteration: 1
- Step: 0
- Resume at: 1/1

### Artifacts
- `NeuroSpecification.md`: locked specification v1, before implementation or simulation
- `report.md`: initialized draft; outcome and review pending

### Important milestones
- Fresh project in an empty workspace. All open decisions explicitly delegated by researcher; clarification gate complete without another question.
- Literature gate skipped under researcher source restrictions. Only skill/API mechanics may be studied. No scientific example code will be opened.
- Fixed seeds, run length, controls, sampling and quantitative decision rules locked; requested labels remain hypotheses.

## Checkpoint
- Iteration: 1
- Step: 1
- Resume at: 1/2

### Artifacts
- `brainx-study-record.md`: completed API mechanics study, source restrictions and API-gap decisions

### Important milestones
- Required component packages import; CPU backend available. Meta-package absence does not require installation because execution dependencies are present. No environment mutation requested or performed.
- No scientific example scripts, implementation sources or papers consulted. Custom endpoint update and exact Poisson count source chosen to preserve the frozen equations.

## Checkpoint
- Iteration: 1
- Step: 2
- Resume at: 1/3

### Artifacts
- `model.py`, `experiment.py`, `analysis.py`, `checks.py`: complete model, immutable run/provenance runner, frozen analysis and focused component checks
- `checks/components.json`, `checks-launch.log`: passing component/reference/unit/Poisson evidence
- `checks-launch-attempt1.log`, `checks-launch-attempt2.log`: preserved pre-production fixture/reset failures and their corrections

### Important milestones
- Native delay and voltage jump verified at 1.5 ms at both grids; integer refractory release exactly 2 ms.
- Compiled spikes match explicit small reference; voltage discrepancies <0.00003 mV. Exact Poisson multiplicity and RNG replay verified.
- Added only a documented State-reset correction after failed full-size replay; no scientific changes.

## Checkpoint
- Iteration: 1
- Step: 3
- Resume at: 1/4

### Artifacts
- `acceleration.md`, `checks/acceleration.json`, `checks/full_size_smoke.npz`: full-size target-CPU smoke, timing, deterministic parity and finite outputs
- `FIGURE_CONTRACT.md`: presentation reductions and deterministic axis rules frozen before production

### Important milestones
- Full-size 500-step run replays exactly after stable State-value restoration. Production uses unchanged compiled physics with at most 3 independent process-owned seed groups, followed by numerical controls.

## Checkpoint
- Iteration: 1
- Step: 4
- Resume at: 1/4 (production still running; monitor existing process, do not relaunch)

### Artifacts
- `runs/baseline-v1/`: immutable run snapshot, exact graphs/initial states, raw events and metrics
- `production-launch.log`: parent session 94082; child fine-grid worker PID 2517, group log `runs/baseline-v1/group_seed101_dt0.05.log`
- `figures/diagnostic-baseline/four_conditions.png`: real completed baseline data; rendered/inspected, unaccepted
- `FIGURE_MANIFEST.md`: interim figure provenance; `checks/evidence_audit.json`, `RAW_EVIDENCE.md`: baseline per-bin/graph serialization audit
- `plot_results.py`, `write_report.py`, `audit_evidence.py`: postprocessing/report/serialization audit code (outside immutable simulation snapshot)

### Important milestones
- All 12 baseline runs completed without scientific settings changing: SR and fast SI supported across seeds; requested AI unsupported; slow SI inconclusive with low ISI eligibility and one failed spectral-concentration test. These conclusions are provisional before full controls/review.
- First two fine-grid controls completed; remaining conditions use the same full physical duration and graph/initial state. Never shorten or retune them after viewing results.
- Next: wait for existing production session completion, audit 16 raw runs, render all diagnostic PNGs, generate report and raw index, and submit fresh independent Codex iteration-1 review. Review must include the explicit no papers/scientific examples/existing scientific implementations/remembered protocols restriction. Only after PASS create acceptance.json and final figures/report. No review call has yet been made.

## Checkpoint
- Iteration: 1
- Step: 4
- Resume at: 1/5

### Artifacts
- `runs/baseline-v1/status.json`, `exit_code`: all 16 runs complete, exit 0; elapsed 1435.38 s
- `runs/baseline-v1/manifest.json`, `environment.json`, `config.json`: immutable execution/provenance hashes
- `runs/baseline-v1/assessment.json`, `assessment.md`, `metrics_summary.csv`, `population_rates.npz`: all frozen reductions and quantitative decisions
- `checks/evidence_audit.json`, `RAW_EVIDENCE.md`: 16/16 raw files audited; every E/I bin matches packed spikes; all graph/identity checks pass
- `checks/temporal_poisson.json`, `check_temporal_input.py`: temporal input independence verified through the production State-aware transform pattern
- `figures/diagnostic/{four_conditions,ei_rates,isi_cv,global_rate_spectra,regime_tests}.png`, `FIGURE_MANIFEST.md`, `report.md`: rendered/inspected diagnostic outputs and provisional report

### Important milestones
- No parameter, graph degree, duration, seed, evaluation rule or display case changed after locking. Controls preserve SR/fast SI support and AI non-support; slow SI remains inconclusive and its oscillation predicate is grid sensitive.
- All 5 PNG types inspected against values; E/I means given cosmetic upper-axis headroom after initial render. No simulation or analysis changed for plotting.
- Scientific outcome provisional partially_supported. Independent review pending. Next step is one fresh MCP Codex review with all paths and researcher source restriction; do not finalize figures before PASS.

## Checkpoint
- Iteration: 1
- Step: 5
- Resume at: 2/1

### Artifacts
- `reviews/iteration-1.md`: verbatim independent REFUSE; threadId 01a1b9fd-a416-7c12-812c-76694878ac9a
- `reviews/iteration-1.response.json`, `reviews/request-iteration-1.txt`: exact transport and request
- `report.md`, `FIGURE_MANIFEST.md`, `figures/diagnostic/`: diagnostic closure, all scientific claims remain provisional

### Important milestones
- Reviewer independently recomputed all 16 runs and confirmed counts, rates, CVs, synchrony, spectra, refractory timing, assessment and all hashes. Scientific outcome PARTIALLY_SUPPORTED.
- BX-001 major: use documented BrainTools spectrogram with frozen windows/detrending and average segment PSD, rather than undocumented SciPy spectral bypass; verify normalization, units, shapes and all decisions against saved evidence.
- BX-002 minor: synthetic test input was overwritten by identically named derived NPZ in the same directory. Preserve a distinct raw fixture path and runnable test; guard against this collision.
- No production simulation rerun required if reanalysis preserves evidence. Preserve original immutable run, diagnostics and review. Restudy owning package mechanics before changes, create iteration-2 reanalysis evidence, then fresh independent review. No scientific parameters or thresholds may change.

## Checkpoint
- Iteration: 2
- Step: 1
- Resume at: 2/2

### Artifacts
- `brainx-study-record-iteration-2.md`: completed finding-to-owner restudy and narrow correction design

### Important milestones
- Documented BrainTools spectrogram covers both frozen estimators; no spectral API gap is needed.
- Preserve the original run and first review. Correct only analysis ownership and fixture serialization, then require all-16 numerical/decision parity before a new review. No model/parameter/seed/threshold changes.

## Checkpoint
- Iteration: 2
- Step: 2
- Resume at: 2/3

### Artifacts
- `analysis.py`: documented physical-unit BrainTools spectra; input/output collision guard
- `check_metric_fixture.py`, `checks/metrics_fixture_v2/test_result.json`: retained raw fixture and passing rerunnable test
- `reviews/addressed-iteration-2.md`: concrete corrections and unchanged scientific scope

### Important milestones
- Both review findings corrected after owning-package restudy. Original input failure and immutable baseline preserved. No scientific parameters or decisions changed.

## Checkpoint
- Iteration: 2
- Step: 3
- Resume at: 2/4

### Artifacts
- `acceleration-iteration-2.md`: unchanged compiled model, analysis-only execution audit and parity
- `runs/iteration-2/spectral_parity.json`: all 16 spectra/reductions/predicates preserved

### Important milestones
- Physical float64 spectral analysis matches original arrays to floating-point precision. No new simulation optimization or production rerun required.

## Checkpoint
- Iteration: 2
- Step: 4
- Resume at: 2/5

### Artifacts
- `runs/iteration-2`: immutable analysis-only code/config/environment/raw-parent snapshot, metrics, assessment, log, manifest and successful status
- `reanalysis-launch.log`: all 16 parity checks PASS

### Important milestones
- 29.505 seconds for all corrected reanalyses. Every original raw hash, model hash and final decision preserved. Next: inspect iteration-2 diagnostic exports and send a fresh independent Codex review with all evidence and source restrictions.

## Checkpoint
- Iteration: 2
- Step: 4
- Resume at: 2/5

### Artifacts
- `figures/iteration-2-diagnostic/*.png`, `figure_data.npz`, `manifest.json`: all five figures rendered and visually inspected
- `report.md`, `FIGURE_MANIFEST.md`, `reviews/request-iteration-2.txt`: current diagnostic closure and concrete verified review paths

### Important milestones
- Supersedes the preceding step-4 checkpoint only for figure/report completion. All original and iteration-2 manifest entries verified; frozen specification byte-identical to pre-production snapshot. All five diagnostic PNGs are legible, nonblank and unclipped. Independent review is the remaining gate.

## Checkpoint
- Iteration: 2
- Step: 5
- Resume at: 2/6

### Artifacts
- `reviews/iteration-2.md`: verbatim PASS, scientific outcome PARTIALLY_SUPPORTED; no findings
- `reviews/iteration-2.response.json`: original tool transport, threadId 01a1ba0c-b2b2-72f3-a630-94c4a387dbde
- `reviews/acceptance.json`: accepted exact run, review hash, scope and code/specification identities

### Important milestones
- Independent recomputation confirmed all 16 runs and both manifests. Both earlier findings resolved; no production rerun required. Native BrainTools execution could not be replayed in the reviewer sandbox because Matplotlib lacked a writable cache; documented API, provenance, all-16 parity and independent numerical recomputation supported PASS. Preserve this limit with the verdict.
- Final scientific labels: SR and fast SI supported; AI unsupported; slow SI inconclusive. Proceed only with accepted results to final visualization.

## Checkpoint
- Iteration: 2
- Step: 6
- Resume at: complete

### Artifacts
- `report.md`: final; scientific outcome partially_supported; review PASS
- `figures/final/four_conditions.png`: 0.1-ms instantaneous global rate with dashed mean over fixed 50-neuron raster, all four conditions
- `figures/final/ei_rates.png`, `isi_cv.png`, `global_rate_spectra.png`, `regime_tests.png`: final accepted comparisons and predicate evidence
- `figures/final/figure_data.npz`, `manifest.json`, `export_audit.json`: exact plotted arrays, hashes and final export verification
- `FIGURE_MANIFEST.md`, `RAW_EVIDENCE.md`, `README.md`, `artifact_manifest.json`: provenance, complete raw index and runnable handoff

### Important milestones
- All five final PNGs rendered and visually inspected. Every plotted array exactly matches the reviewed diagnostic array; image hashes and report/evidence links verify. Frozen model/analysis/specification hashes match the accepted scope.
- Independent review PASS preserved verbatim. Full 16-run experiment complete with every supplied parameter retained, no scientific source consulted, and no threshold tuning. SR supported (333 Hz); fast SI supported (182–185 Hz); AI unsupported (135–139 Hz peak); slow SI inconclusive (17–23 Hz peak, low CV eligibility and fine-grid spectral sensitivity). These are operational finite-window outcomes, with full limitations in report and review.
