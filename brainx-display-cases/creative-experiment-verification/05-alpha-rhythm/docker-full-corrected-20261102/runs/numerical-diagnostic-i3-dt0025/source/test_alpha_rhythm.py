from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import brainstate
import brainunit as u
import jax.numpy as jnp
import numpy as np

import alpha_rhythm as experiment


class AlphaRhythmTests(unittest.TestCase):
    def test_unit_boundary_rejects_wrong_ai_dimension(self):
        with self.assertRaises(u.UnitMismatchError):
            experiment.make_model(22.0 * u.Hz)

    def test_construct_initialize_and_one_step(self):
        model = experiment.make_model(experiment.BASELINE_AI)
        with brainstate.environ.context(dt=experiment.PRODUCTION_DT, fit=False):
            brainstate.nn.init_all_states(model)
            experiment._zero_dynamical_state_and_set_m(model, -1.0 * u.mV)
            before = model.M.value
            model.update(0.0 * u.mV, experiment.EXTERNAL_RATE, 0.0 * u.mV)
            model.update(0.0 * u.mV, experiment.EXTERNAL_RATE, 0.0 * u.mV)
            after = model.M.value
        self.assertEqual(before.shape, (1,))
        self.assertEqual(after.shape, (1,))
        self.assertTrue(u.have_same_dim(after.unit, u.mV))
        self.assertTrue(np.isfinite(np.asarray(after.to_decimal(u.mV))).all())
        self.assertFalse(
            np.array_equal(
                np.asarray(before.to_decimal(u.mV)),
                np.asarray(after.to_decimal(u.mV)),
            )
        )

    def test_short_stateful_vmap_and_component_identity(self):
        results = experiment.run_grid(
            retention_fractions=jnp.asarray([1.0, 0.5]),
            initial_m=jnp.asarray([-1.0, 1.0]) * u.mV,
            dt=0.1 * u.ms,
            duration=1.0 * u.ms,
            jit=False,
        )
        self.assertEqual(results["eeg"].shape, (10, 2, 2))
        self.assertEqual(results["times"].shape, (10,))
        self.assertTrue(np.isclose(results["times"][-1].to_decimal(u.ms), 1.0))
        self.assertLessEqual(experiment.component_identity_error_mv(results), 1e-12)
        self.assertTrue(experiment.finite_and_bounded(results)["all_eeg_finite"])

    def test_spectral_metrics_identify_synthetic_alpha(self):
        dt = 1.0 * u.ms
        times_s = np.arange(4000, dtype=np.float64) * 0.001
        signal = np.sin(2.0 * np.pi * 10.0 * times_s)[:, None, None] * u.mV
        metrics = experiment.spectral_metrics(signal, dt)
        self.assertEqual(metrics["rms_mv"].shape, (1, 1))
        self.assertTrue(np.isclose(metrics["peak_hz"][0, 0], 10.0, atol=0.5))
        self.assertGreater(metrics["alpha_fraction_4_30"][0, 0], 0.95)

    def test_whole_rollout_jit_parity(self):
        kwargs = {
            "retention_fractions": jnp.asarray([1.0, 0.25]),
            "initial_m": jnp.asarray([-1.0, 1.0]) * u.mV,
            "dt": 0.1 * u.ms,
            "duration": 10.0 * u.ms,
        }
        unaccelerated = experiment.run_grid(**kwargs, jit=False)
        accelerated = experiment.run_grid(**kwargs, jit=True)
        for field in ("eeg", "excitatory_psp", "inhibitory_psp"):
            self.assertTrue(u.have_same_dim(unaccelerated[field].unit, accelerated[field].unit))
            np.testing.assert_allclose(
                unaccelerated[field].to_decimal(u.mV),
                accelerated[field].to_decimal(u.mV),
                rtol=0.0,
                atol=1e-6,
            )

    def test_numeric_artifact_round_trip(self):
        results = experiment.run_grid(
            retention_fractions=jnp.asarray([1.0]),
            initial_m=jnp.asarray([-1.0]) * u.mV,
            dt=0.1 * u.ms,
            duration=4.0 * u.second,
            jit=False,
        )
        retained, record_dt = experiment.retained_eeg(
            results["eeg"],
            dt=0.1 * u.ms,
            transient=0.0 * u.second,
        )
        metrics = experiment.spectral_metrics(retained, record_dt)
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            path = temporary_path / "result.npz"
            experiment.save_numeric_results(path, results, metrics)
            with np.load(path) as saved:
                self.assertEqual(
                    saved["axis_order"].item(),
                    "time,condition,initial_condition",
                )
                self.assertEqual(saved["eeg_unit"].item(), "mV")
                self.assertEqual(saved["eeg_mv"].shape, results["eeg"].shape)

            json_path = temporary_path / "config.json"
            experiment.write_json(json_path, experiment.frozen_configuration())
            self.assertEqual(
                json.loads(json_path.read_text())["baseline_ai_mv"],
                22.0,
            )

    def test_convergence_exact_zero_and_tiny_residual(self):
        for a, b in [(0.0, 0.0), (4.25e-9, 2.13e-9)]:
            check = experiment.compare_lane_metrics(a, b, np.nan, np.nan)
            self.assertTrue(check["pass"])
            self.assertEqual(check["comparison_regime"], "both_below_floor")
            self.assertIsNone(check["peak_difference_hz"])

    def test_convergence_oscillatory_bounds_and_discordance(self):
        self.assertTrue(experiment.compare_lane_metrics(1.02, 1.0, 11.0, 11.0)["pass"])
        self.assertFalse(experiment.compare_lane_metrics(1.08, 1.0, 11.0, 11.0)["pass"])
        self.assertFalse(experiment.compare_lane_metrics(1.0, 1.0, 11.0, 12.0)["pass"])
        self.assertFalse(experiment.compare_lane_metrics(0.01001, 0.00999, 11.0, np.nan)["pass"])

    def test_invalid_evidence_never_supports_scientific_claim(self):
        result = experiment.claim_evidence({"validity_pass": False,
            "baseline_alpha_pass": True, "clear_intervention_change": True,
            "scientific_outcome": "invalid"})
        self.assertTrue(result["claims"][0]["observed_predicate"])
        self.assertTrue(all(not claim["supported"] for claim in result["claims"]))

    def test_analysis_samples_align_across_step_sizes(self):
        for dt_ms, decimation in [(0.1, 10), (0.05, 20), (0.025, 40)]:
            time = (np.arange(round(3000 / dt_ms)) + 1) * dt_ms
            q = time[:, None, None] * u.mV
            retained, interval = experiment.retained_eeg(q, dt=dt_ms * u.ms,
                transient=2 * u.second, decimation=decimation)
            expected = np.arange(2001, 3001, dtype=float)
            expected -= expected.mean()
            np.testing.assert_allclose(retained.to_decimal(u.mV)[:, 0, 0], expected, atol=1e-9)
            self.assertAlmostEqual(float(interval.to_decimal(u.ms)), 1.0)


if __name__ == "__main__":
    unittest.main()
