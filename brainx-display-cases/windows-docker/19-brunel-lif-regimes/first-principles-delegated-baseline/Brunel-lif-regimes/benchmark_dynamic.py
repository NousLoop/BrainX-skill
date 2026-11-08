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
 @brainstate.transform.jit
 def f(eta):
  return brainstate.transform.for_loop(lambda i:u.math.sum(drive(eta)),jnp.arange(1000))
 f.compile(jnp.array(2.0))
 t=time.perf_counter();np.asarray(f(jnp.array(2.0)).to_decimal(u.mV));results['dynamic_poisson']=time.perf_counter()-t
 graphs,_=model.make_graph(11)
 net=model.Network(graphs,model.initial_state(11),11,.1*u.ms)
 brainstate.nn.init_all_states(net)
 @brainstate.transform.jit
 def full(g,eta):
  return net.rollout(jnp.arange(1000),g,eta)
 full.compile(jnp.array(3.0),jnp.array(2.0))
 t=time.perf_counter();np.asarray(full(jnp.array(3.0),jnp.array(2.0)));results['full']=time.perf_counter()-t
print(json.dumps(results),flush=True)
