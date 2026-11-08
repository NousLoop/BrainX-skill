# Brunel-lif-regimes

## Prompt
Simulate a current-based LIF network: NE=10,000, NI=2,500; fixed CE/CI/Cext=1000/250/1000; tau_m=20 ms, t_ref=2 ms,threshold/reset=20/10 m V; delta jumps JE=0.1 mV and JI=-gJE with 1.5 ms delay; independent Poisson drive nu_ext=eta*theta/(JE*CE*tau_m).Run (g,eta)=(3,2),(6,4),(5,2),(4.5,0.9) over a fixed seed set. Render and save a 4-condition figure: for each condition, place instantaneous global rate (0.1 ms bins; mean dashed) above a raster for a fixed random 50-neuron sample. Also save E/I rates, ISI CV and global-rate spectrum; report dominant frequency. Verify the respective regimes: synchronous regular, fast synchronous irregular,asynchronous irregular, and slow synchronous irregular. Do not stop at arrays: write PNG files and list paths. Assume you are the very first explorer of this problem, with no prior papers or open-source code available for reference. Please build the model from first principles, using only the data provided instead of searching any existing paper or code.(this is a new task, don't build the model base on your memory)

## Expected BrainX Packages

- `brainpy-state`: build the LIF populations, delayed synapses, and Poisson input.
- `brainevent`: implement sparse event-driven recurrent communication.
- `brainunit`: enforce consistent voltage and time units.
- `brainstate`: manage and compile the network simulation.
## Researcher authorization for this independent Windows Docker baseline

Preserve every supplied network size, indegree, voltage jump, delay, drive equation, condition and output requirement. This is a first-principles exploration using the supplied data, not a paper reproduction. Do not search for or consult papers, scientific example scripts, existing model implementations or open-source scientific code; do not reconstruct a remembered Brunel protocol. Installed BrainX skill instructions and public API contract documentation may be consulted only for library mechanics, not scientific example solutions. Keep this restriction in the independent reviewer request as well.

I explicitly delegate all unspecified choices needed to execute the supplied experiment, including fixed seed set, duration and burn-in, initial states, graph details not specified, integration/event ordering, numerical checks and quantitative regime decision rules. Derive and justify choices from the supplied equations and first principles, write them into NeuroSpecification.md and lock it before simulation. This authorization covers proceeding without another clarification or approval. Do not change specified data or tune thresholds after seeing results. Report a requested regime as unsupported or inconclusive when the frozen tests do not support it; do not force the four labels. Complete independent Codex review and preserve its verdict, code, raw evidence and PNG outputs.
