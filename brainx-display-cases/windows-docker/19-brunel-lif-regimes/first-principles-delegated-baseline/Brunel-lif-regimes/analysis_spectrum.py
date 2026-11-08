"""The frozen Welch estimator through BrainTools' configurable spectrogram."""
import braintools
import brainunit as u
import numpy as np


def global_rate_spectrum(rate_Hz, dt_ms):
    nperseg=round(1000/dt_ms)
    frequency,_,segments=braintools.analysis.spectral.spectrogram(
        rate_Hz*u.Hz,dt=dt_ms*u.ms,nperseg=nperseg,noverlap=nperseg//2,
        window='hann',detrend='constant')
    # Welch is the mean of the documented per-segment power spectra.
    psd=np.asarray(u.math.mean(segments,axis=1).to_decimal(u.Hz))
    # Serialize the physical FFT bin centers exactly; verify the API grid first.
    grid=np.arange(len(psd))*(1000/dt_ms)/nperseg
    assert np.allclose(frequency,grid,rtol=1e-6,atol=1e-5)
    return grid,psd
