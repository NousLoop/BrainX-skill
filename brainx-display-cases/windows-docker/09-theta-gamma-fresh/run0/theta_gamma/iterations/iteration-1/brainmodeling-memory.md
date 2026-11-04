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
