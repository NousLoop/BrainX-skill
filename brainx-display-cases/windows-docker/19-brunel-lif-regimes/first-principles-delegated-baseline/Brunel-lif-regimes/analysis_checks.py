"""Known-signal checks for event decoding, ISI statistics and spectral units."""
import json
from pathlib import Path
import numpy as np
import experiment

results={}
spikes=np.zeros((30000,24),dtype=bool)
spikes[::50]=True
packed=np.packbits(spikes,axis=1,bitorder='little')
metrics,data=experiment.summarize_spikes(packed,.1,ne=16,ni=8)
assert metrics['label']=='synchronous regular'
assert metrics['E_Hz']==200 and metrics['I_Hz']==200
assert np.all(data['ISI_CV']==0)
assert np.all(data['ISI_count']==599)
assert metrics['dominant_Hz'] in [200,400,600,800,1000]  # Exact impulse-train harmonics.
results['regular_known_event_train']=metrics

t=(np.arange(30000)+1)*.0001
for frequency in [23,120]:
    rate=100+40*np.sin(2*np.pi*frequency*t)
    counts=rate[:,None]*np.array([10000,2500])[None,:]*.0001
    m,_,_=experiment.assess(counts,np.ones(12500),.1)
    assert m['dominant_Hz']==frequency
    assert m['label']==('slow' if frequency<50 else 'fast')+' synchronous irregular'
    results[f'known_{frequency}Hz_signal']=m

rng=np.random.default_rng(907)
counts=rng.poisson(np.array([10,2.5]),size=(30000,2))
m,_,_=experiment.assess(counts,np.ones(12500),.1)
assert m['label']=='asynchronous irregular'
results['independent_Poisson_count_fixture']=m
Path('analysis_checks.json').write_text(json.dumps(results,indent=2))
print('Known event rates, CV, count decoding, sinusoid frequency/Hz units and asynchronous count fixture: PASS')
