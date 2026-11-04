"""Exact config consumer; raw outputs saved before offline metrics."""
import argparse
import csv
import json
from pathlib import Path
import resource
import time

import numpy as np
import model
import analysis
import braintools
import brainunit as u


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",required=True)
    args=parser.parse_args()
    path=Path(args.config).resolve(); run=path.parent
    cfg=json.loads(path.read_text())
    print("run",run.name,"config",cfg,flush=True)
    start=time.perf_counter()
    raw=model.run_model(cfg)
    elapsed=time.perf_counter()-start
    np.savez_compressed(run/"raw/trajectories.npz",**raw)
    print("raw saved",raw["E"].shape,"simulation end-to-end s",elapsed,flush=True)
    for key in ["E","I"]:
        if not (np.isfinite(raw[key]).all() and (raw[key]>=0).all() and (raw[key]<=1).all()):
            raise ValueError("invalid state "+key)
    if cfg["level"]=="smoke":
        c=int(np.flatnonzero((raw["depths_flat"]==0)&(raw["gains_flat"]==1))[0])
        witnesses=[]
        for rep in range(len(cfg["initial_e"])):
            for pop in ["E","I"]:
                x=raw[pop][:,rep,c]
                fq,power=braintools.metric.power_spectral_density(x,.001*u.second,nperseg=cfg["nperseg"])
                witness=analysis.carrier_features(x,raw["t_s"],np.asarray(fq),np.asarray(power),cfg)
                witness.update({"pop":pop,"rep":rep})
                witnesses.append(witness)
        (run/"metrics/smoke_carrier.json").write_text(json.dumps(witnesses,indent=2))
        if not all(w["autonomous_gamma_predicate"] for w in witnesses):
            raise ValueError("Smoke failed autonomous gamma carrier predicate; retain evidence, no production")
    if cfg["level"]!="smoke":
        rows,derived=analysis.analyze(raw,cfg)
        np.savez_compressed(run/"raw/derived.npz",**derived)
        (run/"metrics/metrics.json").write_text(json.dumps(rows,indent=2,allow_nan=False))
        with (run/"metrics/metrics.csv").open("w") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
        print("metrics saved",len(rows),flush=True)
    runtime={"simulation_end_to_end_s":elapsed,"total_s":time.perf_counter()-start,
             "max_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             "state_dtype":str(raw["E"].dtype),"raw_shape":list(raw["E"].shape),
             "min_E":float(raw["E"].min()),"max_E":float(raw["E"].max()),
             "min_I":float(raw["I"].min()),"max_I":float(raw["I"].max())}
    (run/"metrics/runtime.json").write_text(json.dumps(runtime,indent=2))
    print(json.dumps(runtime),flush=True)


if __name__=="__main__":
    main()
