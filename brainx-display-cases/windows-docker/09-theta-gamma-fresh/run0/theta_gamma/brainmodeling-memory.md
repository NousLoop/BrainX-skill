# Brain modeling memory

## Checkpoint
- Iteration: 1
- Step: 0

### Artifacts
- `NeuroSpecification.md`: locked；完整数值、对照、指标和允许主张。
- `report.md`: draft，scientific pending，review pending。

### Important milestones
- fresh-new。用户明确委托所有科学/数值选择并授权锁定；澄清门已完成，没有待确认项目。
- 只表示 aggregate E/I populations，路由 BrainMass；forward-simulation，无训练或拟合。
- 文献门跳过：授权现象学 WC 模型，不建立任何生物或实测 EEG 主张。
- 已检查现有 brainmass/brainstate/brainunit/braintools/JAX/分析依赖可导入；不要求安装元包即可运行。
- 下一步 1：完整学习 owning skills，再开始实现。

## Checkpoint
- Iteration: 1
- Step: 1

### Artifacts
- `brainx-study-record.md`: completed before implementation; routed skills, canonical WC script, API decisions and frozen analysis/display contract.
- `docs/`: official WC, input and spectral API pages plus execution checks.

### Important milestones
- Public WC derivative extension preserves locked unshifted logistic equations; inherited Simulator owns all lifecycle and execution.
- Native condition and IC batch axes selected; no training/fitting coverage.
- Next action: step 2, implement model and focused verification.

## Checkpoint
- Iteration: 1
- Step: 2

### Artifacts
- `model.py`, `analysis.py`, `experiment.py`, `verify.py`, `launch.py`: implementation and focused checks.
- `API-gap.md`, `docs/api_execution_checks.json`: verified external analysis boundary.
- `checks/verification.json`, `checks/verification.log`: PASS.
- `failure-log.md`, `checks/first-construction.log`, `checks/verification-failed-1.log`, `checks/verification-failed-2.log`, diagnostic logs: all preliminary failures retained.
- `figures.py`, `assess.py`: predefined figure and deterministic assessment consumers.

### Important milestones
- One-step equations, old-State update order, physical time/input, bounded/finite State, batch/scalar final State, reset, native/synthetic metrics validated.
- Transient Euler error converges linearly; original heuristic cutoff and incompatible native-MI witness failures retained, without changing model/production settings.
- Next action: step 3, unchanged native-batched Simulator acceleration decision.

## Checkpoint
- Iteration: 1
- Step: 3

### Artifacts
- `acceleration.md`: inventory, unchanged decision, parity, timing interpretation and memory estimate.
- `checks/verification.json`: no output/final-State changes from native batching/JIT.

### Important milestones
- Retained highest-level Simulator JIT, native IC/condition batching, no custom lower-level rollout or speedup claim.
- Next action: step 4, immutable CPU smoke snapshot; then separate production and dt-half snapshots.

## Checkpoint
- Iteration: 1
- Step: 4

### Artifacts
- `runs/smoke-01/manifest.json`: CPU target smoke done / exit 0.
- `runs/production-01/manifest.json`: 12 s, 75 trajectories, 300 view/IC/condition metric rows, raw + config + immutable source/environment identities.
- `runs/convergence-01/manifest.json`: fixed-pair dt-half simulation done / exit 0.
- `assessment.json`, `result-assessment.md`, `claim-evidence.md`, `checks/carrier-audit.json`: deterministic band result and honest scientific partial failure.
- `figures/diagnostic/`, `FIGURE_MANIFEST.md`, `report.md`: rendered/inspected diagnostic closure, no final figure.

### Important milestones
- Numeric checks and band-nesting predicate pass, but E autonomous cycle ~21.76 Hz (dominant bin 22 Hz); gamma band peak 43.5 Hz is harmonic. This is NOT accepted as an autonomous gamma circuit.
- Scientific outcome partially_supported. Existing results preserved without outcome tuning.
- Proposed correction after independent review: halve both population time constants, a declared phenomenological time scaling; freeze stronger carrier acceptance before another production run. User delegated remaining settings/locking, so no new approval is required.
- Next action: step 5, fresh independent Codex MCP review of completed iteration 1 including all unfavorable evidence.

## Checkpoint
- Iteration: 1
- Step: 5

### Artifacts
- `reviews/iteration-1.md`: verbatim independent REFUSE; scientific PARTIALLY_SUPPORTED.
- `reviews/iteration-1-thread.json`: threadId 01a1a3e1-de71-7a91-ae87-2177c7c76941.
- `report.md`, `FIGURE_MANIFEST.md`: diagnostic closure completed; figures inspected and unaccepted.

### Important milestones
- BX-001 major: add spectral plus E/I cycle-rate carrier predicate; preserve all original evidence; new common time scaling requires fresh forced/numerical/scan evidence.
- BX-002 minor: regenerate claim matrix and label original band predicates consistently.
- BX-003 minor: use documented brainstate.nn.sigmoid and rerun equation/parity witnesses.
- Transition: iteration 2, step 1. User already delegated all scientific settings and lock authority; no permission gate remains.
- Initial root artifacts will be preserved under iterations/iteration-1; immutable runs remain in runs/*-01.

## Checkpoint
- Iteration: 2
- Step: 0

### Artifacts
- `NeuroSpecification.md`: revision 2 locked under existing explicit researcher delegation; supersedes original step-0 scientific timescales and carrier acceptance, not original evidence.
- `iterations/iteration-1/`: preserved root source, specification, checks, assessment/report and diagnostic figures; original immutable runs remain under runs/*-01.

### Important milestones
- Common tau scale is outcome-calibrated to correct beta carrier failure; no biological/unique-mechanism claim. Revised carrier predicate frozen before new simulation.
- Literature gate remains skipped for approved phenomenological scope; no new biological premise.

## Checkpoint
- Iteration: 2
- Step: 1

### Artifacts
- `brainx-study-record-iteration-2.md`: finding-to-skill map, reread roots/references/canonical script, revised API/experiment design.

### Important milestones
- Restudy completed before implementation changes. Coverage remains forward-simulation.
- Next action: step 2, native sigmoid and timescales; offline carrier audit and regenerated consistent evidence export.

## Checkpoint
- Iteration: 2
- Step: 2

### Artifacts
- `model.py`: native sigmoid and configurable unit-aware tau; same public WC/Simulator extension.
- `analysis.py`: original legacy_band_valid retained; new E/I cycle+spectral continuous carrier margins and timing predicate.
- `verify.py`, `checks/verification.json`, `checks/verification-iteration-2.log`: PASS; harmonic-only gamma negative control rejected.
- `launch.py`, `experiment.py`, `assess.py`, `figures.py`: new immutable *-02 runs, carrier smoke gate and consistent claim export; no old artifact overwrite.

### Important milestones
- Revised equation/State/batching/input/reset/synthetic-metric checks pass; native sigmoid parity <1e-15.
- Baseline gamma carrier will be tested in target CPU smoke before production. Next action: step 3.

## Checkpoint
- Iteration: 2
- Step: 3

### Artifacts
- `acceleration-iteration-2.md`: unchanged native execution decision, renewed parity/memory evidence.

### Important milestones
- No custom rollout/vmap or performance semantics changes; memory budget <2 GB expected.
- Next action: step 4, smoke-02 gamma-carrier gate, then production-02 and convergence-02.

## Checkpoint
- Iteration: 2
- Step: 4

### Artifacts
- `runs/smoke-02/manifest.json`, `runs/smoke-02/metrics/smoke_carrier.json`: CPU carrier gate passed for E/I and all 3 ICs before production.
- `runs/production-02/manifest.json`: full 75-case revised scan; 300 metric rows with peak timing/PSD/band/carrier margins and raw E/I/input, exit 0.
- `runs/convergence-02/manifest.json`: dt=0.025 ms fixed-pair run, exit 0.
- `assessment.json`, `result-assessment.md`, `claim-evidence.md`: carrier-aware supported result, provisional pending review.
- `report.md`, `figures/diagnostic-iteration-2/`, `FIGURE_MANIFEST.md`: current diagnostic report; all PNGs opened/checked against raw data.
- `reviews/addressed-iteration-1.md`, `failure-log.md`: all findings addressed and unfavorable settings retained.

### Important milestones
- Fixed m=0 control E/I mean cycles ~43.53 Hz and strongest PSD ~43.5 Hz pass autonomy predicate; m=0.75 has repeated fast cycles in theta-locked bursts.
- Fixed first-IC proxy R 0.00027168→0.50162450. max dt-half ΔR=0.00134675, peak difference 0 Hz; controls exact, State bounded/finite.
- High-R invalid settings remain visible. Outcome-supported means only frozen illustrative scope; tau scale is outcome-calibrated, not a biological prediction.
- Next action: step 5, fresh independent Codex MCP review iteration 2 with original refusal and preserved failures.

## Checkpoint
- Iteration: 2
- Step: 5

### Artifacts
- `reviews/iteration-2.md`: verbatim independent PASS, SCIENTIFIC_OUTCOME SUPPORTED, no findings.
- `reviews/iteration-2-thread.json`: threadId 01a1a3f1-51c2-7711-ba28-7daa23619485.
- `reviews/acceptance.json`: exact accepted scope and review hash.
- `checks/all-run-integrity.json`: all 6 immutable run manifests verified with no hash failures.

### Important milestones
- Reviewer independently reproduced all 324 production/convergence rows and derived arrays exactly; manifests verify.
- Autonomous ~43.53 Hz, proxy R 0.000272→0.501625; four readouts/three ICs/two windows agree; max dt-half ΔR 0.001347, band peaks unchanged.
- Accepted illustrative scope explicitly retains calibration, initial failure, harmonic ambiguity and unfavorable settings.
- Next action: step 6, final-mode visualization and final Chinese report, then figure-manifest/render verification.

## Checkpoint
- Iteration: 2
- Step: 6
- Workflow status: complete

### Artifacts
- `report.md`: final Chinese report; scientific outcome supported; independent review PASS; all figures explained beside their evidence.
- `figures/final-iteration-2/{traces,nesting,scan}.{png,pdf}`: accepted final figures; all PNG and independently rasterized PDF exports opened and visually inspected.
- `FIGURE_MANIFEST.md`: diagnostic iterations 1/2 and accepted final exports, source hashes, processing, fixed comparisons and render checks retained.
- `checks/final-delivery.json`: report/README links verified, all six final export hashes recorded, reviewer hash verified, isolated PDF renderer identity and visual checks recorded.
- `checks/all-run-integrity.json`: all six immutable run snapshots pass hash verification; original failures and unfavorable settings remain preserved.

### Important milestones
- Step 6 complete after iteration-2 independent Codex MCP PASS; no scientific or numerical changes after acceptance.
- Final answer: autonomous E/I carrier about 43.53 Hz; fixed-pair proxy R about 0.000272 without circuit modulation and 0.501625 with modulation. Depth/gain response is not universally monotonic; invalid/high-R settings remain visible.
- Accepted scope remains illustrative/phenomenological; no biological realism, measured EEG or unique-mechanism claim. Initial beta-carrier failure and outcome-calibrated timescale revision disclosed.
- Next action: none; deliver final report and links. No pending user decision or running experiment.
