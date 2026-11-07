# BrainTools API gap
- Operation and required capability: PAC from externally known theta phase and a prefiltered gamma envelope, with a fixed interior crop; within-cycle independent rotations.
- BrainTools APIs checked: spectral.phase_amplitude_coupling(lfp,dt,phase_freq_range,amplitude_freq_range,n_bins), theta_gamma_coupling(lfp,dt), bandpass, analytic_signal, power_spectral_density. Official extracted documentation retained.
- Observed limitation: the stock PAC routine accepts a single mixed signal, internally derives both bands, and has no external phase or already extracted envelope argument. Generic phase_randomize does not implement independent rotations per prescribed theta cycle.
- Why another routed API does not satisfy the contract: theta_gamma_coupling has the same single-signal phase assumption and fixed bands. Filter/envelope/PSD APIs do meet their contracts and are used.
- Smallest external boundary: host-side descriptive R and KL statistics, binning and rotations on serialized unitless arrays; circuit remains BrainMass-native.
- Unit, State, shape, numerical parity evidence: outputs dimensionless, inputs time-major with saved seconds; no State crossed. Analytic amplitude-modulated and constant-amplitude test controls plus filter parity against SciPy in tests (validation only, not implementation).
