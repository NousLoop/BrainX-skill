# NeuroSpecification

- Status: draft
- Clarification gate: pending
- Researcher approval: pending decision

## Researcher request
- Brain-modeling question or behavior: Create a resting cortical circuit that produces an alpha-like rhythm, then weaken inhibition and determine how the simulated EEG changes.
- Requested model, experiment, or comparison: An interacting cortical-population model with baseline and weakened-inhibition conditions, including independent initial conditions.
- Execution mode: forward-simulation
- Required outputs: BrainMass population dynamics and interpretable simulated-EEG proxy; BrainState `for_loop` evolution and stateful `vmap` comparison over inhibition strengths and initial conditions; BrainUnit-consistent physical quantities; numerical metrics, raw results, and figures.
- Constraints: Keep claims at the aggregate cortical-population scale. Treat the EEG output as a model-derived proxy, not a biophysical scalp-EEG forward solution, unless the design is explicitly expanded.
- Open decisions and handling: Pending researcher choice of the inhibitory-strength intervention. Proposed default is a sweep retaining 100%, 75%, 50%, and 25% of baseline inhibitory coupling. Later setup requires an explicit device choice and installation confirmation because BrainX is absent. Other computational settings will be selected and justified after this parent decision, subject to the locked acceptance boundary.

## Inspected data contract
- Data sources and inspected contents: No empirical data or prior project artifacts were supplied; `/workspace` was empty at project start.
- Shapes, axes, sampling/time base, and physical units: To be fixed after the clarification gate; simulation time will use physical time units and observables will retain explicit rate/signal units where applicable.
- Required preprocessing and the subset used to fit each transform: None; this is a forward simulation with no fitting.
- Mapping from data to model inputs, targets, and observables: Resting external drive will be a model input; excitatory and inhibitory population activity will define an explicitly documented population EEG proxy.
- Known data limitations or unresolved mismatches: No empirical calibration target is available. Alpha likeness and inhibition effects therefore require predeclared simulation metrics and sensitivity checks.
- Conditional interpretations of unanswered experimental questions: Results will be interpreted as conditional behavior of a phenomenological cortical neural-mass model, not evidence that one biological alpha generator or clinical disinhibition mechanism is uniquely identified.

## Acceptance boundary
- Evidence required for success, failure, or an inconclusive result: Baseline simulations must show a stable dominant spectral peak in the conventional alpha band with reproducibility across initial conditions; weakened-inhibition conditions must be compared using the same drive, integration settings, observation mapping, analysis window, and initial-condition ensemble, with changes quantified in peak frequency, alpha-band power, total variance/RMS, and population state stability.
- Required baselines and controls: Baseline inhibition; matched external drive; multiple initial conditions; identical time grid and transient removal; solver/time-step sensitivity; preservation of raw population states alongside the EEG proxy; and an inhibition-strength dose response once approved.
- Invalid-result conditions: Unit inconsistency; unstable or non-finite trajectories; alpha classification driven only by transients; mismatched controls; an observation mapping changed between conditions; or claims based solely on a selected favorable initial condition.
- Allowed claims and explicit non-claims: The study may establish conditional sufficiency of an aggregate E-I cortical circuit for alpha-like activity and quantify its response to a specified inhibition reduction. It may not identify a unique biological alpha generator, equate the proxy with measured scalp EEG, or generalize to disease or pharmacology without additional evidence.
- Model/comparison rationale and decisive assumption checks: Causal comparison is `reduced inhibitory coupling -> altered E-I population dynamics -> changed population EEG proxy`. Decisive checks are intervention magnitude, initial-condition dependence, observation mapping, and numerical resolution. Only inhibitory coupling will differ in the matched main comparison.
