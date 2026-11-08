"""Replayable periodic-spike metric fixture; preserve input independently."""
import hashlib
import json
from pathlib import Path
import numpy as np
import analysis


def main():
    root=Path('checks/metrics_fixture_v2')
    inp=root/'input';out=root/'output';inp.mkdir(parents=True,exist_ok=True)
    path=inp/'periodic_spikes.npz'
    if not path.exists():
        sp=np.zeros((40000,15),bool);sp[::100]=True
        np.savez_compressed(path,packed=np.packbits(sp,axis=1,bitorder='little'),
            counts=np.stack([sp[:,:10].sum(axis=1),sp[:,10:].sum(axis=1)],axis=1),
            dt_ms=.1,steps=40000,ne=10,ni=5,condition=0,seed=0,g=3.,eta=2.)
    before=hashlib.sha256(path.read_bytes()).hexdigest()
    result=analysis.summarize(path,out)
    expected=(48.75**.5)/7.5
    assert result['E_rate_Hz']==100 and result['I_rate_Hz']==100 and result['CV_median']==0
    assert abs(result['synchrony_S']-expected)<1e-12
    assert result['dominant_frequency_Hz']==100 and result['oscillation_supported']
    assert result['baseline_outcome']=='supported'
    try:analysis.summarize(path,inp)
    except ValueError:collision_guard=True
    else:raise AssertionError('Input/output collision was accepted')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==before
    assert {'packed','counts','dt_ms','steps','ne','ni'}.issubset(np.load(path).files)
    evidence=dict(pass_=True,input_sha256=before,raw_input=str(path),derived_output=str(out),
        collision_guard=collision_guard,input_unchanged=True,expected_rate_Hz=100.,expected_CV=0.,
        expected_S=expected,expected_frequency_Hz=100.,result=result,
        scientific_status='synthetic arithmetic test only, not production simulation evidence')
    (root/'test_result.json').write_text(json.dumps(evidence,indent=2))
    print(json.dumps(evidence,indent=2))


if __name__=='__main__':main()
