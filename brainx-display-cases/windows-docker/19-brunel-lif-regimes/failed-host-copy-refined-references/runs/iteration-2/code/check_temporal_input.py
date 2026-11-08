"""Verify temporal independence through the production State-aware transforms."""
import json
from pathlib import Path
import numpy as np
import brainstate
import brainunit as u
import model


def main():
    with brainstate.environ.context(dt=.1*u.ms):
        drive=model.IndependentPoissonDrive(128)
        brainstate.random.seed(842)
        @brainstate.transform.jit
        def rollout():
            return brainstate.transform.for_loop(lambda _:drive(2.),u.math.arange(2000))
        initial=np.asarray(brainstate.random.get_key_data()).copy()
        counts=np.rint(np.asarray(rollout().to_decimal(u.mV))/.1).astype(np.int32)
        final=np.asarray(brainstate.random.get_key_data()).copy()
        corr=float(np.corrcoef(counts[:-1].ravel(),counts[1:].ravel())[0,1])
        assert counts.shape==(2000,128)
        assert abs(counts.mean()-2)<.02 and abs(counts.var()-2)<.04
        assert abs(corr)<.02 and np.all(counts.std(axis=0)>1)
        assert not np.array_equal(initial,final)
        result=dict(pass_=True,mean=float(counts.mean()),variance=float(counts.var()),
            temporal_lag1_correlation=corr,min_per_neuron_temporal_sd=float(counts.std(axis=0).min()),
            rng_state_advanced=True,steps=2000,targets=128,
            transform='brainstate.transform.jit(brainstate.transform.for_loop)',
            purpose='exclude accidentally frozen Poisson draws over time; input-law check only')
        Path('checks/temporal_poisson.json').write_text(json.dumps(result,indent=2))
        print(result)


if __name__=='__main__':main()
