"""First-principles endpoint LIF dynamics; no scientific example code used."""
import os
os.environ.setdefault('JAX_PLATFORMS', 'cpu')
import numpy as np
import scipy.sparse
import jax
import jax.numpy as jnp
import brainpy
import brainstate
import brainevent
import braintools
import brainunit as u

brainstate.environ.set_platform('cpu')

NE, NI, CE, CI, CEXT = 10000, 2500, 1000, 250, 1000
N = NE + NI
TAU, REF, DELAY = 20.0*u.ms, 2.0*u.ms, 1.5*u.ms
THRESHOLD, RESET, JE = 20.0*u.mV, 10.0*u.mV, 0.1*u.mV


def fixed_indegree_graph(seed, ne=NE, ni=NI, ce=CE, ci=CI):
    """Host construction boundary: exact uniform distinct incoming sources."""
    rng = np.random.default_rng(np.random.SeedSequence([seed, 1]))
    n = ne + ni
    matrices, checks = [], []
    for offset, ns, degree in [(0, ne, ce), (ne, ni, ci)]:
        sources = np.empty((n, degree), np.int32)
        for target in range(n):
            local = target-offset
            exclude = 0 <= local < ns
            draw = rng.choice(ns-int(exclude), degree, replace=False)
            if exclude:
                draw += draw >= local
            sources[target] = draw
        ordered = np.sort(sources, axis=1)
        unique = bool(np.all(np.diff(ordered, axis=1) > 0))
        no_self = bool(np.all(sources[offset:offset+ns] != np.arange(ns)[:, None]))
        # A CSC column is one target; convert to source-row CSR on the host.
        csc = scipy.sparse.csc_matrix(
            (np.ones(n*degree, np.float32), sources.ravel(),
             np.arange(n+1, dtype=np.int32)*degree), shape=(ns, n))
        csr = csc.tocsr()
        matrices.append((csr.indices.astype(np.int32), csr.indptr.astype(np.int32)))
        checks.append(dict(source_offset=offset, source_size=ns, degree=degree,
                           edges=int(csr.nnz), unique=unique, no_autapse=no_self,
                           exact_indegree=bool(np.all(np.asarray(csr.sum(axis=0)).ravel()==degree))))
        assert unique and no_self and checks[-1]['exact_indegree']
    return matrices, checks


def initial_voltage(seed, n=N):
    rng = np.random.default_rng(np.random.SeedSequence([seed, 2]))
    return rng.uniform(10., 20., n).astype(np.float32)


class EndpointLIF(brainpy.state.LIFRef):
    """Exact leak, endpoint deltas, hard reset, integer refractory release."""
    def __init__(self, initial_mV, dt_ms):
        super().__init__(len(initial_mV), tau=TAU, tau_ref=REF, V_rest=0.*u.mV,
                         V_th=THRESHOLD, V_reset=RESET,
                         V_initializer=braintools.init.Constant(u.math.asarray(initial_mV)*u.mV))
        self.ref_steps = int(round(float(REF.to_decimal(u.ms))/dt_ms))

    def init_state(self, batch_size=None):
        super().init_state(batch_size=batch_size)
        self.last_step = brainstate.ShortTermState(u.math.full(self.varshape, -1000000, dtype=jnp.int32))

    def update(self, step, external_jump):
        available = step-self.last_step.value >= self.ref_steps
        decayed = self.V.value*u.math.exp(-brainstate.environ.get_dt()/TAU)
        voltage = self.sum_delta_inputs(decayed+external_jump)
        voltage = u.math.where(available, voltage, RESET)
        spikes = (voltage >= THRESHOLD) & available
        self.V.value = u.math.where(spikes, RESET, voltage)
        self.last_step.value = u.math.where(spikes, step, self.last_step.value)
        return spikes


class RecurrentCommunication(brainstate.nn.Module):
    def __init__(self, matrices, ne, ni):
        super().__init__()
        n=ne+ni
        self.ne=ne
        self.e=brainevent.CSR((u.math.asarray(1.,dtype=jnp.float32),
                              u.math.asarray(matrices[0][0]),u.math.asarray(matrices[0][1])),shape=(ne,n))
        self.i=brainevent.CSR((u.math.asarray(1.,dtype=jnp.float32),
                              u.math.asarray(matrices[1][0]),u.math.asarray(matrices[1][1])),shape=(ni,n))
        self.g=brainstate.LongTermState(u.math.asarray(3.,dtype=jnp.float32))

    def update(self, spikes):
        e=brainevent.BinaryArray(spikes[:self.ne]) @ self.e
        i=brainevent.BinaryArray(spikes[self.ne:]) @ self.i
        return JE*(e-self.g.value*i)


class IndependentPoissonDrive(brainstate.nn.Module):
    def __init__(self,n):
        super().__init__()
        self.n=n

    def update(self,eta):
        frequency=eta*THRESHOLD/(JE*CE*TAU)
        expectation=u.math.asarray(CEXT*frequency*brainstate.environ.get_dt())
        return brainstate.random.poisson(expectation,size=(self.n,))*JE


class Network(brainstate.nn.Module):
    def __init__(self,matrices,initial_mV,dt_ms,ne=NE,ni=NI):
        super().__init__()
        self.ne,self.n=ne,ne+ni
        self.dt_ms=dt_ms
        self.delay_steps=int(round(float(DELAY.to_decimal(u.ms))/dt_ms))
        self.pop=EndpointLIF(initial_mV,dt_ms)
        self.comm=RecurrentCommunication(matrices,ne,ni)
        self.proj=brainpy.state.DeltaProj(comm=self.comm,post=self.pop)
        self.drive=IndependentPoissonDrive(self.n)
        self.delay=brainstate.nn.Delay(jax.ShapeDtypeStruct((self.n,),jnp.bool_),DELAY)

    def update(self,step,eta):
        # Latest buffer entry is the previous emitted endpoint, not the current
        # one. Offset D-1 therefore delivers spikes emitted exactly D steps ago.
        arriving=self.delay.retrieve_at_step(u.math.asarray(self.delay_steps-1,dtype=jnp.int32))
        self.proj(arriving)
        spikes=self.pop(step,self.drive(eta))
        self.delay.update(spikes)
        # Pure observation boundary: lossless bit packing, no state feedback.
        return jnp.packbits(spikes,bitorder='little'),u.math.stack([
            u.math.sum(spikes[:self.ne]),u.math.sum(spikes[self.ne:])])


def make_runner(net,steps):
    indices=u.math.arange(steps,dtype=jnp.int32)
    @brainstate.transform.jit
    def run(g,eta):
        net.comm.g.value=u.math.asarray(g,dtype=jnp.float32)
        return brainstate.transform.for_loop(lambda step:net(step,eta),indices)
    return run


def unpack_spikes(packed,n=N):
    return np.unpackbits(packed,axis=1,count=n,bitorder='little').astype(bool)
