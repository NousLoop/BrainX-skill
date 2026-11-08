# Deterministic assessment and claim-evidence matrix

Frozen rules: NeuroSpecification.md. No thresholds or display seeds changed after simulation.

| (g, eta) | Requested | Seed outcomes | Numerical sensitivity | Decision |
|---|---|---|---|---|
| (3.0, 2.0) | SR | supported, supported, supported | False | supported |
| (6.0, 4.0) | fast SI | supported, supported, supported | False | supported |
| (5.0, 2.0) | AI | unsupported, unsupported, unsupported | False | unsupported |
| (4.5, 0.9) | slow SI | inconclusive, inconclusive, inconclusive | True | inconclusive |

Every baseline/control metric is in `metrics/condition*_seed*_dt*.json`; all-neuron CV and exact spectral reductions are in the corresponding NPZ. All native-grid spikes, E/I counts, final State and RNG key are in `raw/`. Graphs are in `graphs/`. Unsupported labels are retained.

The requested SR/AI/SI claims are supported only by their complete frozen predicate sets, including stationarity and numerical controls. These are operational finite-window categories, not assertions of universal phases.
