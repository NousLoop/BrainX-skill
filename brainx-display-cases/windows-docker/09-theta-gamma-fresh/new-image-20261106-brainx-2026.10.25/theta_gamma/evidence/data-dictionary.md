# Data dictionary

Official accepted candidate run ID: production-02 (acceptance status is in report.md / reviews/gate.json). All NPZ bundles load with np.load(..., allow_pickle=False).

## raw/trajectories.npz
- rE, rI: (12000 time, 3 initial-State/observation-seed lanes, 49 conditions), float64, dimensionless abstract population activity. Model monitor is post-update.
- t_s: (12000,), seconds. First retained t=2.0001 s; stride1 ms; analysis crop3≤t<13 s. The .05 ms refinement starts at2.00005 s, so summary comparisons use respective physical phases, not pointwise equality of chaotic/oscillatory traces.
- depth, relative_gain, absolute_gain: (49,), condition rows are depth-major and gain-minor (index = depth_index×7+gain_index). Absolute gain=1.2×relative gain.
- depth_axis: [0,.1,.2,.4,.6,.8,1]; gain_axis: [.7,.8,.9,1,1.1,1.2,1.3]; grid_shape=[7,7].
- initial: (3,2), E/I initial activity at t=0. All matched depth/gain pairs in a lane begin from the same complete dynamical State; no within-run withdrawal switch.
- final_E, final_I: (3,49), final State at14 s; not the last decimated sample.
- input_E_left, input_E_monitor: (12000,49), dimensionless E input evaluated respectively at monitor time minus dt and at monitor time. Q=0. Waveform shared across lanes.
- elapsed_s: simulator call wall time including compilation and synchronized execution, not a warm-runtime benchmark.

## raw/observations.npz
- latent, eeg, eonly, leakage: (12000,3,49), a.u. latent=E−.5I centered by each full post-burn mean; eeg adds theta+noise; eonly uses centered E+theta+noise; leakage is theta+noise only, broadcast across conditions.
- noise: (12000,3,1), paired between all conditions in a lane, independent seeds11/23/37 between lanes; SD=.02.
- theta: (12000,1,1), .15 cos(2π6t), retained in the proxy under both m=0 and m>0.

## metrics/analysis.npz
- signal_names: [E,latent,eeg,eonly,leakage]. All signal-axis fields use this order.
- envelope, band: (12000,3,49,5), BrainTools zero-phase Butterworth order4, band25–90Hz, then Hilbert magnitude; envelope and filtered signal retained before interior crop.
- R, MI, preferred_phase, gamma_rms, null95: (3,49,5). R and MI dimensionless; preferred_phase radians (not meaningful when R≈0 or multimodal profile); RMS in the relevant activity/proxy units.
- profile: (18 bins,3,49,5), mean amplitude in equal phase bins [−π,π); bin_centers radians; bin_counts sample count per bin across the fixed10s analysis window.
- null_R: (200 surrogates,3,49,5), exact independent circular envelope shifts within each of60 cycles; same sampled shifts paired across signals and conditions.
- null_rotations: (200,60), integer sample shifts, sampled uniformly from each cycle's166 or167 original samples; cycle_counts (60,). The surrogate destroys cross-cycle phase consistency; it is not population inference and is not a global time shift.
- window_mask: (12000,), fixed3≤t<13s. Theta phase=2π·6·t_s from known external clock, never recovered from mixed EEG.
- frequency_Hz: Welch frequencies, nperseg2000 and noverlap1000 at1ms recording; psd_E,psd_eeg: (frequency,3,49), squared activity or a.u. per Hz. No condition-specific PSD normalization.
- gamma_peak_Hz: (3,49), strongest bin within25–90Hz, undefined (NaN) below E RMS=.005. A gamma-band peak alone does not establish a baseline gamma fundamental; see broad_peak_Hz below.

## metrics/decision.npz
- broad_peak_Hz: (3,49), dominant E PSD bin in1–150Hz, retained even when near stationary (the frequency must not be scientifically interpreted below the RMS floor).
- baseline_valid: (3,7 gains), independently checks each m=0 control: E gamma RMS>.005 and broad dominant frequency in25–90Hz.
- delta_R: (3,49), R_eeg minus same-lane, same-gain m=0 R.
- nested: (3,49), exact full predicate baseline_valid AND E_gamma_RMS>.005 AND delta_R>.05 AND R_eeg>null95_eeg. False at an invalid baseline means not eligible, not a confirmed absence of possible driven PAC.

## Refinement, calibration and inspection
- raw/refinement.npz and metrics/refinement.npz: same schemas without stored sweep-axis columns; initial lane0; depth-major m=[0,.6,1] and all7 gains; dt=.05ms. Ordering also explicitly saved in metrics/convergence.npz.
- metrics/convergence.npz: 21 ordered conditions, coarse_indices, depth, gain, gamma_relative_error, frequency_error_Hz, R_abs_error, relevant (coarse E RMS>.005), passed. No scientific claim is made for below-floor frequencies.
- calibration-01: raw E/I for18 baseline candidates; calibration.npz stores ordered drive/gain columns, SD stability ratio, gamma RMS, frequency, eligibility mask and PSD. selection.json fixes the subsequent base regime.
- evidence/sweep.csv: all147 lane×condition rows, continuous evidence, eligibility and final predicate. NaN means a frequency is undefined by the amplitude floor; it is not a missing run.
- figures/*_plotted_values.npz: exact displayed lane0 matrices and display indices for figure integrity.
