import time,json
import jax.numpy as jnp
import numpy as np
import brainstate
import brainunit as u
import model
brainstate.environ.set_platform('cpu')
results={}
with brainstate.environ.context(dt=.1*u.ms):
 drive=model.PoissonDrive(12500,11,.1*u.ms)
 rng=brainstate.random.RandomState(11)
 def poisson_body(i):
  return u.math.sum(drive(jnp.array(2.0)))
 def rng_body(i):
  return u.math.sum(rng.random((12500,)))
 graphs,_=model.make_graph(11)
 comm=model.SparseDelta(graphs,10000,2500)
 spikes=jnp.arange(12500)%20==0
 def comm_body(i):
  return u.math.sum(comm(spikes))
 for name,body in [('poisson',poisson_body),('uniform',rng_body),('communication',comm_body)]:
  f=brainstate.transform.jit(lambda:brainstate.transform.for_loop(body,jnp.arange(1000)))
  f.compile()
  t=time.perf_counter();ans=f();np.asarray(u.math.asarray(ans/u.mV) if name!='uniform' else ans)
  results[name]=time.perf_counter()-t
print(json.dumps(results),flush=True)
