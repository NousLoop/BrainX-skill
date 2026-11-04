# BrainX diagnosis: fresh theta–gamma E/I circuit

## Evidence studied

This is the diagnosis of the new `09-theta-gamma-fresh/run0` only. No earlier
theta–gamma case, generated code, figure, diagnosis or expected result was used
to construct the prompt, baseline, review standard or this diagnosis.

Repository policy: `AGENTS.md`, `plan.md`, `how-to-refine-skill.md`.
Routing and existing guidance: general guard, modeling loop, BrainMass,
BrainState, BrainUnit and visualization roots; BrainMass model library,
Simulator input/monitor, parameter sweeps, forward observation and analysis
references; BrainState activation library; the generated study records and
API-gap record. These skills are refinement targets, not independent proof.

Executable composition standards studied line by line:

- `skills/package-skills/brainmass/references/scripts/wilson-cowan-ei-dynamics.py`:
  construct a Step with E/I cross weights, supply tuple inputs to Simulator,
  initialize and monitor rE/rI, retain timestamps, plot trajectories. Transfer
  its lifecycle and composition, not its parameters or assumed oscillation band.
- `skills/package-skills/brainmass/references/scripts/jansen-rit-eeg-proxy.py`:
  distinguish model-specific observable M from latent activity and record its
  units/sampling before PSD. Do not transfer its alpha-generating dynamics or
  voltage interpretation into this dimensionless WC proxy.

Authoritative contracts were retrieved independently into
`outer-audit/official-api/`, with URLs and HTML hashes in `receipt.json`:
WilsonCowanStep constructor/derivative extension, Simulator.run,
BrainState activation/sigmoid and environment, BrainTools Constant and
Sinusoidal, spectral PSD/PAC/filter/analytic-signal pages, BrainMass forward
and visualization pages, and BrainUnit Quantity. The native 0.3 metric
namespace and newer documentation namespace are distinguished by the saved
API execution witnesses, not inferred from installed source. Initial web-tool
fetch failures were resolved by direct official-page retrieval; no installed
source, signatures or docstrings were used as modeling knowledge.

Inspected generated responsibilities: all nine root Python files, both
specifications and study records, both raw reviews and requests, addressed
findings, memory/checkpoints, reports/claim matrices/figure manifests,
acceleration records, API failures and verification logs, six run configs,
source/manifests, raw and derived NPZ arrays, metric JSON/CSV, execution status,
runtime/environment evidence and the outer event stream. Iteration-1 snapshots
and source differences remain part of this single baseline's history.

Execution evidence: `outer-audit.py` runs with the exact pinned image ID,
network disabled, evidence mounted read-only, and temporary copied sources.
`outer-audit/reproduction.json` and `.log` record PASS: all six run manifests
verify; focused verification passes; production and convergence raw arrays
replay exactly; 300+24 metric rows and 18 derived arrays per run match exactly.
This is a verification replay, not another numbered refinement checkpoint.

Visual inspection: opened all three final PNGs. Traces show a fast autonomous
rhythm and theta-locked fast clusters; nesting panels agree with saved spectra,
bins and null values; the discrete scan shows invalid cells and no interpolation.
Axes, legends, units and fixed comparison scales are readable and unclipped.
The generated delivery receipt separately preserves PDF rendering evidence.

## Executive diagnosis

The completed baseline satisfies the authorized illustrative task after one
internal scientific refusal. The original ~22 Hz carrier and its gamma-band
harmonic were correctly retained as a partial failure. Review forced explicit
cycle/spectrum carrier checks, native sigmoid and consistent claim exports.
The corrected run has E/I cycle frequency 43.5268 Hz and a 43.5 Hz dominant
autonomous spectral peak. Fixed-pair proxy R changes from 0.000271679 to
0.501624503; maximum dt-halving difference is 0.001347. The gain/depth scan
retains unfavorable and invalid settings. No unique biological mechanism or
physical EEG correspondence is established.

Decision: **no-edit**. All observed failures are already covered by existing
decision rules; the modeling/review loop detected and resolved the material
ones. No final implementation defect or missing transferable instruction
justifies expanding the skills. Do not manufacture a new guard rule from this
case's parameter choices or duplicate the current validation rules.

## Scientific problems

| Severity | Artifact location | Problem | Consequence | Correction |
|---|---|---|---|---|
| Major, resolved | iteration-1 analysis and carrier audit; review BX-001 | A local gamma-band peak accepted a ~22 Hz oscillator's harmonic | Initial run did not establish gamma carrier | Preserved initial data; revision 2 locks cycle timing plus dominant PSD and harmonic negative control; reruns full matched protocol |
| Minor, resolved | original claim matrix; BX-002 | Matrix lagged behind the report's partial-failure qualification | Inconsistent standalone claim | Revised generator and matrix explicitly distinguish legacy band validity and actual carrier evidence |
| Validation witness, resolved/disclosed | failure-log and verification logs | Initial absolute Euler error cutoff and incompatible native-PAC synthetic witness failed | Those witnesses could not validate the intended claim | Independent solver demonstrates first-order convergence; compatible phase-bearing synthetic signal used; original failures retained; production tolerances unchanged |
| Minor documentation, retained | NeuroSpecification data contract | Declares time × condition × IC, while code/raw/manifests correctly use time × IC × condition | A consumer reading this line alone could swap axes | Use raw shape, model docstring and figure manifest as operative axis contract; correct this line in any future modeling continuation, not in preserved baseline |
| Minor wording, retained | result-assessment.md | “No post-outcome tuning” is overbroad beside explicitly disclosed timescale calibration | Ambiguous standalone wording | Read with the next paragraph and final report: iteration 2 is outcome-calibrated, then frozen; future regeneration should say “no further tuning after revision-2 freeze” |
| Minor provenance, retained | initial approval date in specification | Uses 2026-11-03 while client task date is 2026-11-04 Asia/Shanghai | Date labeling inconsistency only | Current case records use client date; preserve raw agent artifact without editing |

## Complete BrainX API coverage map

| Generated code or responsibility | Current approach | Owning BrainX API or host boundary | Assessment | Improvement |
|---|---|---|---|---|
| Model family/scale | two aggregate E/I activity States | BrainMass WilsonCowanStep | Correct single neural-mass scale; no unnecessary point neurons | None |
| Custom nonlinearity | tiny drE/drI overrides | documented derivative extension; brainstate.nn.sigmoid | Preserves locked unshifted/no-refractory equations; native solver/lifecycle retained | Initial manual logistic resolved |
| Parameters and units | condition arrays; tau/dt in ms; f in Hz | BrainUnit math/Quantity | Correct dimensionless activation and inverse-time derivatives | None |
| Initial conditions | Constant arrays broadcast across conditions | braintools.init.Constant; Simulator batch_size | Separate IC and condition axes; exact scalar/batch parity | None |
| Input | unit-aware cosine callable | Simulator inputs(i,t); BrainUnit cos | Exact prescribed scientific drive; input API comparison documented | None; no input framework needed |
| Actual input witness | applied_P ShortTermState | registered State plus named monitor | Correctly records input used in update | Initial attempted environment-time monitor resolved |
| Time, initialization, reset, JIT | Simulator.run | highest-level owning orchestrator | No rebuilt time loop; same-object reset and JIT parity verified | None |
| Sweep execution | in_size=25; batch_size=3 | native batched State and parameter broadcasting | All 75 simulations execute together; no Python timestep loop or superfluous vmap | None |
| Monitor sampling | E/I/P and returned ts; input_t=ts−dt | Simulator named monitors/transient/sample_every | Post-update timestamps and applied-input phase differ deliberately | None |
| EEG proxy | E−0.5I plus fixed theta mixture; other linear views | explicit host observation boundary | No physical lead field/dipole input exists; no claim requiring EEGLeadFieldModel | None |
| PSD | native Welch on sampled signal | braintools.metric.power_spectral_density | dt in seconds/Quantity, channel axis and 0.5 Hz resolution correct | None |
| Native single-signal PAC | supplementary native MI | braintools.metric.phase_amplitude_coupling | Retained and distinguished from external-reference R | None |
| Envelope/filter phase | host SciPy butter/sosfiltfilt/Hilbert | verified analysis-namespace dependency gap | Time-major filtering and edge removal; synthetic/native parity saved | None; do not install a newer ecosystem mid-baseline |
| Known-reference R/MI/bins | explicit offline statistics | host NumPy boundary | Native same-signal PAC cannot accept external reference or expose needed trajectories | None |
| Cycle surrogate | seeded NumPy per-cycle rotations | host offline null-model statistic | Tests deterministic phase consistency; not animal inference or unique causality | None |
| Carrier verification | native PSD plus host peak/interval statistics | BrainTools PSD + legitimate observation statistics | Joint frequency/rate/CV/amplitude checks; harmonic negative control | None |
| Controls and validity | same lane path, saved continuous evidence | native batched Simulator plus host predicates | Every gain/IC has m=0; high R cannot override invalid gamma | None |
| Numerical validation | one-step equation, adaptive reference, dt half | public BrainMass model execution; SciPy only independent test oracle | Scientific metrics certified at fixed pair; rest of grid explicitly descriptive | None |
| Performance | fused native batch; CPU float64 | Simulator JIT and BrainState environment | No unjustified optimization; exact parity; compile-inclusive timing labeled correctly | None |
| Execution/provenance | immutable snapshots, configs, SHA256, timeout/status | host orchestration, file and process boundary | Appropriate; package metadata used for run identity, not modeling knowledge | None |
| Acceptance and claims | deterministic assess.py; two independent reviews | host logic + configured Codex MCP | REFUSE→restudy→new experiment→PASS recorded | Retain wording caveats above |
| Figures | BrainMass timeseries + simple subplots/host curves | brainmass.viz then high-level Matplotlib | One subplots per figure; preserved diagnostic/final distinction and source manifest | None |
| Serialization/report | NPZ/CSV/JSON, Chinese Markdown | legitimate host boundary | No invented BrainX API for reporting or hashes | None |

## Missing, bypassed, or misused BrainX APIs

The only confirmed avoidable API bypass was the original logistic expression;
revision 2 uses native `brainstate.nn.sigmoid`. The existing general guard's
high-level API rule and BrainState's activation-library route already cover it.

The analysis namespace absence is a frozen-release capability limitation,
explicitly documented and tested. Native metric PSD and PAC still run. A physical
EEG forward model, Fitter, point-neuron package, extra vmap or generic custom
solver would add semantics the task does not require. Host statistics,
serialization and prescribed dimensionless observation remain legitimate.

## Performance and code simplicity

The scientific core is a short subclass and one Simulator call. State is native
batched, units survive to explicit host conversion, and no raw JAX transform wraps
State. Full sampled histories are necessary for the requested proxy/phase audit.
The 5×5×3 grid fits CPU memory; the recorded 432 MB intermediate estimate and
compile-inclusive timing are candid. Offline loops iterate metric columns, not
simulation timesteps. No speedup is claimed without a stable cached benchmark.

Nine source files and duplicated immutable snapshots are more extensive than a
single demonstration script, but serve the explicitly required experiment,
verification, review, failure preservation and report contracts. Do not turn
that case packaging into a new generic framework or extra skill requirement.

## Skill improvements

**no-edit; edit specification: none.**

| Observed issue | Existing authoritative instruction | Why no skill edit |
|---|---|---|
| Harmonic mistaken for requested carrier | guard “Validate scientific claims”: validate baseline/mechanism before calibration; apply each claim's full predicate; freeze then disclose calibration | Final loop independently detects and fixes the precise failed predicate; parameter/band-specific recipe stays in this case |
| Manual logistic | guard “Prefer high-level BrainX APIs”; BrainState activation-library route | Already directs the correct native operation |
| Claim matrix inconsistency | modeling-loop step 5 packet, diagnostic closure and step 6 report; guard claim/observable rules | A stale generated artifact, not missing instruction |
| Failed validation witnesses | guard scientific validation; loop implementation checks and REFUSE restudy | Failures retained, diagnosed and rerun without hiding changed assumptions |
| Axis/date/wording slips | BrainMass simulator reference, visualization data contract, current client-time instructions | Existing requirements are explicit; duplicating them would not improve routing or implementation |

No general-guard edit was attempted, so no invariant rewrite audit is needed.
No package root, reference, example, installed skill or plan scope changed.

## Checks for the next run

No next numbered run is warranted. `how-to-refine-skill.md` forbids `runN+1`
with the same snapshot. The user explicitly permits no-edit when no transferable
gap exists; therefore leave `run1/` absent. The read-only verification replay is
clearly labeled as such and makes no skill-improvement claim.

If a later task exposes a new gap, require a new edit specification from its
latest numbered run, validate and install the actual patch, then run the exact
634-byte prompt with SHA256
`c3ad8eb63e3c056e581717baf55f8c35f2f6ba690af75767201a57f934b58246`
under the same frozen environment. Check autonomous carrier versus harmonic,
matched removal, proxy controls, every scan lane, dt-half parity, native APIs,
raw evidence retention, consistent axis/claim text, review and visual inspection.
