"""Offline analysis; SciPy boundary justified in API-gap.md."""
import braintools
import brainunit as u
import numpy as np
import scipy.signal


def analytic_band(x, dt_s, band):
    sos = scipy.signal.butter(4, band, btype="bandpass", fs=1/dt_s, output="sos")
    filtered = scipy.signal.sosfiltfilt(sos, x, axis=0)
    return scipy.signal.hilbert(filtered, axis=0)


def reference_pac(amplitude, phase, n_bins=18):
    """Known-reference mean vector and Tort MI; no phase estimated from carrier."""
    phase = (phase + np.pi) % (2*np.pi) - np.pi
    counts, _ = np.histogram(phase, bins=n_bins, range=(-np.pi, np.pi))
    sums, edges = np.histogram(phase, bins=n_bins, range=(-np.pi, np.pi), weights=amplitude)
    means = sums / np.maximum(counts, 1)
    probability = means / max(means.sum(), 1e-300)
    positive = probability > 0
    mi = np.sum(probability[positive] * np.log(n_bins*probability[positive])) / np.log(n_bins)
    vector = np.mean(amplitude * np.exp(1j*phase)) / max(np.mean(amplitude), 1e-300)
    return float(abs(vector)), float(mi), float(np.angle(vector)), means, counts


def carrier_features(x, t, freqs, power, config):
    """Cycle timing plus strongest native-Welch peak; excludes harmonic-only gamma."""
    dt=float(np.median(np.diff(t)))
    peaks=scipy.signal.find_peaks(x, prominence=config["carrier_prominence"],
        distance=max(1,round(config["carrier_min_distance_s"]/dt)))[0]
    intervals=np.diff(t[peaks])
    rate=float((len(peaks)-1)/(t[peaks[-1]]-t[peaks[0]])) if len(peaks)>1 else None
    cv=float(intervals.std()/intervals.mean()) if len(intervals)>0 else None
    fast=float(np.mean((intervals>=.01-1e-10)&(intervals<=.04+1e-10))) if len(intervals)>0 else 0.0
    p2p=float(np.ptp(x))
    mask=(freqs>=1)&(freqs<=120)
    dominant=float(freqs[mask][np.argmax(power[mask])]) if p2p>config["carrier_p2p_floor"] else None
    autonomous=bool(len(peaks)>=config["carrier_min_peaks"] and rate is not None and dominant is not None
        and 25<=rate<=100 and 25<=dominant<=100 and abs(rate-dominant)<=config["carrier_agreement_hz"]
        and cv<config["carrier_cv_max"])
    return {"peak_count":len(peaks),"mean_cycle_hz":rate,"dominant_hz":dominant,"interval_cv":cv,
        "fast_interval_fraction":fast,"p2p":p2p,"autonomous_gamma_predicate":autonomous,
        "peak_times_s":t[peaks].tolist()}


def cycle_surrogates(amplitude, phase_unwrapped, seed, n_surrogates):
    """Rotate reference phase independently per complete theta cycle."""
    cycle = np.floor(phase_unwrapped / (2*np.pi)).astype(int)
    # Exclude partial edge cycles. Fixed physical protocol phase defines cycle identity.
    full = (cycle > cycle.min()) & (cycle < cycle.max())
    ids, inverse = np.unique(cycle[full], return_inverse=True)
    ph = phase_unwrapped[full]
    amp = amplitude[full]
    real, _, _, _, _ = reference_pac(amp, ph)
    cycle_vectors = np.bincount(inverse, weights=amp*np.cos(ph), minlength=len(ids)) + 1j*np.bincount(
        inverse, weights=amp*np.sin(ph), minlength=len(ids))
    rng = np.random.default_rng(seed)
    angles = rng.uniform(-np.pi, np.pi, (n_surrogates, len(ids)))
    null = np.abs(np.exp(1j*angles) @ cycle_vectors) / max(amp.sum(), 1e-300)
    p = (1 + np.count_nonzero(null >= real)) / (n_surrogates+1)
    return real, null, float(p), len(ids)


def analyze(raw, config):
    t = raw["t_s"]
    dt = float(np.median(np.diff(t)))
    assert np.allclose(np.diff(t), dt, atol=1e-10)
    phase = 2*np.pi*config["theta_hz"]*t
    base = raw["E"] - 0.5*raw["I"]
    theta = np.cos(phase)[:, None, None]
    views = {"proxy": base+0.2*theta, "no_theta": base,
             "E": raw["E"], "E_minus_I": raw["E"]-raw["I"]}
    keep = (t >= t[0]+config["edge_trim_s"]) & (t <= t[-1]-config["edge_trim_s"])
    shape = base.shape[1:]
    envelope = np.abs(analytic_band(views["proxy"], dt, config["gamma_band_hz"]))
    theta_z = analytic_band(views["proxy"], dt, config["theta_band_hz"])
    all_metrics = []
    curves = np.empty((len(views), *shape, config["n_bins"]))
    counts = np.empty((len(views), *shape, config["n_bins"]), dtype=int)
    surrogates = np.empty((len(views), *shape, config["n_surrogates"]))
    all_psd = []
    dynamics={}
    for pop in ["E","I"]:
        fq,power=braintools.metric.power_spectral_density(raw[pop][keep].reshape(keep.sum(),-1),
            dt*u.second,nperseg=config["nperseg"])
        fq,power=np.asarray(fq),np.asarray(power).reshape((-1,*shape))
        for rep in range(shape[0]):
            for cond in range(shape[1]):
                dynamics[pop,rep,cond]=carrier_features(raw[pop][keep,rep,cond],t[keep],fq,power[:,rep,cond],config)
    for vi, (view, y) in enumerate(views.items()):
        amp = np.abs(analytic_band(y, dt, config["gamma_band_hz"]))
        freqs, psd = braintools.metric.power_spectral_density(
            y[keep].reshape(keep.sum(), -1), dt*u.second, nperseg=config["nperseg"])
        freqs, psd = np.asarray(freqs), np.asarray(psd).reshape((-1, *shape))
        all_psd.append(psd)
        for rep in range(shape[0]):
            for cond in range(shape[1]):
                a = amp[keep, rep, cond]
                R, MI, preferred, curve, bins = reference_pac(a, phase[keep], config["n_bins"])
                curves[vi,rep,cond], counts[vi,rep,cond] = curve,bins
                real, null, p, n_cycles = cycle_surrogates(a, phase[keep], config["surrogate_seed"],
                                                         config["n_surrogates"])
                surrogates[vi,rep,cond] = null
                power = psd[:,rep,cond]
                gamma = (freqs >= 25) & (freqs <= 100)
                total = (freqs >= 1) & (freqs <= 120)
                fraction = float(power[gamma].sum()/max(power[total].sum(),1e-300))
                band_peak = float(freqs[gamma][np.argmax(power[gamma])])
                peaks = scipy.signal.find_peaks(power)[0]
                gamma_peak = bool(np.any((freqs[peaks] >= 25) & (freqs[peaks] <= 100)))
                legacy_valid = gamma_peak and fraction > config["gamma_fraction_floor"] and a.mean() > config["amplitude_floor"]
                ecycle,icycle=dynamics["E",rep,cond],dynamics["I",rep,cond]
                timing_valid=all(v["fast_interval_fraction"]>=config["fast_interval_fraction_floor"]
                    and v["p2p"]>config["carrier_p2p_floor"] for v in [ecycle,icycle])
                autonomous=all(v["autonomous_gamma_predicate"] for v in [ecycle,icycle]) and abs(
                    (ecycle["mean_cycle_hz"] or 0)-(icycle["mean_cycle_hz"] or 0))<=config["carrier_agreement_hz"]
                valid = legacy_valid and timing_valid
                th = theta_z[keep,rep,cond]
                estimated_phase = np.angle(th)
                est_R, _, _, _, _ = reference_pac(a, estimated_phase, config["n_bins"])
                th_error = np.angle(np.mean(np.exp(1j*(estimated_phase-phase[keep]))))
                native_mi, _, _ = braintools.metric.phase_amplitude_coupling(
                    y[keep,rep,cond], dt*u.second, phase_freq_range=tuple(config["theta_band_hz"]),
                    amplitude_freq_range=tuple(config["gamma_band_hz"]), n_bins=config["n_bins"])
                windows = []
                for lo,hi in config["time_windows_s"]:
                    w = keep & (t >= lo) & (t < hi)
                    windows.append(reference_pac(amp[w,rep,cond], phase[w], config["n_bins"])[0])
                all_metrics.append({"view":view,"rep":rep,"condition":cond,
                    "depth":float(raw["depths_flat"][cond]),"gain":float(raw["gains_flat"][cond]),
                    "R":R,"MI":MI,"preferred_phase_rad":preferred,"mean_envelope":float(a.mean()),
                    "gamma_fraction":fraction,"band_peak_hz":band_peak,"gamma_peak_present":gamma_peak,
                    "legacy_band_valid":bool(legacy_valid),"fast_timing_valid":bool(timing_valid),
                    "autonomous_gamma_predicate":bool(autonomous),"E_cycle":ecycle,"I_cycle":icycle,
                    "valid_gamma":bool(valid),"defined_peak_hz":band_peak if valid else None,
                    "surrogate_observed_R":real,"surrogate_q95":float(np.quantile(null,0.95)),
                    "surrogate_p_descriptive":p,"surrogate_cycles":n_cycles,
                    "estimated_phase_R":est_R,"theta_phase_bias_rad":float(th_error),
                    "theta_phase_consistency":float(abs(np.mean(np.exp(1j*(estimated_phase-phase[keep]))))),
                    "native_single_signal_MI":float(native_mi),"window_R":windows})
    derived = {"t_s":t,"analysis_keep":keep,"phase_rad":phase,"proxy":views["proxy"],
        "base_proxy":base,"gamma_envelope":envelope,"theta_phase_est_rad":np.angle(theta_z),
        "phase_curves":curves,"phase_counts":counts,"surrogates_R":surrogates,
        "phase_bin_centers_rad":np.linspace(-np.pi,np.pi,config["n_bins"],endpoint=False)+np.pi/config["n_bins"],
        "freqs_hz":freqs,"psd":np.asarray(all_psd),"view_names":np.asarray(list(views)),
        "depth_axis":np.asarray(config["depth_axis"]),"gain_axis":np.asarray(config["gain_axis"]),
        "grid_shape":np.asarray([len(config["depth_axis"]),len(config["gain_axis"])]),
        "axis_order":np.asarray(["view","IC","condition"])}
    return all_metrics, derived
