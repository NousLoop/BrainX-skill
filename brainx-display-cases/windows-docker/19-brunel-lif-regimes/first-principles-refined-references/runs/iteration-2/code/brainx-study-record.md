# BrainX mechanics study, iteration 1

Completed before model/experiment implementation. Scientific source: task text and first-principles derivation only.

Read in full: brainx-general-guard, brainx-modeling-loop, brainpy-state, brainevent, brainstate, brainunit, brainx-install (presence routing only), brainx-acceleration; package references component-selection, projection-patterns, brain-dynamics-delay-protocol, braintools/connectivity, sparse-formats, randomness-and-reproducibility and brainstate-control-flow-patterns; acceleration audit-and-rewrite-patterns; workflow run-experiment and monitor-experiment. Scientific scripts mentioned by these files were deliberately not opened, under the researcher's overriding restriction.

Public API contracts checked: BrainState random.poisson(lam,size,key), and Dynamics sum_delta_inputs(init,...) / add_delta_input(key,inp,...). Some BrainPy API URLs returned HTTP 403/404; the Dynamics URL redirected to BrainSpikes documentation exposing the shared input interface. No source links were followed. The task-relevant signatures for LIFRef, DeltaProj, Delay and CSR are also specified explicitly in the installed skills. Use small execution probes, not installed source introspection. Imported required packages successfully; native brainpy.state.LIFRef constructed and initialized. A unit-boundary probe showed that a fully canceled quantity returns a plain scalar; use u.math.asarray on the dimensionless expectation rather than calling a Quantity-only method.

## Implementation design
- One native BrainPy-State LIFRef subclass stores identical E/I cell equations in a contiguous vector (E then I); override only the endpoint transition to enforce the explicitly frozen exponential/jump/threshold/refractory convention. Native V initialization, Module graph, delta input collection and DeltaProj lifecycle remain in use. Integer last-spike steps avoid floating-point equality at refractory release.
- One DeltaProj deposits JE*(E incoming count - g*I incoming count). Its communication Module uses BinaryArray @ two explicit CSR matrices with scalar unitless one weights, then attaches voltage units to communicated counts. No synaptic filter State is introduced for delta events.
- brainstate.nn.Delay stores binary emitted spikes. At entry to transition i (endpoint (i+1)*dt), its newest sample is the previous endpoint i*dt; retrieve offset D-1 to obtain (i+1-D)*dt, then update with the newly emitted spike after the transition. Prove the full latency with an impulse test at both dt values. The index offset is derived from retrieval-before-update ordering.
- An input Module uses brainstate.random.poisson with the dimensionless, unit-derived superposed expectation; it returns JE times integer counts. Global RNG is reseeded before each independent rollout; graph and initial-state RNGs live at host construction boundaries with independent SeedSequence child streams.
- brainstate.transform.for_loop owns every timestep. An outer brainstate.transform.jit owns the complete rollout, with g and eta runtime arguments and graph as stable structure. Packed binary monitoring is a pure observation boundary; no voltage history is needed. Host loops enumerate independent runs, never timesteps.
- No native package orchestrator documented here expresses this precise custom endpoint transition, full binary monitoring and regime assessment. The canonical BrainState loop is the documented runner for native BrainPy-State Dynamics.
- Host NumPy/SciPy handle explicitly stored graph preparation, serialization and statistical analysis. Keep physical quantities in voltage and time dynamics; convert to mV/ms/Hz only at observation and serialization boundaries.

## BrainTools API gap: fixed indegree graph
- Required: uniform sampling without replacement separately from E/I for each target, excluding self for the relevant population, exact CE/CI and inspectable edges.
- Checked: connectivity reference Random/FixedProb, Regular, ExcitatoryInhibitory, ConnectionResult; BrainEvent fixed-degree and CSR contracts.
- Limitation: documented Random/ExcitatoryInhibitory use fixed probability; the routed Regular table does not specify uniform fixed incoming degree with distinct source population exclusions. BrainEvent fixed-degree storage does not define the required uniform graph sampler.
- Smallest boundary: NumPy Generator.choice on each target's allowed integer source set; construct source-row CSR with host SciPy; pass only explicit integer CSR topology to BrainEvent. This is graph preparation, not numerical simulation. Verify every target's exact degree, exclusions and uniqueness; save graph and hashes. Event product parity against explicit edge sums is required.

## BrainTools/BrainPy API gap: exact Poisson counts
- Required: superposition of 1000 independent Poisson sources per neuron with multiplicities (lambda=0.9 to 4 at baseline dt).
- Checked: component-selection PoissonSpike/PoissonEncoder (binary), PoissonInput/poisson_input (no exact count-distribution guarantee in routed contract), BrainState random.poisson public API (exact specified distribution).
- Smallest boundary: a named input Module calls BrainState's documented Poisson sampler, retaining RNG State under the same compiled rollout. This avoids assuming that a binary source or undocumented approximation meets the input law.
- Unit/shape/distribution parity: expectation computed with Hz and dt; test mean, variance, multi-event probability and cross-target correlation.

Host Welch spectra and CV/variance summaries are analysis and serialization boundaries, not replacement simulation infrastructure. No fitting/training applies. Device: CPU in the provided Linux container; no claim of a Windows-native execution.

## Lifecycle refinement during focused checks, before production
Read collective_model_operations.md and transformation-jit-expansion.md after the full-size repeat check failed when init_all_states replaced State objects already captured by a cached runner. Follow the more specific collective-operation contract: initialize once, snapshot every State value by its existing path, and restore with assign_state_values before each independent rollout, requiring both unexpected and missing collections empty. Reseed the global RNG separately. This preserves original State identity, exact empty buffers and initial voltages. Retain the failed pre-production log; require exact full-size spike/count/final-voltage replay before production. No scientific setting or acceptance rule changes.
