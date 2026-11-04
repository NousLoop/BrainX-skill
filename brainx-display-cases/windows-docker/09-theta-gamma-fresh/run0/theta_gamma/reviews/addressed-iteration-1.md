# Findings addressed in iteration 2

- BX-001: New locked specification requires E/I cycle timing plus strongest native PSD
  carrier evidence at m=0. Common tau scale 1.25/2.5 ms explicitly outcome-calibrated;
  fresh smoke-02, production-02, convergence-02 retain all raw/metrics. Synthetic
  22 Hz plus 44 Hz harmonic fails carrier predicate. Original beta result preserved.
- BX-002: assess.py regenerates claim-evidence.md consistently. Original band-only
  result is named legacy_band_valid, distinct from new timing validity/carrier.
  Archived iteration-1 matrix and full source remain unchanged for historical evidence.
- BX-003: model.py uses brainstate.nn.sigmoid twice. checks/verification.json records
  native activation mathematical parity, one-step equations, batch/final-State/reset/JIT
  checks, all PASS.

No approval request: user's original instruction explicitly delegated all remaining
settings and locking. Revision rationale and frozen settings are in NeuroSpecification.
No training or fitting. Proposed next action: independent iteration-2 review;
final figures/report only after PASS.
