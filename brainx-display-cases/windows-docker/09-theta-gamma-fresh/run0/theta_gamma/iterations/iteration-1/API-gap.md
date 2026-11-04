# BrainTools API gaps and explicit boundaries

- Operation and required capability: phase/envelope time series for external-reference
  PAC, per-cycle surrogates, edge trimming and matching filter sensitivity.
- BrainTools APIs checked: metric.phase_amplitude_coupling, metric.theta_gamma_coupling,
  metric.power_spectral_density; official analysis.spectral.bandpass and analytic_signal.
- Observed limitation: this environment (braintools 0.3.0) has no analysis namespace;
  exact execution failures are in docs/api_execution_checks.json. Native metric PAC
  works, but returns MI/phase-bin centers/mean amplitudes only, with phase derived from
  the same signal. It does not expose the trajectories or accept external reference phase.
- Why another routed API does not satisfy contract: theta_gamma_coupling delegates
  single-signal PAC and cannot supply external-reference phase or the time series.
- Smallest external boundary: host SciPy butter/sosfiltfilt/hilbert after serialization
  boundary, preserving time axis 0, at measured sample dt. Keep native BrainTools
  PSD and native single-signal PAC (secondary metric) rather than replacing those.
- Parity evidence: focused synthetic 6/60 Hz AM tests, constant-amplitude and
  linear-mixture nulls, native MI comparison with periodic analytic filtering,
  known analytic R=depth/2. Saved in checks/verification.json.

## Prescribed input

Sinusoidal has no continuous phase parameter (docs/braintools.input.Sinusoidal.txt).
TimeShifted operates on generated arrays and shifts boundaries on a sample grid;
6 Hz quarter period is not an integer dt. The smallest exact implementation of
the locked cosine is a unit-aware callable accepted by Simulator: cos(2π f t).
This expresses the prescribed scientific input, not a new input framework.

## Observation and statistics

The unitless linear EEG proxy, known-reference R/18-bin MI and cycle-phase null
are declared study-specific observations/statistics. Host NumPy owns these offline
reductions and serialization. No physical lead field is claimed. All quantities
crossing this boundary are explicitly dimensionless or converted to seconds.
