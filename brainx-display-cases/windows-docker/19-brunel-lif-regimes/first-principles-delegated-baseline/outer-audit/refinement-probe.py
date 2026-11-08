import json
from pathlib import Path
import jax
jax.config.update('jax_enable_x64',True)
import jax.numpy as jnp
import numpy as np
import scipy.signal
import brainstate
import brainunit as u
import braintools
r=brainstate.random.RandomState(42)
x=r.randn(32); r.seed(42);np.testing.assert_array_equal(x,r.randn(32))
other=brainstate.random.RandomState(123);assert not np.array_equal(x,other.randn(32))
kw=brainstate.random.RandomState(seed_or_key=42);np.testing.assert_array_equal(x,kw.randn(32))
rejected=False
try:brainstate.random.RandomState(seed=42)
except TypeError:rejected=True
assert rejected
rng=brainstate.random.RandomState(11)
@brainstate.transform.jit
def draw():return rng.poisson(4.0,size=(64,))
saved=rng.value;y=draw();rng.value=saved;np.testing.assert_array_equal(y,draw())
t=np.arange(4096)*.001
signal=3+np.sin(2*np.pi*31.25*t)
f,centers,sxx=braintools.analysis.spectral.spectrogram(signal*u.mV,dt=1*u.ms,nperseg=256,noverlap=128,window='hann',detrend='constant')
psd=u.math.mean(sxx,axis=1).to_decimal(u.mV**2/u.Hz)
reference_f,reference_psd=scipy.signal.welch(signal,fs=1000,nperseg=256,noverlap=128,window='hann',detrend='constant')
np.testing.assert_allclose(f,reference_f,rtol=1e-12,atol=1e-12)
np.testing.assert_allclose(psd,reference_psd,rtol=1e-10,atol=1e-12)
assert sxx.shape==(129,31)
assert float(f[np.argmax(psd)])==31.25
result=dict(positional_constructor=True,seed_or_key_constructor=True,seed_keyword_rejected=True,independent_streams=True,reseed_replay=True,compiled_stream_replay=True,segment_axis_shape=list(sxx.shape),quantity_psd_conversion=True,welch_parity=True,maximum_psd_abs_error=float(np.max(abs(psd-reference_psd))))
Path('/audit/refinement-probe.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
