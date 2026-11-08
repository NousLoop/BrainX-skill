"""First-principles endpoint LIF dynamics; see the locked NeuroSpecification."""
import brainpy
import brainstate
import brainevent
import brainunit as u
import jax
import jax.numpy as jnp
import numpy as np
import scipy.sparse

NE, NI = 10_000, 2_500
N = NE + NI
CE, CI, CEXT = 1_000, 250, 1_000
TAU, REF, DELAY = 20.0 * u.ms, 2.0 * u.ms, 1.5 * u.ms
THETA, RESET, JE = 20.0 * u.mV, 10.0 * u.mV, 0.1 * u.mV


def make_graph(seed, ne=NE, ni=NI, ce=CE, ci=CI):
    """Host-only quenched topology: exact, distinct incoming E/I sources."""
    rng = np.random.default_rng(np.random.SeedSequence([seed, 1]))
    n = ne + ni
    graphs, checks = [], []
    for offset, size, degree in [(0, ne, ce), (ne, ni, ci)]:
        incoming = np.empty((n, degree), dtype=np.int32)
        for post in range(n):  # Topology construction, never simulation time.
            local = post - offset
            exclude = 0 <= local < size
            sources = rng.choice(size - int(exclude), degree, replace=False)
            if exclude:
                sources += sources >= local
            incoming[post] = np.sort(sources)
        assert np.all(np.diff(incoming, axis=1) > 0)
        assert not np.any(incoming == (np.arange(n) - offset)[:, None])
        # Incoming rows are CSC columns of the pre-by-post communication matrix.
        csc = scipy.sparse.csc_matrix(
            (np.ones(n * degree, np.uint8), incoming.ravel(),
             np.arange(n + 1, dtype=np.int32) * degree), shape=(size, n))
        csr = csc.tocsr()
        assert np.all(np.bincount(csr.indices, minlength=n) == degree)
        graphs.append((csr.indices.copy(), csr.indptr.copy()))
        checks.append(dict(source_size=size, degree=degree, edges=n * degree,
                           duplicates=0, autapses=0, all_indegrees_exact=True))
    return graphs, checks


class DeltaLIF(brainpy.state.Dynamics):
    """Exact leak plus endpoint delta arrivals and an absolute refractory clamp."""
    def __init__(self, initial_voltage, dt):
        super().__init__(initial_voltage.shape[0])
        self.initial_voltage = initial_voltage
        self.decay = u.math.exp(-dt / TAU)
        self.ref_steps = int(round(float((REF / dt))))

    def init_state(self, **kwargs):
        self.V = brainstate.HiddenState(self.initial_voltage)
        self.last = brainstate.ShortTermState(
            jnp.full(self.initial_voltage.shape, -1_000_000, dtype=jnp.int32))
        self.spike = brainstate.ShortTermState(
            jnp.zeros(self.initial_voltage.shape, dtype=bool))

    def update(self, step, external_jump):
        elapsed = step - self.last.value
        active = elapsed >= self.ref_steps
        # At refractory expiry the preceding interval was still clamped.
        leaked = u.math.where(elapsed > self.ref_steps,
                              self.V.value * self.decay, RESET)
        voltage = leaked + self.sum_delta_inputs(external_jump)
        voltage = u.math.where(active, voltage, RESET)
        spike = active & (voltage >= THETA)
        self.V.value = u.math.where(spike, RESET, voltage)
        self.last.value = jnp.where(spike, step, self.last.value)
        self.spike.value = spike
        return spike


class PoissonDrive(brainstate.nn.Module):
    """Exact superposition of independent external sources on the time grid."""
    def __init__(self, size, seed, dt):
        super().__init__()
        self.size, self.dt = size, dt
        self.rng = brainstate.random.RandomState(seed + 100_003)

    def update(self, eta):
        nu_ext = eta * THETA / (JE * CE * TAU)
        # BrainUnit automatically unwraps a dimensionless product.
        mean = u.math.asarray(CEXT * nu_ext * self.dt)
        return self.rng.poisson(mean, size=(self.size,)) * JE


class SparseDelta(brainstate.nn.Module):
    def __init__(self, graphs, ne, ni):
        super().__init__()
        self.ne = ne
        self.exc = brainevent.CSR(
            (jnp.array(1.0), jnp.asarray(graphs[0][0]), jnp.asarray(graphs[0][1])),
            shape=(ne, ne + ni))
        self.inh = brainevent.CSR(
            (jnp.array(1.0), jnp.asarray(graphs[1][0]), jnp.asarray(graphs[1][1])),
            shape=(ni, ne + ni))
        self.gain = brainstate.ShortTermState(jnp.array(1.0, dtype=jnp.float32))

    def update(self, spikes):
        exc_count = brainevent.BinaryArray(spikes[:self.ne]) @ self.exc
        inh_count = brainevent.BinaryArray(spikes[self.ne:]) @ self.inh
        return (exc_count - self.gain.value * inh_count) * JE


class Network(brainstate.nn.Module):
    def __init__(self, graphs, initial_voltage, seed, dt, ne=NE, ni=NI):
        super().__init__()
        self.ne, self.ni = ne, ni
        self.seed = seed
        self.dt = dt
        self.delay_steps = int(round(float(DELAY / dt)))
        self.pop = DeltaLIF(initial_voltage, dt)
        self.drive = PoissonDrive(ne + ni, seed, dt)
        self.comm = SparseDelta(graphs, ne, ni)
        # Eagerly initialize the public sparse operator before tracing it.
        # Otherwise its lazily allocated workspace can retain a dead tracer
        # when BrainState compiles a second static condition.
        self.comm(jnp.zeros(ne + ni, dtype=bool))
        self.proj = brainpy.state.DeltaProj(comm=self.comm, post=self.pop)
        self.delay = brainstate.nn.Delay(
            jax.ShapeDtypeStruct((ne + ni,), jnp.bool_), DELAY)

    def update(self, step, g, eta):
        # Buffer receives spike[n-1] at step n. Its offset D-1 is spike[n-D].
        # Thus a spike at endpoint t reaches the neuron exactly at t+D*dt.
        self.delay.update(self.pop.spike.value)
        delayed = self.delay.retrieve_at_step(jnp.asarray(self.delay_steps - 1))
        self.comm.gain.value = g
        self.proj(delayed)
        spikes = self.pop(step, self.drive(eta))
        return jnp.packbits(spikes, bitorder='little')

    def rollout(self, indices, g, eta):
        return brainstate.transform.for_loop(
            lambda i: self.update(i, g, eta), indices)


def initial_state(seed, n=N):
    rng = np.random.default_rng(np.random.SeedSequence([seed, 2]))
    return jnp.asarray(rng.uniform(0, 20, n), dtype=jnp.float32) * u.mV


def snapshot_states(net):
    """Capture immutable values while preserving registered State identities."""
    return [(state, state.value) for state in net.states().values()]


def restore_states(snapshot):
    for state, value in snapshot:
        state.value = value
