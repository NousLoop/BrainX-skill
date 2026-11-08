# BrainX diagnosis: first-principles LIF regimes

## Evidence studied

Scope: the completed `first-principles-delegated-baseline` only, including its internal failed checks/production and internal reviews; no legacy result, other case, or earlier outer evaluation supplies a proposed skill edit. This is an approved-variant baseline, not a numbered unchanged-original-prompt checkpoint.

- Original/approved prompt fingerprints and harness receipt: empty Docker workspace, no seed, CLI 0.166.0, image `brainx-eval:2026.10.25-py312` / `sha256:845d4814bf308a3fd0f99d9090df922bc809782470954d7bac5284226952d897`, `codex/gpt-6.1-sol`, magpie-local, xhigh; skill hash `57c4ab3a3c4e81947d7de55a9e0ddc68e09cc501a65ca79f1cc651787910878f`.
- Generated specification, first-principles derivation, model.py, experiment.py and frozen source, checks.py, analysis_checks.py, audit_results.py, analysis_spectrum.py, recompute_spectra.py, plot_results.py, freeze_run.py contracts, reports, study/acceleration/API-gap records, all 16 metrics and numerical sensitivity, graph/hash receipts, native PSD parity, both internal independent reviews, final PNG source/render records.
- Same-image outer copy replay: component, analysis, full raw-count audit and all-16 native spectrum checks each exit 0. Three manifests / 107 entries match; all 239 generated files remain unchanged. Main PNG visually inspected.
- Owning guidance: brainx-general-guard; brainpy-state, brainstate, brainevent, brainunit cores; projection-patterns, brain-dynamics-delay-protocol, connectivity, sparse representations, randomness-and-reproducibility, JIT/control-flow references, shared/installed metric references.
- Scientific application examples: deliberately NOT opened. The user's explicit no-paper/no-existing-scientific-code restriction overrides the example-study step in how-to-refine-skill.md. Use elementary derivation, generated code under review, public API contracts and independent execution; do not infer missing scientific knowledge from any existing model solution.
- Public contracts: BrainState random index and generated RandomState class; BrainTools analysis index, power_spectral_density and spectrogram; BrainState Delay; generated Dynamics; baseline archived DeltaProj/Dynamics/Poisson contract receipts. Exact public URLs and retrieval outcomes are in `outer-audit/refinement-contracts/`. Current unversioned class contract is RandomState(seed_or_key=None), while its module overview still shows seed=. The target-release executable probe must arbitrate this inconsistency. Current DeltaProj/LIFRef and guessed CSR generated paths return 404; this is documentation retrieval evidence, not proof of API absence. Do not rewrite those routes or claim a stock-neuron equivalence from these responses.

## Executive diagnosis

Mechanical exit is 0; independent iteration 2 PASS accepts PARTIALLY_SUPPORTED. No evidence supports forcing four requested labels. Two transferable reference gaps are grounded in this evaluation: an invalid RNG constructor keyword copied from guidance, and missing routing to configurable native spectral estimation. Correct these narrowly; do not edit the general guard, introduce model parameters, or codify an undocumented sparse-runtime workaround as a universal API rule.

## Scientific problems

| Severity | Artifact location | Problem | Consequence | Correction |
|---|---|---|---|---|
| Limitation | numerical_sensitivity.json, condition 1 | CV median 0.79795/0.80450/0.80412 brackets frozen 0.8; fine-step seed 11 is 0.92789. Different dt consumes different Poisson realizations. | Fast synchronization has evidence, but irregularity is not robust; cannot separate discretization and realization effects. | Retain inconclusive and continuous evidence. Do not lower threshold or claim convergence. |
| Limitation | condition 3 per-neuron metrics | CV 0.64844–0.66087; fine-step 0.64728, inside frozen (0.5,0.8) gray zone. Typical neuron has about 16 ISIs. | Slow population modulation does not establish the required median irregularity; finite-window uncertainty remains. | Retain inconclusive and eligibility/distribution evidence. |
| Negative result | condition 2 | F1 125–138, c1 0.514–0.540, CV 0.409–0.411, with same qualitative fine-step result. | Both asynchronous and irregular predicates fail, substantially rather than at a boundary. | Retain unsupported within this protocol; do not infer universal impossibility. |
| Limitation | NeuroSpecification.md, model.py | Rest=0, refractory input discard, autapse exclusion, endpoint arrivals, initialization and finite observation are delegated assumptions. | No factorial intervention identifies which assumption causes a regime mismatch. | Keep conditional claims; do not relabel an untested alternative as a repair. |
| Limitation | experiment.assess | F1 and c1 obey F1=c1^2*mean(count); they are not independent evidence. Population modulation is operational synchrony, not a complete microscopic phase measure. | Avoid double-counting evidence or stronger synchronization claims. | Retain definitions and bounded wording; no post-result predicate changes. |
| Resolved implementation failure | failed production and corrected_execution_parity.json | Sparse operator lazy workspace retained a tracer across static-condition compilation. | Initial production could not finish. | Completed agent initialized the public operator eagerly and proved exact first-trajectory/State/RNG parity; preserve failures. No documented universal workaround is inferred. |
| Resolved API failure | checks.log; randomness reference | RandomState(seed=...) raises unexpected-keyword TypeError. | Readiness fails before simulation. | Fix reference constructor syntax against exact class contract and same-image probe. |
| Resolved coverage failure | review iteration 1 / BX-001 | SciPy Welch used without checking a native configurable alternative. | Avoidable native API bypass and review refusal. | Agent's native spectrogram segment mean matches all 16 frozen spectra and labels; teach its selection boundary. |

## Complete BrainX API coverage map

| Generated code or responsibility | Current approach | Owning BrainX API or host boundary | Assessment | Improvement |
|---|---|---|---|---|
| Scientific contract and categorical claims | Locked specification and explicit predicates | Researcher-authorized host protocol | Correct; defaults are assumptions, not recovered paper settings | Keep negative/inconclusive outcomes and distinguish review PASS |
| Network topology | Host without-replacement incoming sampling and sparse conversion | BrainTools conn first; explicit NumPy/SciPy topology boundary documented | Exact indegree, offset-aware autapse exclusion and duplicates verified; do not silently substitute fixed-probability wiring | Retain scoped gap evidence; do not assert all connector releases lack a matching composition |
| Binary communication | BinaryArray @ two scalar-weight CSR matrices | BrainEvent BinaryArray, CSR | Suitable explicit inspectable graph; E/I signs preserved | Check scalar/event parity; no dense recurrent activity |
| Cell dynamics | Small Dynamics subclass, exact leak, threshold/reset/refractory State | BrainPy Dynamics; stock LIFRef only if event-order semantics match | Custom equation is justified by the locked endpoint and refractory contract, not by lack of LIF APIs | Require analytic and endpoint tests; no unsupported stock substitution |
| Delta deposition | DeltaProj before cell update and sum_delta_inputs | BrainPy DeltaProj/Dynamics delta-input contract | Correct instantaneous voltage jumps; no unwanted synaptic filter | Preserve projection-before-target order |
| Recurrent delay | Delay update/retrieve with documented previous-spike convention | BrainState nn.Delay | Offset D-1 is explained and actual target onset tested | Maintain impulse evidence for the actual production path |
| External input | Unit-derived Poisson superposition, multiplicity retained | BrainState RandomState.poisson plus BrainUnit | Suitable exact counts on grid; not Bernoulli occupancy | Repair constructor guidance only; retain input independence checks |
| Initialization | Explicit initial V, empty delays, stable State reset | nn.init_all_states, Module.states, State.value | Entire condition reset includes custom RNG, membrane, refractory and delay State | Preserve registered identities and key parity |
| Physical dimensions | Quantity dynamics, explicit to_decimal serialization | BrainUnit quantities and math | Correct voltage/time/frequency boundaries | No untyped input conversion inside dynamics |
| Simulation time | One for_loop, whole-rollout state-aware jit | BrainState transform.for_loop/jit | No Python timestep loop | Preserve whole-operation compilation |
| Independent trials | Small host loops over seeds/conditions | Host run orchestration with compiled rollout | Appropriate serial memory use; no vmap requirement in this prompt | Do not add batching merely to name an API |
| Static specialization | g/eta static, readiness/full-size parity | BrainState JIT static_argnums | Measured full-size warm speedup ~2.67; initial compilation failure retained | Check second static condition, events, final State and RNG |
| Monitoring | In-loop packbits and lossless events/counts | Host/device serialization boundary; JAX bit packing | Preserves all spikes at lower memory; no scientific loss | Keep padding and count/event audit |
| Event statistics | Per-neuron complete ISIs, counts, eligibility, CV | Host observation definition; BrainTools spike metrics only when exact eligibility/window semantics match | Correct frozen ddof=0 and within-window rules; not a generic replacement solver | Avoid forcing a metric API with different pooling or eligibility |
| Rate and synchrony | Exact 0.1-ms count normalization, fixed F1/c1 | Host frozen count statistics | Correct unsmoothed rates and predicate reductions | Keep units, population normalization and dependence caveat |
| Spectral estimation | BrainTools spectrogram plus mean over segment axis | braintools.analysis.spectral.spectrogram; BrainUnit mean | Correct final implementation; direct PSD defaults do not match all frozen controls | Add a narrow API selection boundary and exact axis/unit contract |
| Offline precision | Separate float64 analysis, float32 neural archive | BrainState/JAX precision environment; host comparison | Appropriate spectral parity; does not establish float32 dynamical convergence | Keep precision claims separate |
| Figures | BrainTools spike_raster; one subplots per figure; basic plots | BrainTools visualization and Matplotlib host presentation | Required per-condition rate/raster, E/I, CV, PSD, numerical plots present | Keep fixed sample/window and declared scales; inspect images |
| Provenance and reporting | JSON/CSV/NPZ, hashes, command/env receipts | Host serialization/reporting | Legitimate boundary; complete artifacts | Do not manufacture package APIs for Markdown/hash work |
| Independent review | Two Codex reviews, REFUSE then PASS | Maintained reviewer MCP workflow | Finding corrected without scientific tuning; both verdicts retained | New evaluation must independently obtain its own verdict |

## Missing, bypassed, or misused BrainX APIs

1. BrainState RandomState is already the correct stream owner. Replace only the erroneous seed= constructor spelling in its reference; retain rng.seed(seed) for reseeding. The public module-overview example conflicts with the generated class signature; link the class directly and validate in BrainState 0.6.0 / BrainX 2026.10.25.
2. BrainTools spectrogram is the missing representative API in the shared metric reference. Use power_spectral_density only when its estimator defaults satisfy the scientific contract. When window/detrending are specified, spectrogram exposes those controls; average PSD axis 1 (segments) for mean-Welch, preserve quantity units, and specify overlap explicitly. This is a variant-selection instruction, not an expanded spectral catalogue.
3. General guard already requires checking alternative routed APIs, exact categorical predicates, frozen thresholds and honest null outcomes. No edit is justified there. Existing delay and transform guidance already covers arrival/order/reset correctness. Do not add a release-sensitive private-workspace claim to BrainEvent guidance.

## Performance and code simplicity

The final product uses sparse active-event communication, compiled stateful time, serial independent trials, stable resets and compressed monitoring. API-readiness and sparse compilation failures cost avoidable iterations. Spectral native reanalysis is inexpensive and reproduces all 16 PSDs, peaks and labels; its final choice is simpler than an unjustified SciPy boundary. Native spectral computation owns segmentation, FFT, scaling and units; NumPy remains at explicit data/observation/serialization boundaries. No evidence justifies scientific rescaling, lower precision, new population batching, or changing the plotting requirements for speed.

## Skill improvements

Patch specification, before edits:

- `brainstate/references/brainstate/randomness-and-reproducibility.md`: change constructor table to RandomState(seed_or_key=None); show positional seeds in the existing single canonical independent-stream example; route the constructor to its exact generated API rather than the inconsistent module overview. Preserve all unrelated stream, transform and checkpoint guidance.
- `braintools-references/braintools-metric.md` first, then its installed BrainCell, BrainPy-State and BrainMass copies: add only spectrogram's configurable-estimator decision boundary, segment-axis mean and quantity PSD unit contract, with an exact public API link. Preserve package-specific and unrelated material.
- No root-skill, general-guard, model, prompt or scientific-threshold changes. No plan.md design change: these remain specialized variants under existing routes. A guard invariant audit is not needed because guard bytes remain unchanged.

## Checks for the next run

Before launch, run focused constructor/reseeding/independent-stream checks and a deterministic signal PSD/window/overlap/unit/segment-axis parity probe inside the identical frozen image. Inventory only changed routes/links; run the repository documentation smoke check separately. Do not inspect external scientific scripts to satisfy the default example-study rule: user restriction wins.

Launch a fresh empty-workspace evaluator with the byte-identical 2865-byte approved prompt, same model/provider/config/image and no seed archive. Use a descriptive name because approved variants cannot be runN. The harness installs the refined skill snapshot into a new isolated Codex home. Require exit 0 and an independent verdict. Compare API selection and failed-check evidence, not equality of scientific outcomes: unspecified scientific defaults are delegated to each fresh agent. Do not transmit baseline seeds, thresholds, findings, reference suggestions or outcomes to it. Do not coach or repair the agent.

After the fresh process exits, write its own full diagnosis, compare against these checks, and only then decide whether another edit is warranted. Preserve original project bytes and both prompt fingerprints. Commit only completed scope; exclude AGENTS.md and unrelated earlier-case work; scan secrets and large files before push.
