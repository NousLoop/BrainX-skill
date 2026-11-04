# BrainX iteration review

- **OUTCOME:** `REFUSE`
- **SCIENTIFIC_OUTCOME:** `PARTIALLY_SUPPORTED`
- **LOSS_CLOSURE:** `NOT_APPLICABLE`
- **OPTIMIZATION_ADEQUACY:** `NOT_APPLICABLE`
- **NEXT_ACTION:** `RETURN_TO_STUDY`

## Good-enough reason

Raw-data recomputation supports the reported band-envelope effect: fixed-pair proxy R rises from 0.000112 to 0.209661, persists across observation controls, and passes the declared numerical checks. Manifests and metric exports agree. BrainMass simulation, batching, units, and the documented SciPy boundary are appropriate. However, the approximately 22 Hz autonomous rhythm does not establish the requested gamma carrier, and the claim–evidence matrix has not consistently incorporated that limitation.

## Findings

### BX-001: Band validity does not establish a gamma carrier

- **Severity:** `major`
- **Location:** [analysis.py](/workspace/theta_gamma/analysis.py:78); [carrier-audit.json](/workspace/theta_gamma/checks/carrier-audit.json)
- **Problem:** The predicate accepts a local 25–100 Hz peak without distinguishing a fundamental from harmonics. Independent recomputation confirms approximately 21.76 E cycles/s and a dominant 22 Hz E/I peak at the fixed autonomous control; the 43.5 Hz band peak is harmonic.
- **Scientific consequence:** The evidence supports theta-dependent band-envelope coupling and the reported partial failure. It cannot certify completion of an autonomous gamma circuit.
- **Minimum fix:** Preserve iteration 1. Before another iteration, lock a carrier predicate combining E/I cycle timing with spectral evidence, using the existing `braintools.metric.power_spectral_density` path. A common time-constant scaling to 1.25/2.5 ms is a suitable single-change comparison, but requires fresh driven-pair, numerical-convergence, and scan evidence before claiming completion.

### BX-002: Claim–evidence export retains the superseded interpretation

- **Severity:** `minor`
- **Location:** [claim-evidence.md](/workspace/theta_gamma/claim-evidence.md:5); [assess.py](/workspace/theta_gamma/assess.py:72)
- **Problem:** The supplied matrix still presents band predicates as evidence for “E/I gamma circuit,” without the carrier qualification already present in the report and current assessment generator.
- **Scientific consequence:** A standalone evidence consumer receives an interpretation inconsistent with the supported partial outcome.
- **Minimum fix:** Regenerate the corrected matrix and explicitly identify retained validity and strong-predicate fields as results of the original band criterion. Keep the original raw evidence intact. This reporting correction requires no new simulation.

### BX-003: Logistic activation duplicates a documented native operation

- **Severity:** `minor`
- **Location:** [model.py](/workspace/theta_gamma/model.py:31)
- **Problem:** Both derivatives manually implement `1/(1+exp(...))`; BrainState documents the functional `brainstate.nn.sigmoid`.
- **Scientific consequence:** No numerical defect was detected, but the implementation contains avoidable activation machinery.
- **Minimum fix:** Use `brainstate.nn.sigmoid` for the two dimensionless activation arguments, retaining the justified derivative subclass and BrainMass orchestration. Check the existing equation and parity witnesses.

## Unverified assumptions

- Halving both time constants will also preserve sufficient nesting under the fixed 6 Hz drive. Autonomous time scaling does not establish the forced-system outcome; no revised simulation has been supplied.