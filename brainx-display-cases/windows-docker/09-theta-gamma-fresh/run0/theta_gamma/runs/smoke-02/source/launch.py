"""Freeze an immutable local run snapshot, launch, and collect mechanical status."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
SOURCES=["model.py","analysis.py","experiment.py","launch.py","verify.py","assess.py","figures.py","NeuroSpecification.md"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def config(level):
    depth=[0,.25,.5,.75,1.0]; gain=[.8,.9,1.0,1.1,1.2]
    if level=="convergence": depth,gain=[0,.75],[1.0]
    return {"schema_version":1,"level":level,"depth_axis":depth,"gain_axis":gain,
        "depths_flat":[m for m in depth for g in gain],"gains_flat":[g for m in depth for g in gain],
        "initial_e":[.1,.11,.09],"initial_i":[.1,.09,.11],"theta_hz":6.0,"mean_drive":1.25,
        "duration_s":2.5 if level=="smoke" else 12.0,"transient_s":.5 if level=="smoke" else 2.0,
        "dt_ms":.025 if level=="convergence" else .05,"sample_every":40 if level=="convergence" else 20,
        "tau_e_ms":1.25,"tau_i_ms":2.5,
        "method":"euler","precision":64,"backend":"cpu","edge_trim_s":.5,
        "theta_band_hz":[4,8],"gamma_band_hz":[25,100],"n_bins":18,"nperseg":2000,
        "gamma_fraction_floor":.1,"amplitude_floor":1e-4,"surrogate_seed":20261103,
        "n_surrogates":199,"time_windows_s":[[5,10],[10,11.5]],
        "R_difference_threshold":.05,"R_convergence_tolerance":.02,"peak_convergence_tolerance_hz":2.0,
        "carrier_prominence":.2,"carrier_min_distance_s":.004,"carrier_min_peaks":20,
        "carrier_p2p_floor":.05,"carrier_agreement_hz":2.0,"carrier_cv_max":.2,
        "fast_interval_fraction_floor":.5,"iteration":2}


def main():
    p=argparse.ArgumentParser(); p.add_argument("level",choices=["smoke","production","convergence"])
    p.add_argument("run_id"); a=p.parse_args()
    run=ROOT/"runs"/a.run_id; run.mkdir(parents=True,exist_ok=False)
    for d in ["raw","metrics","checkpoints","source"]: (run/d).mkdir()
    cfg=config(a.level)
    env=dict(os.environ,JAX_PLATFORMS="cpu",JAX_ENABLE_X64="true",MPLBACKEND="Agg")
    # All environment/device provenance is read-only; no environment changes.
    packages=json.loads(subprocess.check_output([sys.executable,"-m","pip","list","--format=json"],text=True))
    preflight=subprocess.check_output([sys.executable,"-c",
        "import BrainX,jax; assert jax.default_backend()=='cpu'; print(jax.default_backend(),jax.devices())"],env=env,text=True)
    identity={"interpreter":sys.executable,"packages":packages,"device_preflight":preflight,
        "platform":sys.platform,"precision":64,"JAX_PLATFORMS":"cpu","JAX_ENABLE_X64":"true",
        "data":"none; deterministic simulated input","checkpoint_source":None,
        "git":"not a git repository; full source snapshots and SHA256 supplied"}
    for source in SOURCES: shutil.copy2(ROOT/source,run/"source"/source)
    (run/"config.json").write_text(json.dumps(cfg,indent=2))
    (run/"environment.json").write_text(json.dumps(identity,indent=2))
    command=[sys.executable,str(run/"source/experiment.py"),"--config",str(run/"config.json")]
    (run/"command.txt").write_text("JAX_PLATFORMS=cpu JAX_ENABLE_X64=true "+" ".join(command)+"\n")
    (run/"code.diff").write_text("No git baseline. See source snapshots and source_hashes.json.\n")
    hashes={s:sha(run/"source"/s) for s in SOURCES}
    (run/"source_hashes.json").write_text(json.dumps(hashes,indent=2))
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (run/"RUN_SPEC.md").write_text(f"# {a.run_id}\nLevel: {a.level}; entry: new; start: {start}\n"
        f"Config SHA256: {sha(run/'config.json')}\nSpecification SHA256: {hashes['NeuroSpecification.md']}\n"
        "CPU float64, deterministic dynamics; surrogate seed 20261103. No empirical data.\n"
        "Expected: raw trajectories NPZ, runtime JSON, exit_code/log/status; non-smoke also derived NPZ, metrics JSON/CSV.\n"
        "Resource estimate: <2 GB RSS, <120 s runtime. Hard timeout 300 s; zero automatic retries.\n"
        "Stop on timeout, nonfinite/invalid State or artifact failure; preserve all outputs.\n"
        "Full histories are sampled at 1 kHz for analysis; no ongoing checkpoint/resume is needed for this short run.\n"
        "Mechanical completion does not imply scientific acceptance.\n")
    (run/"status.json").write_text(json.dumps({"status":"running","start":start}))
    with (run/"run.log").open("a") as log:
        try:
            proc=subprocess.Popen(command,cwd=run/"source",env=env,stdout=log,stderr=subprocess.STDOUT)
            (run/"process.json").write_text(json.dumps({"pid":proc.pid,"command":command,"cwd":str(run/"source")}))
            code=proc.wait(timeout=300)
        except subprocess.TimeoutExpired:
            proc.terminate(); code=proc.wait(timeout=10)
            log.write("Declared timeout reached; terminated.\n")
    (run/"exit_code").write_text(str(code)+"\n")
    expected=["raw/trajectories.npz","metrics/runtime.json"]
    if a.level!="smoke": expected += ["raw/derived.npz","metrics/metrics.json","metrics/metrics.csv"]
    complete=code==0 and all((run/f).is_file() for f in expected)
    if complete:
        import numpy as np
        with np.load(run/"raw/trajectories.npz") as data:
            complete=bool(np.isfinite(data["E"]).all() and np.isfinite(data["I"]).all())
    (run/"status.json").write_text(json.dumps({"status":"done" if complete else "failed",
        "start":start,"end":datetime.datetime.now(datetime.timezone.utc).isoformat(),"exit_code":code,
        "mechanical_complete":complete},indent=2))
    manifest={str(f.relative_to(run)):{"sha256":sha(f),"bytes":f.stat().st_size}
              for f in sorted(run.rglob("*")) if f.is_file() and f.name!="manifest.json"}
    (run/"manifest.json").write_text(json.dumps(manifest,indent=2))
    print(json.dumps({"run":str(run),"code":code,"complete":complete}),flush=True)
    sys.exit(0 if complete else 1)


if __name__=="__main__": main()
