"""BrainTools filtering/PSD, explicit host observation and known-phase statistics."""
import braintools
import brainunit as u
import jax
import numpy as np


def envelope(x, dt_s):
    filtered = braintools.analysis.spectral.bandpass(x, dt=dt_s*u.second, band=(25.,90.), order=4)
    return np.asarray(u.math.abs(braintools.analysis.spectral.analytic_signal(filtered))), np.asarray(filtered)


def psd(x, dt_s):
    f, p = braintools.analysis.spectral.power_spectral_density(
        x, dt=dt_s*u.second, nperseg=2000, noverlap=1000)
    return np.asarray(f), np.asarray(p)


def phase_metrics(amplitude, phase):
    """Host statistics: known phase, time is axis zero; 18 equal phase bins."""
    phasor = np.exp(1j*phase)
    vector = np.mean(amplitude*phasor.reshape((-1,)+(1,)*(amplitude.ndim-1)), axis=0)
    mean = amplitude.mean(axis=0)
    R = np.abs(vector)/np.maximum(mean, 1e-15)
    wrapped = (phase+np.pi)%(2*np.pi)-np.pi
    edges = np.linspace(-np.pi, np.pi, 19)
    index = np.minimum(np.searchsorted(edges, wrapped, side='right')-1,17)
    profile = np.stack([amplitude[index==b].mean(axis=0) for b in range(18)])
    prob = profile/np.maximum(profile.sum(axis=0), 1e-15)
    mi = np.sum(prob*np.log(np.maximum(prob*18,1e-15)), axis=0)/np.log(18)
    return dict(R=R, MI=mi, profile=profile, preferred_phase=np.angle(vector),
                bin_centers=(edges[1:]+edges[:-1])/2,
                bin_counts=np.bincount(index,minlength=18))


def cycle_surrogates(amplitude, phase, n=200, seed=20261106):
    """Exactly circularly rotate envelope samples independently within each cycle.

    FFT circular correlation computes every possible integer rotation's weighted
    sum without materializing surrogate trajectories. Unequal 166/167-sample
    cycles keep their original samples and phase coordinates. The test compares
    these sums with direct np.roll, including an incomplete-sampling phase grid.
    """
    cycle = np.floor((phase+1e-8)/(2*np.pi)).astype(int)
    ids = np.unique(cycle)
    rng = np.random.default_rng(seed)
    vectors = np.zeros((n,)+amplitude.shape[1:], dtype=complex)
    rotations = np.zeros((n,len(ids)),dtype=int)
    counts = []
    for j,c in enumerate(ids):
        k = cycle==c
        a = amplitude[k]
        w = np.exp(1j*phase[k]).reshape((-1,)+(1,)*(amplitude.ndim-1))
        # C[s] = sum_k a[k] * w[(k+s) mod L].
        correlation = np.fft.ifft(np.conj(np.fft.fft(a,axis=0))*np.fft.fft(w,axis=0),axis=0)
        shifts = rng.integers(0,k.sum(),n)
        rotations[:,j] = shifts
        vectors += correlation[shifts]
        counts.append(int(k.sum()))
    values = np.abs(vectors)/np.maximum(amplitude.sum(axis=0),1e-15)
    return values, rotations, np.asarray(counts)


def observations(raw, seeds):
    E,I,t = raw['rE'],raw['rI'],raw['t_s']
    noise = np.stack([np.random.default_rng(s).normal(0,0.02,len(t)) for s in seeds],axis=1)[:,:,None]
    theta = 0.15*np.cos(2*np.pi*6*t)[:,None,None]
    latent = E-0.5*I
    latent = latent-latent.mean(axis=0)
    eeg = latent+theta+noise
    eonly = E-E.mean(axis=0)+theta+noise
    leakage = np.broadcast_to(theta+noise,eeg.shape).copy()
    return dict(latent=latent,eeg=eeg,eonly=eonly,leakage=leakage,noise=noise,theta=theta)


def analyze(raw, seeds, window=(3.,13.)):
    t = raw['t_s']; dt=float(np.median(np.diff(t)))
    assert abs(dt-0.001)<1e-9
    obs=observations(raw,seeds)
    names=['E','latent','eeg','eonly','leakage']
    signals=np.stack([raw['rE'],obs['latent'],obs['eeg'],obs['eonly'],obs['leakage']],axis=-1)
    amp,band=envelope(signals,dt)
    keep=(t>=window[0])&(t<window[1]); phase=2*np.pi*6*t[keep]
    metrics=phase_metrics(amp[keep],phase)
    null,rotations,counts=cycle_surrogates(amp[keep],phase)
    metrics.update(gamma_rms=np.sqrt(np.mean(band[keep]**2,axis=0)),
                   null95=np.quantile(null,.95,axis=0),null_R=null,
                   null_rotations=rotations,cycle_counts=counts,
                   signal_names=np.asarray(names),window_mask=keep,
                   envelope=amp,band=band)
    f,p=psd(np.concatenate([raw['rE'][keep].reshape(keep.sum(),-1),obs['eeg'][keep].reshape(keep.sum(),-1)],axis=1),dt)
    n=raw['rE'].shape[1]*raw['rE'].shape[2]
    pE=p[:,:n].reshape(len(f),*raw['rE'].shape[1:]); pY=p[:,n:].reshape(pE.shape)
    inband=(f>=25)&(f<=90)
    peak=f[inband][np.argmax(pE[inband],axis=0)]
    peak=np.where(metrics['gamma_rms'][...,0]>.005,peak,np.nan)
    metrics.update(frequency_Hz=f,psd_E=pE,psd_eeg=pY,gamma_peak_Hz=peak)
    return obs,metrics
