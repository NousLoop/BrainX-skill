# BrainX study record — iteration 1

Completed before implementation. Coverage: forward-simulation; no training/fitting.

Read full roots: brainx-general-guard, brainx-modeling-loop, BrainMass, BrainState,
BrainUnit; execution/monitoring, mechanism-comparison references. Also studied
BrainX acceleration and diagnostic visualization roots in preparation for later steps.
BrainMass routed references: model library, simulator input/monitor, parameter sweeps,
forward/observation, batch/transform acceleration, visualization/analysis,
Braintools metrics and initializers. BrainState simulation environment; BrainTools
input-current reference. Neural-data visualization reference.

Canonical script traced end to end:
`/codex-home/skills/package-skills/brainmass/references/scripts/wilson-cowan-ei-dynamics.py`.
It constructs E/I Step with explicit cross weights, supplies tuple input, monitors rE/rI,
and plots rate/phase trajectories; its default nonlinearities differ from this specification.
No other script is needed: Jansen–Rit EEG is a different model.

## API and scientific decisions

- Official WC API saved as `docs/wc.txt`: stock WC uses baseline-subtracted sigmoid
  and refractory factor. The locked model uses an unshifted logistic with no refractory
  term. Therefore use the public `drE(rE,rI,ext)` and `drI(rI,rE,ext)` extension contract
  in a tiny subclass, inheriting State initialization, integrator, update and Simulator.
  Do not silently substitute stock equations. Set method=euler and verify simultaneous
  old-State evaluation by a hand-computed one-step witness. dt halving is predeclared.
- Read-only runtime catalogue confirms WilsonCowanStep. No installed source,
  signatures or internals inspected. Official API docs and skill scripts own API knowledge.
- `in_size=25` is the condition axis; `batch_size=3` is the initial-condition axis.
  A fixed initializer array (3,1) broadcasts to (3,25). E and I State are independent
  across both axes. Parameters are static arrays by condition, no learned State or RNG.
- Simulator owns initialization/reset, time loop, transient and sampling. Callable
  input returns (P(t),0); monitors include input and post-update E/I. Returned ts is the
  authority for time. Input at ts−dt is saved alongside each post-update state.
- Units remain on tau, dt, t and frequency; external host analysis/serialization uses
  explicitly named seconds and dimensionless activity. Native batched execution with
  JIT, no raw JAX transformation of State and no Python timestep loop.
- Native metric Welch PSD and single-signal Tort PAC are checked with execution
  witnesses. Primary known-reference PAC needs phase and envelope trajectories,
  cycle surrogates and controlled edge trimming; stock single-signal PAC does not
  provide those. Any SciPy boundary must be justified in API-gap.md before use.
- EEG is a declared linear, dimensionless observation, not a physical forward model;
  no calibrated lead field or dipole data exist. Model E/I and multiple readouts are saved.

## Acceleration design

Native batched State already covers all 75 cases; retain Simulator JIT. Prove scalar
versus batch outputs and final State, reset replay, JIT versus unjitted small-rollout
parity. Report synchronized end-to-end timings without claiming steady cached speedup
if Simulator rebuilds its callable. No performance refactor is warranted.

## Analysis and figure contract frozen before outcomes

Primary gamma band 25–100 Hz, fourth-order zero-phase Butterworth, Hilbert envelope;
theta 4–8 Hz for proxy-estimated phase; trim 0.5 s each edge after 2 s warmup.
Welch nperseg=2000 (0.5 Hz resolution), symmetric Hann. Use known 6 Hz input phase
for primary R and MI; phase zero is drive maximum. Surrogates randomize each complete
theta cycle's reference phase independently (199 draws, fixed seed), preserving
within-cycle amplitude waveform. Null tests fixed phase consistency, not biological causality.
Display original planned pair at g=1,m=0/0.75, first IC, 3–4 s; E/I [0,1],
EEG proxy [−0.5,1.2], envelope [0,0.6], phase curves [0,0.6], PSD 0–120 Hz.
Discrete scan matrices use R [0,1], ΔR [−1,1], band fraction [0,1], peak [25,100];
no interpolation. Three ICs are deterministic sensitivity, no confidence intervals.
Final figures only after review PASS; diagnostic figures before review.

## Initial documentation failures

BeautifulSoup was absent; retrieval switched to Python's standard HTMLParser without
installing anything. Two guessed metric document URLs returned 404; correct URLs
were found from the official index and saved. These were documentation retrieval
failures, not failed simulations. `BrainX` is case-sensitive and is importable;
the initial lower-case brainx presence check was corrected without environment mutation.
