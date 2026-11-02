"""Formal immutable production runner for the alpha-rhythm experiment."""

from __future__ import annotations

import argparse
import contextlib
import json
import time
from pathlib import Path

import brainunit as u
import jax
import numpy as np

import alpha_rhythm as experiment


def run(output_dir: Path, run_level: str) -> None:
    if not output_dir.is_dir():
        raise FileNotFoundError("the immutable run directory must exist before launch")
    required_snapshot = (
        "RUN_SPEC.md",
        "config.json",
        "environment.json",
        "command.txt",
        "code.diff",
        "status.json",
    )
    missing = [
        name for name in required_snapshot if not (output_dir / name).is_file()
    ]
    if missing:
        raise FileNotFoundError(f"run snapshot is incomplete: {missing}")
    snapshot = json.loads((output_dir / "config.json").read_text())
    if snapshot.get("run_level") != run_level:
        raise ValueError("command run level does not match immutable config")
    if snapshot.get("scientific_config") != experiment.frozen_configuration():
        raise ValueError("immutable scientific config does not match the code")
    experiment.write_json(
        output_dir / "status.json",
        {"status": "running", "run_level": run_level},
    )
    log_path = output_dir / "run.log"
    with (
        log_path.open("a") as log,
        contextlib.redirect_stdout(log),
        contextlib.redirect_stderr(log),
    ):
        print(f"alpha-rhythm {run_level} run")
        print(json.dumps(experiment.frozen_configuration(), indent=2, sort_keys=True))

        smoke = experiment.run_grid(
            retention_fractions=np.asarray([1.0, 0.25]),
            initial_m=np.asarray([-2.0, 2.0]) * u.mV,
            dt=experiment.PRODUCTION_DT,
            duration=2.0 * u.ms,
            jit=False,
        )
        smoke_checks = experiment.finite_and_bounded(smoke)
        smoke_component_error = experiment.component_identity_error_mv(smoke)
        if not smoke_checks["all_eeg_finite"] or smoke_component_error > 1e-9:
            raise RuntimeError("target-device smoke gate failed")
        experiment.write_json(
            output_dir / "smoke_checks.json",
            {**smoke_checks, "component_identity_error_mv": smoke_component_error},
        )
        if run_level == "smoke":
            experiment.write_json(
                output_dir / "provenance.json",
                experiment.environment_provenance(
                    [Path(experiment.__file__), Path(__file__)]
                ),
            )
            experiment.write_json(
                output_dir / "status.json",
                {"status": "done", "run_level": run_level, "exit_code": 0},
            )
            (output_dir / "exit_code").write_text("0\n")
            artifacts = sorted(path.name for path in output_dir.iterdir())
            experiment.write_json(
                output_dir / "artifact_manifest.json",
                {
                    "schema_version": experiment.SCHEMA_VERSION,
                    "artifacts": artifacts + ["artifact_manifest.json"],
                    "completed": True,
                },
            )
            print("smoke completed")
            return

        runner = experiment.build_mapped_rollout(
            dt=experiment.PRODUCTION_DT,
            duration=experiment.PRODUCTION_DURATION,
            jit=True,
        )
        ai_lanes = np.repeat(
            np.asarray(experiment.RETENTION_FRACTIONS),
            experiment.INITIAL_M.shape[0],
        ) * experiment.BASELINE_AI
        initial_lanes = u.math.tile(
            experiment.INITIAL_M,
            experiment.RETENTION_FRACTIONS.shape[0],
        )

        start = time.perf_counter()
        warmup = runner(ai_lanes, initial_lanes)
        jax.block_until_ready(warmup)
        first_call_seconds = time.perf_counter() - start

        start = time.perf_counter()
        results = experiment.run_grid(runner=runner, jit=True)
        jax.block_until_ready(results["eeg"])
        steady_call_seconds = time.perf_counter() - start
        retained, record_dt = experiment.retained_eeg(
            results["eeg"],
            dt=experiment.PRODUCTION_DT,
        )
        metrics = experiment.spectral_metrics(retained, record_dt)

        half_step = experiment.run_grid(
            retention_fractions=experiment.RETENTION_FRACTIONS,
            initial_m=experiment.INITIAL_M,
            dt=experiment.PRODUCTION_DT / 2,
            duration=experiment.PRODUCTION_DURATION,
            jit=True,
        )
        half_retained, half_record_dt = experiment.retained_eeg(
            half_step["eeg"],
            dt=experiment.PRODUCTION_DT / 2,
            decimation=experiment.ANALYSIS_DECIMATION * 2,
        )
        half_metrics = experiment.spectral_metrics(half_retained, half_record_dt)
        convergence = experiment.convergence_evidence(
            results,
            metrics,
            half_step,
            half_metrics,
        )
        finite_checks = experiment.finite_and_bounded(results)
        component_error = experiment.component_identity_error_mv(results)
        assessment = experiment.assess_results(
            metrics,
            finite_checks=finite_checks,
            component_error_mv=component_error,
            convergence=convergence,
        )
        summaries = experiment.summarize_conditions(metrics)

        experiment.write_json(
            output_dir / "provenance.json",
            experiment.environment_provenance(
                [Path(experiment.__file__), Path(__file__)]
            ),
        )
        experiment.save_numeric_results(output_dir / "results.npz", results, metrics)
        experiment.save_numeric_results(
            output_dir / "half_step_results.npz", half_step, half_metrics
        )
        experiment.write_json(
            output_dir / "metrics.json",
            {
                "condition_summaries": summaries,
                "rms_mv": metrics["rms_mv"].tolist(),
                "peak_hz": metrics["peak_hz"].tolist(),
                "alpha_fraction_4_30": metrics["alpha_fraction_4_30"].tolist(),
            },
        )
        experiment.write_json(output_dir / "convergence.json", {"checks": convergence})
        experiment.write_json(
            output_dir / "assessment.json",
            {
                **assessment,
                "finite_checks": finite_checks,
                "component_identity_error_mv": component_error,
            },
        )
        experiment.write_json(
            output_dir / "performance.json",
            {
                "first_call_compilation_plus_execution_seconds": first_call_seconds,
                "steady_call_seconds": steady_call_seconds,
                "device": str(jax.devices()[0]),
                "output_shape": list(results["eeg"].shape),
                "output_bytes_lower_bound": int(
                    results["eeg"].size * results["eeg"].dtype.itemsize * 3
                ),
            },
        )
        claim_matrix = experiment.claim_evidence(assessment)
        experiment.write_json(output_dir / "claim_evidence.json", claim_matrix)

        experiment.write_json(
            output_dir / "status.json",
            {"status": "done", "run_level": run_level, "exit_code": 0},
        )
        (output_dir / "exit_code").write_text("0\n")
        artifacts = sorted(path.name for path in output_dir.iterdir())
        experiment.write_json(
            output_dir / "artifact_manifest.json",
            {
                "schema_version": experiment.SCHEMA_VERSION,
                "artifacts": artifacts + ["artifact_manifest.json"],
                "completed": True,
            },
        )
        print("completed")
        print(json.dumps(assessment, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--run-level",
        choices=("smoke", "production"),
        required=True,
    )
    args = parser.parse_args()
    run(args.output_dir.resolve(), args.run_level)


if __name__ == "__main__":
    main()

