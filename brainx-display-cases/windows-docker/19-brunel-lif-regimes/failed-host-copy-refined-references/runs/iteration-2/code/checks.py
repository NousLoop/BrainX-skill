"""Focused checks against independent small arithmetic references."""
import json
import time
from pathlib import Path
import numpy as np
import jax
import brainstate
import brainunit as u
import model


def component_checks():
    results={}
    for dt in [.1,.05]:
        with brainstate.environ.context(dt=dt*u.ms):
            cell=model.EndpointLIF(np.array([12.,19.9],np.float32),dt)
            brainstate.nn.init_all_states(cell)
            cell(0,u.math.asarray([0.,0.])*u.mV)
            first=np.asarray(cell.V.value.to_decimal(u.mV))
            expected=12*np.exp(-dt/20)
            assert np.isclose(first[0],expected,atol=3e-6)
            # Second cell needs a jump exceeding its leaked distance to threshold.
            cell.V.value=u.math.asarray([12.,19.9])*u.mV
            cell(1,u.math.asarray([0.,1.])*u.mV)
            assert float(cell.V.value.to_decimal(u.mV)[1])==10.
            last=np.asarray(cell.last_step.value)
            assert last[1]==1
            ref=int(round(2/dt))
            spikes=brainstate.transform.for_loop(
                lambda i:cell(i,u.math.asarray([0.,100.])*u.mV),
                u.math.arange(2,ref+3))
            fired=np.flatnonzero(np.asarray(spikes)[:,1])+2
            assert fired.tolist()==[1+ref]
            results[f'leak_threshold_refractory_dt{dt}']=dict(leak_mV=float(first[0]),
                expected_mV=float(expected),last_spike_step=1,next_spike_step=int(fired[0]),pass_=True)

            graph,_=model.fixed_indegree_graph(991,ne=10,ni=5,ce=3,ci=2)
            net=model.Network(graph,np.full(15,10.,np.float32),dt,ne=10,ni=5)
            brainstate.nn.init_all_states(net)
            dense=[]
            import scipy.sparse
            for (indices,indptr),ns in zip(graph,[10,5]):
                dense.append(scipy.sparse.csr_matrix((np.ones(len(indices)),indices,indptr),shape=(ns,15)).toarray())
            event=np.arange(15)%3==0
            actual=np.asarray(net.comm(u.math.asarray(event)).to_decimal(u.mV))
            expected=.1*(event[:10]@dense[0]-3*(event[10:]@dense[1]))
            assert np.allclose(actual,expected,atol=2e-7)

            # Isolated event through production buffer -> DeltaProj -> membrane.
            impulse=u.math.zeros((net.delay_steps+4,15),dtype=bool).at[1,0].set(True)
            def route(events):
                arriving=net.delay.retrieve_at_step(u.math.asarray(net.delay_steps-1))
                net.proj(arriving)
                delta=net.pop.sum_delta_inputs(0.*u.mV)
                net.delay.update(events)
                return delta
            response=np.asarray(brainstate.transform.for_loop(route,impulse).to_decimal(u.mV))
            active=np.flatnonzero(np.any(response!=0,axis=1))
            assert active.tolist()==[1+net.delay_steps]
            assert np.allclose(response[active[0]],.1*dense[0][0],atol=1e-8)
            results[f'event_delta_delay_dt{dt}']=dict(input_step=1,arrival_step=int(active[0]),
                latency_ms=float((active[0]-1)*dt),event_product_parity=True,pass_=True)

            # Independent explicit small-network reference, prescribed jumps.
            # Tiny reference loops here are test arithmetic, never production.
            brainstate.nn.init_all_states(net)
            ext=np.random.default_rng(74).poisson(2.,size=(250,15)).astype(np.float32)*.1
            ext[0,:]=25.
            def step(i,jump):
                arriving=net.delay.retrieve_at_step(u.math.asarray(net.delay_steps-1))
                net.proj(arriving)
                spk=net.pop(i,jump*u.mV)
                net.delay.update(spk)
                return spk,net.pop.V.value
            indices=u.math.arange(len(ext))
            baseline=brainstate.transform.for_loop(step,indices,u.math.asarray(ext))
            brainstate.nn.init_all_states(net)
            compiled=brainstate.transform.jit(lambda:brainstate.transform.for_loop(step,indices,u.math.asarray(ext)))()
            sp,vol=np.asarray(compiled[0]),np.asarray(compiled[1].to_decimal(u.mV))
            assert np.array_equal(sp,np.asarray(baseline[0]))
            assert np.allclose(vol,np.asarray(baseline[1].to_decimal(u.mV)),atol=1e-6)
            v=np.full(15,10.,np.float64);last=np.full(15,-1000000)
            hist=np.zeros((len(ext),15),bool);vs=[]
            for i in range(len(ext)):
                arriving=hist[i-net.delay_steps] if i>=net.delay_steps else np.zeros(15,bool)
                rec=.1*(arriving[:10]@dense[0]-3*(arriving[10:]@dense[1]))
                v=v*np.exp(-dt/20)+rec+ext[i]
                available=i-last>=int(round(2/dt))
                v=np.where(available,v,10.)
                hist[i]=(v>=20)&available
                last=np.where(hist[i],i,last)
                v=np.where(hist[i],10.,v)
                vs.append(v.copy())
            error=float(np.max(np.abs(vol-np.array(vs))))
            assert np.array_equal(sp,hist)
            assert error<.001
            results[f'compiled_reference_dt{dt}']=dict(max_voltage_error_mV=error,
                spikes_identical=True,stateful_jit_parity=True,pass_=True)

    with brainstate.environ.context(dt=.1*u.ms):
        brainstate.random.seed(711)
        drive=model.IndependentPoissonDrive(300000)
        counts=np.asarray(brainstate.transform.jit(drive)(2.).to_decimal(u.mV))/.1
        assert abs(counts.mean()-2)<.02 and abs(counts.var()-2)<.04
        corr=float(np.corrcoef(counts[:150000],counts[150000:])[0,1])
        assert abs(corr)<.015
        multi=float(np.mean(counts>=1.9))
        assert abs(multi-(1-3*np.exp(-2)))<.01
        results['poisson']=dict(mean=float(counts.mean()),variance=float(counts.var()),
            expectation=2.,cross_target_correlation=corr,multiple_fraction=multi,pass_=True)
        brainstate.random.seed(711)
        again=np.asarray(brainstate.transform.jit(drive)(2.).to_decimal(u.mV))/.1
        assert np.array_equal(counts,again)
        results['rng_replay']=dict(identical=True,pass_=True)
    try:
        _=1*u.ms+1*u.mV
    except Exception:
        results['unit_mismatch_rejected']=True
    else:
        raise AssertionError('unit mismatch accepted')
    return results


def benchmark():
    graph,checks=model.fixed_indegree_graph(101)
    np.savez_compressed('checks/graph_seed101.npz',e_indices=graph[0][0],e_indptr=graph[0][1],
                         i_indices=graph[1][0],i_indptr=graph[1][1])
    with brainstate.environ.context(dt=.1*u.ms):
        net=model.Network(graph,model.initial_voltage(101),.1)
        brainstate.nn.init_all_states(net)
        snapshot={path:state.value for path,state in net.states().items()}
        runner=model.make_runner(net,500)
        brainstate.random.seed(101)
        start=time.perf_counter();out=runner(3.,2.);jax.block_until_ready(out);cold=time.perf_counter()-start
        raw=np.asarray(out[0]);counts=np.asarray(out[1]);v=np.asarray(net.pop.V.value.to_decimal(u.mV))
        unexpected,missing=brainstate.nn.assign_state_values(net,snapshot)
        assert not unexpected and not missing
        brainstate.random.seed(101)
        start=time.perf_counter();warm=runner(3.,2.);jax.block_until_ready(warm);elapsed=time.perf_counter()-start
        assert np.array_equal(raw,np.asarray(warm[0]))
        assert np.array_equal(counts,np.asarray(warm[1]))
        assert np.array_equal(v,np.asarray(net.pop.V.value.to_decimal(u.mV)))
        np.savez_compressed('checks/full_size_smoke.npz',packed=raw,counts=counts,final_mV=v)
        return dict(ne=model.NE,ni=model.NI,steps=500,dt_ms=.1,graph_checks=checks,
                    cold_seconds=cold,warm_seconds=elapsed,spikes=int(counts.sum()),
                    exact_replay=True,finite=bool(np.isfinite(v).all()),
                    estimate_4000ms_seconds=elapsed*80)


if __name__=='__main__':
    Path('checks').mkdir(exist_ok=True)
    results=component_checks()
    Path('checks/components.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2),flush=True)
    bench=benchmark()
    Path('checks/acceleration.json').write_text(json.dumps(bench,indent=2))
    print(json.dumps(bench,indent=2),flush=True)
