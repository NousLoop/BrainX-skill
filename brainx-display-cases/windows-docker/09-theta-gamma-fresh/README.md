# Fresh theta–gamma skill refinement

Started from zero on 2026-11-04 (Asia/Shanghai). No old case artifacts were used.
`prompt.md` is the frozen modeling task, including the user's authorization to
choose and lock illustrative/phenomenological settings without another question.

- Environment and real main/reviewer calls passed before baseline: see
  `../00-live-model-probe/transport-20261104/`.
- Baseline: `run0/`, exit 0, isolated empty Docker workspace, no seed archive,
  frozen skill hash `bfffa8f44e0b508783e0e77b6d3e80f03d6ebb35ebcc05c1279d34c9c9a2d36d`.
- Independent scientific review: internal iteration 1 REFUSE, iteration 2 PASS;
  both reviews, failed initial carrier and complete experiments retained.
- Result: ~43.53 Hz autonomous carrier; fixed-pair R 0.000272→0.501625;
  maximum fixed-pair dt-half ΔR 0.001347. Grid is descriptive and not universally
  monotonic. Scope remains illustrative, with no physical EEG claim.
- Outer verification: same image, read-only evidence, no model call; all six
  manifests and exact production/convergence replay pass.
- Refinement decision: **no-edit**. Existing instructions cover the diagnosed
  failures; no transferable missing rule remains. `run1/` is intentionally absent
  because a same-snapshot numbered rerun is forbidden.

[中文科学报告](run0/theta_gamma/report.md) ·
[外层 API 覆盖诊断与 no-edit 理由](run0/brainmass-api-coverage-diagnosis.md) ·
[独立 review](run0/theta_gamma/reviews/iteration-2.md) ·
[复跑证据](run0/outer-audit/reproduction.json)

The outer audit adds files beside the untouched generated `theta_gamma/` tree.
It never repairs the baseline. Minor specification axis/date and assessment
wording inconsistencies are recorded in the diagnosis. One transient EOF
reconnected inside the original CLI process; no quota error ended this run.
