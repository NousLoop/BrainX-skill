"""Unit-aware Jansen--Rit alpha rhythm experiment.

The scientific intervention is the retention fraction of the inhibitory
postsynaptic gain ``Ai``.  BrainMass owns the neural-mass equations, BrainState
owns stateful control flow and vectorization, and BrainUnit owns physical
quantities until the explicit NumPy/JSON artifact boundary.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any, Callable

import brainmass
import brainstate
import braintools
import brainunit as u
import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402


SCHEMA_VERSION = "alpha-rhythm-v1"
MODEL_NAME = "brainmass.JansenRitStep"
BASELINE_AI = 22.0 * u.mV
EXTERNAL_RATE = 220.0 * u.Hz
RETENTION_FRACTIONS = jnp.asarray([1.0, 0.75, 0.50, 0.25])
INITIAL_M = jnp.asarray([-2.0, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5, 2.0]) * u.mV
PRODUCTION_DT = 0.1 * u.ms
PRODUCTION_DURATION = 6.0 * u.second
TRANSIENT = 2.0 * u.second
ANALYSIS_DECIMATION = 10
PSD_NPERSEG = 2000
PSD_NOVERLAP = 1000
OSCILLATION_RMS_FLOOR_MV = 0.01
BASELINE_RMS_FLOOR_MV = 0.05
EEG_ABS_BOUND_MV = 100.0


def _require_quantity(value: u.Quantity, expected_unit: u.Unit, name: str) -> None:
    if not isinstance(value, u.Quantity):
        raise TypeError(f"{name} must be a BrainUnit Quantity")
    if not u.have_same_dim(value.unit, expected_unit):
        raise u.UnitMismatchError(
            f"{name} must have dimension {expected_unit.dim}, got {value.dim}"
        )


def validate_run_inputs(
    ai: u.Quantity,
    initial_m: u.Quantity,
    dt: u.Quantity,
    duration: u.Quantity,
) -> None:
    """Validate physical boundaries before constructing transformed execution."""

    _require_quantity(ai, u.mV, "Ai")
    _require_quantity(initial_m, u.mV, "initial_M")
    _require_quantity(dt, u.ms, "dt")
    _require_quantity(duration, u.second, "duration")
    if float(dt.to_decimal(u.ms)) <= 0.0:
        raise ValueError("dt must be positive")
    if float(duration.to_decimal(u.second)) <= 0.0:
        raise ValueError("duration must be positive")


def make_model(ai: u.Quantity) -> brainmass.JansenRitStep:
    """Construct the package-owned cortical-column model."""

    _require_quantity(ai, u.mV, "Ai")
    return brainmass.JansenRitStep(in_size=1, Ai=ai)


def _zero_dynamical_state_and_set_m(
    model: brainmass.JansenRitStep,
    initial_m: u.Quantity,
) -> None:
    """Create deterministic, exactly paired dynamical initial conditions."""

    for state in model.states(brainstate.HiddenState).values():
        state.value = u.math.zeros_like(state.value)
    model.M.value = u.math.zeros_like(model.M.value) + initial_m


def build_mapped_rollout(
    *,
    dt: u.Quantity,
    duration: u.Quantity,
    jit: bool,
) -> Callable[[u.Quantity, u.Quantity], tuple[u.Quantity, u.Quantity, u.Quantity]]:
    """Build one stable stateful vmap whose inner operation owns one rollout."""

    validate_run_inputs(BASELINE_AI, INITIAL_M[0], dt, duration)
    n_steps_float = duration.to_decimal(u.second) / dt.to_decimal(u.second)
    n_steps = int(round(float(n_steps_float)))
    if not np.isclose(n_steps, float(n_steps_float), rtol=0.0, atol=1e-9):
        raise ValueError("duration must be an integer multiple of dt")
    indices = jnp.arange(n_steps, dtype=jnp.int32)

    def run_lane(ai: u.Quantity, initial_m: u.Quantity):
        model = make_model(ai)
        with brainstate.environ.context(dt=dt, fit=False):
            brainstate.nn.init_all_states(model)
            _zero_dynamical_state_and_set_m(model, initial_m)

            def step(index):
                with brainstate.environ.context(
                    i=index,
                    t=(index + 1) * dt,
                ):
                    model.update(0.0 * u.mV, EXTERNAL_RATE, 0.0 * u.mV)
                return model.eeg(), model.E.value, model.I.value

            return brainstate.transform.for_loop(step, indices)

    mapped = brainstate.transform.vmap(run_lane)
    return brainstate.transform.jit(mapped) if jit else mapped


def _lane_major_to_time_grid(
    value: u.Quantity,
    n_conditions: int,
    n_initial: int,
) -> u.Quantity:
    """Convert [lane, time, 1] to [time, condition, initial_condition]."""

    lane_time = value[:, :, 0]
    return lane_time.reshape(
        (n_conditions, n_initial, lane_time.shape[1])
    ).transpose(2, 0, 1)


def run_grid(
    retention_fractions: jax.Array = RETENTION_FRACTIONS,
    initial_m: u.Quantity = INITIAL_M,
    *,
    dt: u.Quantity = PRODUCTION_DT,
    duration: u.Quantity = PRODUCTION_DURATION,
    jit: bool = False,
    runner: Callable | None = None,
) -> dict[str, u.Quantity]:
    """Run the complete intervention-by-initial-condition grid."""

    retention_fractions = jnp.asarray(retention_fractions, dtype=jnp.float64)
    _require_quantity(initial_m, u.mV, "initial_M")
    if retention_fractions.ndim != 1 or initial_m.ndim != 1:
        raise ValueError("retention_fractions and initial_m must be one-dimensional")
    if bool(jnp.any(retention_fractions <= 0.0)):
        raise ValueError("all inhibition retention fractions must be positive")

    n_conditions = int(retention_fractions.shape[0])
    n_initial = int(initial_m.shape[0])
    ai_lanes = jnp.repeat(retention_fractions, n_initial) * BASELINE_AI
    initial_lanes = u.math.tile(initial_m, n_conditions)
    mapped_rollout = runner or build_mapped_rollout(dt=dt, duration=duration, jit=jit)
    eeg_lanes, excitatory_lanes, inhibitory_lanes = mapped_rollout(ai_lanes, initial_lanes)

    eeg = _lane_major_to_time_grid(eeg_lanes, n_conditions, n_initial)
    excitatory = _lane_major_to_time_grid(excitatory_lanes, n_conditions, n_initial)
    inhibitory = _lane_major_to_time_grid(inhibitory_lanes, n_conditions, n_initial)
    times = (jnp.arange(eeg.shape[0], dtype=jnp.float64) + 1.0) * dt
    return {
        "times": times,
        "eeg": eeg,
        "excitatory_psp": excitatory,
        "inhibitory_psp": inhibitory,
        "retention_fractions": retention_fractions,
        "initial_m": initial_m,
        "ai": retention_fractions * BASELINE_AI,
    }


def retained_eeg(
    eeg: u.Quantity,
    *,
    dt: u.Quantity,
    transient: u.Quantity = TRANSIENT,
    decimation: int = ANALYSIS_DECIMATION,
) -> tuple[u.Quantity, u.Quantity]:
    """Apply only the locked transient removal, decimation, and demeaning."""

    _require_quantity(eeg, u.mV, "eeg")
    transient_steps_float = transient.to_decimal(u.second) / dt.to_decimal(u.second)
    transient_steps = int(round(float(transient_steps_float)))
    if not np.isclose(transient_steps, float(transient_steps_float), atol=1e-9):
        raise ValueError("transient must be an integer multiple of dt")
    if decimation < 1:
        raise ValueError("decimation must be positive")
    retained = eeg[transient_steps::decimation]
    retained = retained - u.math.mean(retained, axis=0, keepdims=True)
    return retained, dt * decimation


def spectral_metrics(
    demeaned_eeg: u.Quantity,
    record_dt: u.Quantity,
    *,
    nperseg: int = PSD_NPERSEG,
    noverlap: int = PSD_NOVERLAP,
) -> dict[str, np.ndarray]:
    """Compute locked per-lane amplitude and Welch spectral summaries."""

    _require_quantity(demeaned_eeg, u.mV, "demeaned_eeg")
    _require_quantity(record_dt, u.ms, "record_dt")
    if demeaned_eeg.ndim != 3:
        raise ValueError("demeaned_eeg must have [time, condition, initial] axes")
    eeg_mv = np.asarray(demeaned_eeg.to_decimal(u.mV), dtype=np.float64)
    n_time, n_conditions, n_initial = eeg_mv.shape
    channels = jnp.asarray(eeg_mv.reshape(n_time, n_conditions * n_initial))
    frequencies, power = braintools.metric.power_spectral_density(
        channels,
        record_dt,
        nperseg=nperseg,
        noverlap=noverlap,
    )
    frequencies_hz = np.asarray(frequencies, dtype=np.float64)
    power_np = np.asarray(power, dtype=np.float64).reshape(
        frequencies_hz.size,
        n_conditions,
        n_initial,
    )
    rms_mv = np.sqrt(np.mean(eeg_mv**2, axis=0))
    search = (frequencies_hz >= 4.0) & (frequencies_hz <= 30.0)
    alpha = (frequencies_hz >= 8.0) & (frequencies_hz <= 13.0)
    if not np.any(search) or not np.any(alpha):
        raise ValueError("PSD frequency grid does not cover the locked bands")
    search_power = power_np[search]
    peak_indices = np.argmax(search_power, axis=0)
    peak_hz = frequencies_hz[search][peak_indices]
    peak_hz = np.where(rms_mv >= OSCILLATION_RMS_FLOOR_MV, peak_hz, np.nan)
    band_power = np.sum(search_power, axis=0)
    alpha_power = np.sum(power_np[alpha], axis=0)
    alpha_fraction = np.divide(
        alpha_power,
        band_power,
        out=np.full_like(alpha_power, np.nan),
        where=band_power > 0.0,
    )
    return {
        "frequencies_hz": frequencies_hz,
        "power_mv2_per_hz": power_np,
        "rms_mv": rms_mv,
        "peak_hz": peak_hz,
        "alpha_fraction_4_30": alpha_fraction,
    }


def component_identity_error_mv(results: dict[str, u.Quantity]) -> float:
    """Check the public Jansen--Rit EEG mapping M = E - I."""

    error = results["eeg"] - (
        results["excitatory_psp"] - results["inhibitory_psp"]
    )
    return float(np.max(np.abs(np.asarray(error.to_decimal(u.mV)))))


def finite_and_bounded(results: dict[str, u.Quantity]) -> dict[str, Any]:
    eeg_mv = np.asarray(results["eeg"].to_decimal(u.mV), dtype=np.float64)
    finite = bool(np.isfinite(eeg_mv).all())
    max_abs = float(np.max(np.abs(eeg_mv)))
    return {
        "all_eeg_finite": finite,
        "max_abs_eeg_mv": max_abs,
        "within_locked_eeg_bound": finite and max_abs < EEG_ABS_BOUND_MV,
    }


def summarize_conditions(metrics: dict[str, np.ndarray]) -> dict[str, list[float]]:
    return {
        "median_rms_mv": np.nanmedian(metrics["rms_mv"], axis=1).tolist(),
        "median_peak_hz": np.nanmedian(metrics["peak_hz"], axis=1).tolist(),
        "median_alpha_fraction_4_30": np.nanmedian(
            metrics["alpha_fraction_4_30"], axis=1
        ).tolist(),
    }


def assess_results(
    metrics: dict[str, np.ndarray],
    *,
    finite_checks: dict[str, Any],
    component_error_mv: float,
    convergence: list[dict[str, Any]],
) -> dict[str, Any]:
    """Apply the prespecified deterministic acceptance boundary."""

    rms = metrics["rms_mv"]
    peak = metrics["peak_hz"]
    alpha_fraction = metrics["alpha_fraction_4_30"]
    baseline_alpha = (
        np.isfinite(peak[0])
        & (peak[0] >= 8.0)
        & (peak[0] <= 13.0)
        & (rms[0] >= OSCILLATION_RMS_FLOOR_MV)
    )
    baseline_pass = bool(
        baseline_alpha.sum() >= 7
        and np.nanmedian(alpha_fraction[0]) >= 0.50
        and np.nanmedian(rms[0]) >= BASELINE_RMS_FLOOR_MV
    )

    amplitude_percent = 100.0 * (rms[1:] - rms[0]) / rms[0]
    frequency_difference = peak[1:] - peak[0]
    condition_changes: list[dict[str, Any]] = []
    any_clear_change = False
    for index in range(amplitude_percent.shape[0]):
        amp_values = amplitude_percent[index]
        freq_values = frequency_difference[index]
        amp_median = float(np.nanmedian(amp_values))
        freq_median = float(np.nanmedian(freq_values))
        amp_direction_count = int(
            max(np.sum(amp_values > 0.0), np.sum(amp_values < 0.0))
        )
        freq_direction_count = int(
            max(np.sum(freq_values > 0.0), np.sum(freq_values < 0.0))
        )
        amp_clear = abs(amp_median) >= 10.0 and amp_direction_count >= 6
        freq_clear = abs(freq_median) >= 0.5 and freq_direction_count >= 6
        any_clear_change = any_clear_change or amp_clear or freq_clear
        condition_changes.append(
            {
                "condition_index": index + 1,
                "median_paired_rms_change_percent": amp_median,
                "rms_direction_count": amp_direction_count,
                "median_paired_peak_change_hz": freq_median,
                "peak_direction_count": freq_direction_count,
                "amplitude_change_clear": bool(amp_clear),
                "frequency_change_clear": bool(freq_clear),
            }
        )

    convergence_pass = bool(convergence) and all(item["pass"] for item in convergence)
    validity_pass = bool(
        finite_checks["all_eeg_finite"]
        and finite_checks["within_locked_eeg_bound"]
        and component_error_mv <= 1e-9
        and convergence_pass
    )
    if not validity_pass or not baseline_pass:
        scientific_outcome = "invalid"
    elif any_clear_change:
        scientific_outcome = "supported"
    else:
        scientific_outcome = "partially_supported"
    return {
        "validity_pass": validity_pass,
        "baseline_alpha_lane_count": int(baseline_alpha.sum()),
        "baseline_alpha_pass": baseline_pass,
        "baseline_median_rms_mv": float(np.nanmedian(rms[0])),
        "baseline_median_peak_hz": float(np.nanmedian(peak[0])),
        "baseline_median_alpha_fraction_4_30": float(
            np.nanmedian(alpha_fraction[0])
        ),
        "clear_intervention_change": bool(any_clear_change),
        "condition_changes": condition_changes,
        "scientific_outcome": scientific_outcome,
    }


def convergence_evidence(
    production_results: dict[str, u.Quantity],
    production_metrics: dict[str, np.ndarray],
    half_step_results: dict[str, u.Quantity],
    half_step_metrics: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    """Compare 0.1 ms and 0.05 ms summary metrics at 100% and 25% inhibition."""

    evidence: list[dict[str, Any]] = []
    for half_index, production_index in enumerate((0, 3)):
        full_rms = float(production_metrics["rms_mv"][production_index, 0])
        half_rms = float(half_step_metrics["rms_mv"][half_index, 0])
        full_peak = float(production_metrics["peak_hz"][production_index, 0])
        half_peak = float(half_step_metrics["peak_hz"][half_index, 0])
        rms_relative = abs(half_rms - full_rms) / max(abs(half_rms), 1e-12)
        peak_difference = abs(half_peak - full_peak)
        evidence.append(
            {
                "retention_fraction": float((1.0, 0.25)[half_index]),
                "production_rms_mv": full_rms,
                "half_step_rms_mv": half_rms,
                "rms_relative_difference": rms_relative,
                "production_peak_hz": full_peak,
                "half_step_peak_hz": half_peak,
                "peak_difference_hz": peak_difference,
                "pass": bool(rms_relative <= 0.05 and peak_difference <= 0.5),
            }
        )
    return evidence


def frozen_configuration() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "model": MODEL_NAME,
        "model_defaults": "installed BrainMass defaults except explicit Ai",
        "baseline_ai_mv": float(BASELINE_AI.to_decimal(u.mV)),
        "retention_fractions": np.asarray(RETENTION_FRACTIONS).tolist(),
        "ai_mv": np.asarray((RETENTION_FRACTIONS * BASELINE_AI).to_decimal(u.mV)).tolist(),
        "external_rate_hz": float(EXTERNAL_RATE.to_decimal(u.Hz)),
        "initial_m_mv": np.asarray(INITIAL_M.to_decimal(u.mV)).tolist(),
        "dt_ms": float(PRODUCTION_DT.to_decimal(u.ms)),
        "duration_s": float(PRODUCTION_DURATION.to_decimal(u.second)),
        "transient_s": float(TRANSIENT.to_decimal(u.second)),
        "monitor_phase": "post-update; sample 0 is at one dt",
        "analysis_decimation": ANALYSIS_DECIMATION,
        "analysis_dt_ms": float(
            (PRODUCTION_DT * ANALYSIS_DECIMATION).to_decimal(u.ms)
        ),
        "welch_window": "hann",
        "psd_nperseg": PSD_NPERSEG,
        "psd_noverlap": PSD_NOVERLAP,
        "oscillation_rms_floor_mv": OSCILLATION_RMS_FLOOR_MV,
        "baseline_rms_floor_mv": BASELINE_RMS_FLOOR_MV,
        "eeg_abs_bound_mv": EEG_ABS_BOUND_MV,
        "seed": None,
        "stochasticity": "none",
    }


def environment_provenance(source_files: list[Path]) -> dict[str, Any]:
    hashes = {
        str(path.resolve()): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in source_files
    }
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "jax_backend": jax.default_backend(),
        "jax_devices": [str(device) for device in jax.devices()],
        "jax_x64_enabled": bool(jax.config.read("jax_enable_x64")),
        "source_sha256": hashes,
        "dependency_identity_policy": (
            "BrainX package versions are not introspected; public API identity and "
            "source hashes define this run."
        ),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def save_numeric_results(
    path: Path,
    results: dict[str, u.Quantity],
    metrics: dict[str, np.ndarray],
) -> None:
    """Write one self-describing numeric bundle at the explicit host boundary."""

    np.savez_compressed(
        path,
        schema_version=np.asarray(SCHEMA_VERSION),
        times_s=np.asarray(results["times"].to_decimal(u.second)),
        eeg_mv=np.asarray(results["eeg"].to_decimal(u.mV)),
        excitatory_psp_mv=np.asarray(results["excitatory_psp"].to_decimal(u.mV)),
        inhibitory_psp_mv=np.asarray(results["inhibitory_psp"].to_decimal(u.mV)),
        retention_fractions=np.asarray(results["retention_fractions"]),
        initial_m_mv=np.asarray(results["initial_m"].to_decimal(u.mV)),
        ai_mv=np.asarray(results["ai"].to_decimal(u.mV)),
        frequencies_hz=metrics["frequencies_hz"],
        power_mv2_per_hz=metrics["power_mv2_per_hz"],
        rms_mv=metrics["rms_mv"],
        peak_hz=metrics["peak_hz"],
        alpha_fraction_4_30=metrics["alpha_fraction_4_30"],
        axis_order=np.asarray("time,condition,initial_condition"),
        eeg_unit=np.asarray("mV"),
        time_unit=np.asarray("s"),
        frequency_unit=np.asarray("Hz"),
    )

