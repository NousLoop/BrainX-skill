# BrainX mechanics study, iteration 1

Completed before implementation. The user prohibits scientific example solutions: no application scripts, installed library source, papers or scientific repositories were consulted. Scientific design is solely the locked specification and elementary ODE/Poisson derivation. Inline API snippets were considered only for syntax/lifecycle; no scientific example design is adopted.

Studied skill instructions in full: brainx-general-guard, brainx-modeling-loop, brainpy-state, brainevent, brainunit, brainstate, brainx-acceleration and brainx-visualization. Supporting mechanics references: BrainPy component-selection, projection-patterns, brain-dynamics-delay-protocol, braintools/connectivity; BrainEvent sparse-formats; BrainState randomness-and-reproducibility, control-flow-patterns, transformation-jit-expansion; experiment runner/monitor.

Public contract pages only: `api-docs/Dynamics.txt`, `api-docs/poisson.txt`, `api-docs/base.txt`, `api-docs/random.txt`. Initial readthedocs URLs returned HTTP 403; BrainX official documentation supplied the relevant contracts. No package source or introspection was used. The lowercase importability check `brainx` initially returned false; correctly capitalized `BrainX` is importable, as are all requested packages. No installation or environment mutation is needed.

Design: a small custom `brainpy.state.Dynamics` implements the specified endpoint jump and integer refractory semantics with unit-bearing voltage, rather than assuming an undocumented stock LIFRef event order. Native `DeltaProj` deposits recurrent increments through the documented delta-input contract. BrainEvent CSR stores the quenched graph; two scalar-weight event products preserve E/I signs and reduce floating summation sensitivity. BrainState Delay stores binary history; BrainState RandomState owns the independent external Poisson stream; BrainState jit(for_loop) owns the whole rollout. Native LIFRef was checked as the high-level alternative, but its exact refractory endpoint/jump order is not specified by the skill contract, so the short explicit equation is needed for this protocol. No exponential synaptic filter is appropriate for delta jumps.

## BrainTools API gap: exact graph
- Operation: fixed, distinct incoming CE/CI, exclude autapses, uniform without replacement for each target, preserve explicit graph.
- APIs checked: braintools.conn.Random/FixedProb, Regular, ExcitatoryInhibitory, ConnectionResult; BrainEvent FixedNumPerPost and CSR.
- Limitation: the documented Random/EI APIs fix probability, not exact indegree; the routed Regular contract does not specify this directed bipartite without-replacement contract or E/I exclusions.
- Smallest boundary: host NumPy sampling of the explicitly specified topology, then compressed sparse serialization and BrainEvent CSR for every simulation communication. Verify every degree, absence of self edges/duplicates and product parity.

## Exact stochastic drive
BrainPy PoissonSpike is a binary source and PoissonInput's routed contract does not guarantee the exact multi-arrival superposition distribution/refractory order needed here. Use the documented BrainState RandomState.poisson operation with dimensionless mean derived by BrainUnit, inside a BrainPy input Module; retain all count multiplicities. This preserves the Poisson process on the time grid rather than approximating it by Bernoulli source occupancy or Gaussian input.

Host statistics and serialization are legitimate boundaries. Welch PSD, ISI distributions, frozen decision rules and figures operate on saved events/counts and cannot change dynamics. Training/fitting coverage: none.

Acceleration plan: sparse binary event communication, unit-bearing neuron State, a single compiled fixed-length rollout, bit-packed spike recording to avoid a 0.5–1 GB boolean history. Compare compiled and uncompiled small-network state/event results before production. CPU is the available backend; preserve the existing environment. No scientific equations or parameters may change for speed.
