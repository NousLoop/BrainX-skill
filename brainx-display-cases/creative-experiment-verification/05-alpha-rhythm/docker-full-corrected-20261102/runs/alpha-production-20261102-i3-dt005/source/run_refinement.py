"""Immutable numerical diagnostic and full-grid refined alpha sweep."""
import argparse
import contextlib
import hashlib
import os
from pathlib import Path
import shutil
import time
import traceback

import brainunit as u
import jax
import numpy as np
import alpha_rhythm as experiment


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(dt_ms):
    dt = dt_ms * u.ms
    runner = experiment.build_mapped_rollout(dt=dt, duration=experiment.PRODUCTION_DURATION, jit=True)
    start = time.perf_counter()
    results = experiment.run_grid(dt=dt, runner=runner)
    jax.block_until_ready(results["eeg"])
    first = time.perf_counter() - start
    retained, interval = experiment.retained_eeg(results["eeg"], dt=dt, decimation=round(1 / dt_ms))
    metrics = experiment.spectral_metrics(retained, interval)
    return results, metrics, {"first_call_compile_and_execute_s": first, "raw_shape": list(results["eeg"].shape)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["diagnostic", "production"], required=True)
    parser.add_argument("--dt-ms", type=float, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=False)
    names = ["alpha_rhythm.py", "run_refinement.py", "test_alpha_rhythm.py",
             "NeuroSpecification.md", "NUMERICAL_PROTOCOL_AMENDMENT.md"]
    snapshot = out / "source"
    snapshot.mkdir()
    for name in names:
        shutil.copyfile(name, snapshot / name)
    config = experiment.frozen_configuration()
    config.update(dt_ms=args.dt_ms, analysis_decimation=round(1 / args.dt_ms), analysis_dt_ms=1.0,
                  half_step_dt_ms=args.dt_ms / 2, convergence_grid="all 4 conditions x all 8 initial states",
                  mode=args.mode, original_runs="alpha-production-20261102-i1 and i2 remain invalid")
    experiment.write_json(out / "config.json", config)
    experiment.write_json(out / "environment.json", {
        **experiment.environment_provenance([Path(name) for name in names]),
        "docker_image_id": os.environ["BRAINX_IMAGE_ID"],
        "docker_seccomp_sha256": os.environ["BRAINX_SECCOMP_SHA256"],
        "integration_method": "exp_euler",
    })
    (out / "command.txt").write_text("python run_refinement.py --mode " + args.mode
        + " --dt-ms " + str(args.dt_ms) + " --output-dir " + str(out) + "\n")
    (out / "RUN_SPEC.md").write_text("# Immutable numerical run\n\nUse the locked specification and numerical amendment. "
        "No biological parameter or acceptance threshold is tuned. Inputs are deterministic. "
        "Source snapshots are in source/. Mechanical completion is not scientific acceptance.\n")
    before = {name: digest(Path(name)) for name in names}
    experiment.write_json(out / "status.json", {"status": "running"})
    try:
        with (out / "run.log").open("w") as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            results, metrics, performance = execute(args.dt_ms)
            experiment.save_numeric_results(out / "results.npz", results, metrics)
            experiment.write_json(out / "metrics.json", {
                "condition_summaries": experiment.summarize_conditions(metrics),
                "rms_mv": metrics["rms_mv"].tolist(), "peak_hz": metrics["peak_hz"].tolist(),
                "alpha_fraction_4_30": metrics["alpha_fraction_4_30"].tolist()})
            if args.mode == "diagnostic":
                with np.load("runs/alpha-production-20261102-i1/half_step_results.npz") as old:
                    q, interval = experiment.retained_eeg(old["eeg_mv"] * u.mV, dt=0.05 * u.ms, decimation=20)
                    old_metrics = experiment.spectral_metrics(q, interval)
                checks = []
                for old_index, new_index in [(0, 0), (1, 3)]:
                    checks.append({"condition_index": new_index,
                        **experiment.compare_lane_metrics(float(old_metrics["rms_mv"][old_index, 0]),
                            float(metrics["rms_mv"][new_index, 0]),
                            float(old_metrics["peak_hz"][old_index, 0]),
                            float(metrics["peak_hz"][new_index, 0]))})
                experiment.write_json(out / "diagnostic_comparison.json", {"coarse_dt_ms": 0.05,
                    "fine_dt_ms": args.dt_ms, "checks": checks, "scientific_acceptance": False})
            else:
                fine, fine_metrics, fine_performance = execute(args.dt_ms / 2)
                experiment.save_numeric_results(out / "half_step_results.npz", fine, fine_metrics)
                checks = experiment.convergence_evidence(results, metrics, fine, fine_metrics)
                experiment.write_json(out / "convergence.json", {"checks": checks,
                    "all_lanes_pass": all(c["pass"] for c in checks)})
                finite = experiment.finite_and_bounded(results)
                finite["all_eeg_finite"] = bool(finite["all_eeg_finite"] and all(
                    np.isfinite(np.asarray(value.to_decimal(u.mV))).all()
                    for value in [results["excitatory_psp"], results["inhibitory_psp"],
                                  fine["eeg"], fine["excitatory_psp"], fine["inhibitory_psp"]]))
                error = max(experiment.component_identity_error_mv(results),
                            experiment.component_identity_error_mv(fine))
                assessment = experiment.assess_results(metrics, finite_checks=finite,
                    component_error_mv=error, convergence=checks)
                experiment.write_json(out / "assessment.json", {**assessment,
                    "finite_checks": finite, "component_identity_error_mv": error})
                experiment.write_json(out / "claim_evidence.json", experiment.claim_evidence(assessment))
                performance["half_step"] = fine_performance
            experiment.write_json(out / "performance.json", performance)
            assert before == {name: digest(Path(name)) for name in names}, "Source changed during run"
            print("completed", args.mode, args.dt_ms)
        experiment.write_json(out / "status.json", {"status": "done", "exit_code": 0})
        (out / "exit_code").write_text("0\n")
    except Exception:
        (out / "failure.txt").write_text(traceback.format_exc())
        experiment.write_json(out / "status.json", {"status": "failed", "exit_code": 1})
        (out / "exit_code").write_text("1\n")
        raise
    experiment.write_json(out / "artifact_manifest.json", {"completed": True,
        "sha256": {str(path.relative_to(out)): digest(path) for path in out.rglob("*") if path.is_file()}})
    print("DONE", args.mode, args.dt_ms, str(out), flush=True)


if __name__ == "__main__":
    main()
