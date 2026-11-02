import hashlib
import json
from pathlib import Path
import numpy as np

root=Path("runs/alpha-production-20261102-i3-dt005")
config=json.loads((root/"config.json").read_text())
checks=json.loads((root/"convergence.json").read_text())["checks"]
assert len(checks)==32 and all(c["pass"] for c in checks)
assert {(c["condition_index"],c["initial_index"]) for c in checks}=={(i,j) for i in range(4) for j in range(8)}
summary={}
for filename,dt in [("results.npz",0.05),("half_step_results.npz",0.025)]:
    with np.load(root/filename) as saved:
        assert saved["eeg_mv"].shape==(round(6000/dt),4,8)
        assert saved["eeg_mv"].dtype==np.float64
        assert all(np.isfinite(saved[k]).all() for k in ["eeg_mv","excitatory_psp_mv","inhibitory_psp_mv"])
        residual=np.max(np.abs(saved["eeg_mv"]-(saved["excitatory_psp_mv"]-saved["inhibitory_psp_mv"])))
        assert residual<=1e-9
        assert np.max(np.abs(saved["eeg_mv"]))<100
        stride=round(1/dt);first=round(2000/dt)+stride-1
        time=saved["times_s"][first::stride]
        np.testing.assert_allclose(time,np.arange(2001,6001)/1000,atol=1e-12,rtol=0)
        traces=saved["eeg_mv"][first::stride]
        computed=np.sqrt(np.mean((traces-traces.mean(axis=0))**2,axis=0))
        np.testing.assert_allclose(computed,saved["rms_mv"],atol=1e-12,rtol=1e-12)
        summary[filename]={"shape":list(saved["eeg_mv"].shape),"component_error_mv":float(residual),
            "max_abs_eeg_mv":float(np.max(np.abs(saved["eeg_mv"]))),"common_analysis_samples":len(time)}
with np.load(root/"half_step_results.npz") as fine,np.load("runs/numerical-diagnostic-i3-dt0025/results.npz") as diagnostic:
    for key in fine.files: np.testing.assert_array_equal(fine[key],diagnostic[key])
manifest=json.loads((root/"artifact_manifest.json").read_text())
for name,digest in manifest["sha256"].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
for path in root.glob("*.json"):
    json.loads(path.read_text(),parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
summary.update(all_32_convergence_checks=True,half_step_matches_independent_diagnostic=True,
    artifact_hashes_valid=True,strict_json_valid=True)
Path("saved-evidence-verification-i3.json").write_text(json.dumps(summary,indent=2)+"\n")
print("PASS: complete raw arrays, common physical sampling, RMS, finite/bound/component checks, full-grid convergence, independent replicate and hashes")
