# BrainX study record — iteration 1

Completed before implementation. Active coverage: forward simulation; no training/fitting.

Read the complete general guard, modeling loop, BrainMass, BrainUnit, BrainState, acceleration and visualization skills, plus mechanism-comparison, paired-perturbation, simulation-environment, model library, simulator input/monitor, parameter sweeps, batch/transform acceleration, forward observation, analysis/visualization, initializer, run/monitor experiment and neural/statistical visualization references. Traced Wilson–Cowan and Jansen–Rit example scripts from construction through simulation and plots.

## Design and API decisions
- `brainmass.list_models()` checks WilsonCowanStep availability as explicitly permitted by the BrainMass skill. No installed code, signatures, object internals or docstrings are inspected.
- `brainmass.WilsonCowanStep(in_size=N, tau_E=..., tau_I=..., wEE=..., wEI=..., wIE=..., wII=..., rE_init=..., rI_init=..., method='rk4')` owns dynamics. Simulator owns initialization, environment, State-aware compiled time loop, transient and point sampling. Parameter vectors broadcast over condition axis; `batch_size=3` owns sensitivity lanes.
- Official generated WilsonCowanStep API was retrieved into `evidence/wilson_cowan_official.txt`. Its equations include refractory factors and offset sigmoid omitted in the short example narrative:
  tauE dE/dt = −E + (1−r E) F_E(g·16E−g·12I+P), tauI dI/dt = −I + (1−r I) F_I(g·15E−g·3I+Q),
  F_j(z)=sigmoid[a_j(z−theta_j)]−sigmoid(−a_j theta_j).
  Fix documented defaults aE=1.2, thetaE=2.8, aI=1, thetaI=4, r=1 explicitly. Offset sigmoids permit small negative activity: derive invariant bounds from F_min=−c and F_max=1−c, r_state∈[−c/(1−c),(1−c)/(2−c)]. Such values are abstract activity, not physical negative firing rates. Check these rather than impose a mismatched [0,1] bound.
- Time input is the scientifically prescribed equation evaluated on Simulator's unit-aware t using `u.math.cos(2π·6*u.Hz*t)`; no custom input generator, time loop or solver. Input time is left endpoint and monitor time is post-update; save both input-at-left-edge and input-at-monitor time, and the dt offset.
- `braintools.analysis.spectral.bandpass`, `analytic_signal`, `power_spectral_density` cover filtering, envelopes and Welch PSD. Their official pages are saved under evidence. No SciPy substitute required. Host NumPy handles serialization, observation noise, binned known-drive-phase statistics and cycle rotations.
- Stock `phase_amplitude_coupling` estimates phase internally from one mixed signal and cannot accept prescribed drive phase. For the specification's ground-truth phase contract implement the small host R, 18-bin and KL reductions after BrainTools envelope extraction; see `evidence/api-gap.md`.
- EEG is an explicitly synthetic observation, not a lead-field model. The forward reference confirms a physical EEGLeadFieldModel requires calibrated dipoles/lead fields absent here. Do not add false voltage units or Jansen–Rit biology.
- Native batch/condition execution avoids custom stateful transforms; acceleration will compare JIT vs non-JIT and vector vs scalar lanes, including final State. Retain the high-level runner if parity passes.
- Plot trajectories with brainmass.viz.plot_timeseries; use simple Matplotlib composition for mixed phase profiles and nonuniform parameter grids. All figures have exactly one subplots call, fixed cases/scales, PNG+PDF exports.

## Study failures preserved
- First official-page extraction attempted unavailable bs4; replaced only the HTML-text extraction with Python regex, no dependency mutation.
- A guessed generated sinusoidal-input documentation URL returned HTTP 404; no guessed API was used. Callback is the specified model input equation.
- Lowercase brainx absence was a case mismatch: uppercase `BrainX` is importable. No installation necessary.

## Pre-experiment execution compatibility correction
Numerical public-API derivative tests exposed the cross-weight keyword reversal documented in `evidence/api-direction-discrepancy.md`. Constructor mapping is adapted to preserve the locked scientific weights, and the full analytic derivatives are tested. No scientific parameter was changed and no modulation outcome was available.
