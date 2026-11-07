# Brain modeling memory

## Checkpoint
- Iteration: 1
- Step: 0

### Artifacts
- `NeuroSpecification.md`: locked under explicit user delegation; all design and numerical choices fixed, including a baseline-only calibration rule.
- `report.md`: draft, scientific outcome pending, review pending.

### Important milestones
- Entry: fresh-new; empty workspace, no data or earlier state.
- Clarification frontier resolved by the user's explicit choose-and-lock instruction; no question or wait required.
- Literature gate skipped: exclusively illustrative design with no empirical or biological mechanism claim.
- Required execution components are importable in /brainx-venv/bin/python. Lowercase brainx meta import absent; install skill read, no installation needed because all execution dependencies are present. No environment changes planned.
- Next: step 1 package/API study; forward simulation, no training/fitting coverage.

## Checkpoint
- Iteration: 1
- Step: 1

### Artifacts
- `brainx-study-record.md`: completed study and exact equations/API conventions.
- `evidence/*_official.txt`, `evidence/api-gap.md`: official API evidence and justified host metric boundary.

### Important milestones
- Corrects step-0 lowercase-meta-package note: `BrainX` is present. No environment mutation needed.
- All controls are m=0 from t=0 matched by exact initial State, not a within-run withdrawal switch; no shared dynamical prefix is scientifically claimed. Initial State is the intervention boundary and all lanes share it within each pair.
- Package sigmoid allows bounded negative abstract activity. Its documented default transfer parameters and invariant-domain interpretation recorded before any execution; this clarifies the locked family rather than outcome-driven tuning.
- Next: step 2 implementation and small checks.

## Checkpoint
- Iteration: 1
- Step: 2

### Artifacts
- `model.py`, `analysis.py`, `experiment.py`, `launch.py`, `base_config.json`: implemented model, analysis, frozen run launcher and experiment.
- `test_checks.py`, `evidence/tests.json`, `evidence/test.log`: PASS equations, units, State reset, time/shape, native batching vs scalar and JIT vs non-JIT (including final E/I), paired observation noise, metric positive/null and independent phase rotation tests.
- `evidence/tests-attempt1.log` through `tests-attempt4.log`: retained development failures (unit conversion, shape conversion, equation mismatch).
- `evidence/api-direction-discrepancy.md`: tested compatibility adapter, no scientific parameter change.

### Important milestones
- Host statistics use ground-truth drive phase. BrainTools filter agrees with SciPy to 1.2e−14 in the validation witness; analytic AM R≈0.300, constant-amplitude R<1e−6.
- No production outcome inspected. Next: step 3 acceleration assessment.

## Checkpoint
- Iteration: 1
- Step: 3

### Artifacts
- `evidence/acceleration.md`: audit, native batched execution unchanged decision, parity and memory rationale.
- `evidence/tests.json`: output/final-State parity, reset and independence evidence.

### Important milestones
- High-level Simulator already covers time and batch axes. No speedup claim or custom rollout.
- Next: step 4 immutable target-CPU smoke, baseline calibration, production, refinement, monitor and collection.

## Checkpoint
- Iteration: 1
- Step: 4

### Artifacts
- `runs/smoke-01/`, `runs/calibration-01/`, `runs/production-01/`, `runs/production-02/`: immutable source/config/environment snapshots, logs, exit codes, data and manifests.
- `evidence/run-lineage.md`: development failures, superseded approximate surrogate and exact replacement; no scientific retuning.
- `evidence/result-assessment.md`, `evidence/sweep.csv`, `evidence/integrity.json`, `assess_results.py`: deterministic reconstruction, all conditions and claim-evidence matrix.
- `figures/diagnostic_*.png`, `.pdf`, `FIGURE_MANIFEST.md`: diagnostic evidence; first renders preserved separately.
- `report.md`: provisional supported scientific result, review pending.

### Important milestones
- Calibration chose P0=1.6, absolute base gain=1.2 by locked unmodulated-only rule; 8/18 eligible, baseline peak29.5Hz.
- production-02 complete: shape12000×3×49, 60 cycles, all 21 refinement checks PASS. All three prespecified display lanes pass the fixed full nesting predicate. Nonmonotonic and ineligible settings retained.
- Exact within-cycle envelope rotations supersede the approximation; direct-roll witness error<3e−17. The original two runs have exactly equal circuit trajectories.
- Source-value checks exposed initial R color saturation; expanded to full mathematical range with explicit disclosure and preserved originals, no condition or threshold change.
- Next: step 5 fresh independent Codex MCP review; no final figures before PASS.

## Checkpoint
- Iteration: 1
- Step: 5

### Artifacts
- `reviews/iteration-1.md`: exact verbatim independent MCP Markdown report, preserved before classification.
- `reviews/gate.json`: PASS, accepted run production-02 and review hash.
- `reviews/request-iteration-1.txt`: exact review request with 64 verified concrete artifact paths.

### Important milestones
- Review outcome: PASS; scientific outcome: SUPPORTED; no findings. Next action ADVANCE_TO_VISUALIZATION.
- threadId: 01a1ae86-d767-74a2-9de3-9206de1fc7d0.
- Reviewer independently reconstructed observations, filters, envelopes, spectra, all 200 surrogate values and every classification from raw trajectories. All 21 refinement checks pass. The read-only reviewer environment blocked its package-test rerun through a Matplotlib cache permission, noted explicitly in the raw report; retained owner test results and independent reconstruction support PASS.
- Accepted scope is the locked illustrative/phenomenological demonstration only. Next: step 6 final figures, manifest inspection, and Chinese report.

## Checkpoint
- Iteration: 1
- Step: 6

### Artifacts
- `report.md`: FINAL Chinese report; Scientific outcome supported; Review outcome PASS. Contains all final figures beside their explanation, paired values, nonmonotonic and ineligible cases, scope limits and reproducibility links.
- `figures/final_traces.png`, `final_phase_and_spectra.png`, `final_parameter_sweep.png` plus matching PDFs and `final_plotted_values.npz`: post-PASS exports.
- `FIGURE_MANIFEST.md`, `figures/DIAGNOSTIC_FIGURE_MANIFEST.md`, `evidence/final-figure-checks.json`: inspected render/source contracts, exact final/diagnostic numeric parity, source hashes; independent PDF rasterizer unavailable, displayed PNGs visually inspected and PDF structure verified.
- `README.md`, `evidence/data-dictionary.md`: entry points and complete axes/units/field semantics.
- `reviews/iteration-1.md`, `reviews/gate.json`: independent PASS, scope and reviewer thread retained.

### Important milestones
- Loop completed. Final displays use only review-passed production-02, with no changed science or decision after review.
- All failures, superseded outputs, ineligible baseline conditions and unsupported monotonic expectations preserved.
- Result: externally imposed theta produces modest known-phase gamma-envelope nesting at the prespecified display case; removal leaves gamma but greatly reduces nesting. Effects depend nonmonotonically on sampled depth/gain. All claims remain illustrative, no empirical EEG or mechanism uniqueness.
