# BrainX study record — iteration 1

## Scope and package selection

- Represented biological scale: one aggregate cortical column with interacting pyramidal, excitatory-interneuron, and inhibitory-interneuron populations. The owning modeling package is BrainMass; no point neurons, cellular channels, event connectivity, training, or fitting are represented.
- Supporting infrastructure: BrainState owns mutable dynamical State, scoped time, `for_loop`, `vmap`, and optional whole-rollout JIT. BrainUnit owns time, voltage, gain, and rate quantities and explicit conversion at the numeric-analysis boundary. BrainTools owns Welch power spectral density through the BrainMass-routed analysis API.
- Public catalogue check: `brainmass.list_models()` reports `JansenRitStep` as a six-State physiological model for “EEG generation, alpha rhythms” and `WilsonCowanStep` as a two-State E-I firing-rate model. This supports the corrected locked selection of `JansenRitStep`.
- Active optional coverage: none (`forward-simulation`).

## Sources studied completely or end to end

- `/codex-home/skills/brainx-general-guard/SKILL.md`
- `/codex-home/skills/brainx-modeling-loop/SKILL.md`
- `/codex-home/skills/brainx-modeling-loop/references/mechanism-comparison.md`
- `/codex-home/skills/package-skills/brainmass/SKILL.md`
- BrainMass references: `modellibrary.md`, `simulator-input-monitor-api.md`, `parameter-sweeps-and-regime-analysis.md`, `batch-transform-acceleration.md`, `forward-observation-api.md`, and `visualization-analysis-api.md`.
- BrainMass canonical scripts: `scripts/jansen-rit-eeg-proxy.py` and, for the rejected cheaper alternative, `scripts/wilson-cowan-ei-dynamics.py`.
- `/codex-home/skills/package-skills/brainstate/SKILL.md`
- BrainState references: `simulation-environment.md`, `collective_model_operations.md`, `paired-perturbation-execution.md`, `brainstate/transformation-vmap-expansion.md`, and `brainstate/brainstate-control-flow-patterns.md`.
- `/codex-home/skills/package-skills/brainunit/SKILL.md`
- BrainUnit references: `quantity-inspection-and-conversion.md` and `array-mechanics.md`.

## Reconciled API decisions

1. Model and observable: instantiate `brainmass.JansenRitStep(in_size=1, Ai=...)`. Drive it each step with the canonical input tuple `(0 mV, 220 Hz, 0 mV)`. Monitor the public `eeg()` result and the documented `M`, `E`, and `I` States where available. Treat `eeg()`/`M` as a cortical source proxy in mV, not a calibrated scalp sensor voltage; no lead field is justified without source geometry and a calibrated matrix.
2. Intervention: baseline `Ai = 22 mV`; mapped values are `[22, 16.5, 11, 5.5] mV`, exactly the requested retention fractions. Every other constructor default and input is shared. This changes inhibitory postsynaptic gain, not a uniquely identified presynaptic, receptor, or cell-count mechanism.
3. Initialization: call `brainstate.nn.init_all_states()` under the run's `dt` context, replace every dynamical `HiddenState` with a unit-preserving zero, then set public `M` to one of the eight locked mV values. The same initial value is repeated under all four `Ai` values. Inspect State paths, shapes, dtypes, and units during the construction gate; do not use path/rank coincidences to choose mapped State roles.
4. Time evolution: define one complete `run_lane(Ai, initial_M, dt, n_steps)`; inside it, use a single `brainstate.transform.for_loop(step, indices)`. Each body sets scoped `i` and post-update time, calls the model once, and returns fixed-structure unit-aware observables. No Python timestep loop and no explicit carry are needed because the model States carry the recurrence.
5. Vectorization: flatten condition-major coordinates with inhibition repeated over eight initial conditions and initial conditions tiled over four inhibition levels. Construct the model inside `run_lane`, then use `brainstate.transform.vmap(run_lane)` over both coordinate arrays, matching the BrainMass parameter-sweep contract. Reshape the fixed output from `[lane, time, 1]` to the locked `[time, condition, initial_condition]` layout. This maps the complete independent stateful simulation, rather than only input construction or host analysis.
6. Compilation: retain one stable mapped rollout callable. Step 2 first proves an unjitted short rollout. Step 3 may wrap the whole mapped rollout with `brainstate.transform.jit`, measure first-call and warmed execution separately, and compare all outputs against the unjitted baseline. JIT is not required for scientific validity.
7. Units: keep `dt`, duration, transient, `Ai`, initial `M`, all model States, drive, and recorded time unit-bearing. At the self-describing NPZ/metric boundary, call `to_decimal(u.mV)` for EEG/potentials and `to_decimal(u.second)` for time; record units as named fields. Never use a raw mantissa as an implicit conversion.
8. Spectrum: after locked transient removal and 10× decimation, flatten condition/initial-condition lanes as channels and call `braintools.metric.power_spectral_density` with `dt=1 ms`, `nperseg=2000`, and `noverlap=1000`. The metric returns Hz frequencies and one-sided PSD. Host NumPy is limited to deterministic reductions, serialization, manifests, and paired summaries.
9. Peak validity: a lane below 0.01 mV retained RMS has undefined peak frequency; this amplitude floor was fixed before any result inspection. Search dominant frequency only within 4–30 Hz. Compute alpha fraction as integrated 8–13 Hz power divided by integrated 4–30 Hz power. Keep every per-lane continuous metric.
10. Controls: run the same lane path for the full 4×8 mapped experiment. Separately rerun the first initial condition at 0.05 ms for 100% and 25% inhibition, compare it with the corresponding production lane, verify unit/shape/finite/magnitude invariants, and check `eeg() == E - I` when the public component States are present.

## Implementation design

- `alpha_rhythm.py`: constants and unit-aware construction; short/sweep/half-step rollout entry points; explicit analysis boundary; BrainTools Welch metrics; deterministic acceptance assessment; NPZ/JSON artifact writing; provenance fields.
- `test_alpha_rhythm.py`: construction and unit checks, one-step State write-back, short mapped shape/paired-coordinate checks, EEG component identity, invalid unit rejection, spectral helper behavior, and artifact round trip.
- `run_experiment.py`: immutable run-directory creation, frozen configuration serialization, smoke gate, production rollout, half-step controls, metrics/assessment, logs, and artifact manifest.
- Scientific outputs are full retained/raw EEG and component trajectories where storage is modest, per-lane metrics, condition summaries, convergence evidence, and a claim-evidence matrix. Plotting is deferred until diagnostic closure or accepted-result step 6.

## Known boundaries

- `Simulator.run()` is the preferred ordinary BrainMass runner, but this task explicitly requires visible BrainState `for_loop` and `vmap` over both inhibition and initial conditions. The custom rollout keeps model construction and equations in BrainMass while using the documented custom-loop/parameter-sweep path.
- No empirical fitting, stochastic uncertainty, thalamic generator, cortical geometry, lead field, or sensor calibration is included. Initial-condition dispersion is a deterministic attractor-sensitivity check, not a population confidence interval.
- The 100/75/50/25% points are discrete tested levels. Do not describe an interval boundary or interpolate a continuous dose response.
