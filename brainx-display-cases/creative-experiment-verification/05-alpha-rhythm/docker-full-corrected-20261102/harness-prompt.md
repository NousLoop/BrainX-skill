# Generating an Alpha Rhythm

## Prompt

Create a resting cortical circuit that produces an alpha-like brain rhythm, then weaken inhibition and show how the simulated EEG changes.

## Expected BrainX Packages

- `brainmass`: model interacting cortical populations and derive an interpretable population signal for the simulated EEG.
- `brainstate`: evolve population dynamics with `for_loop` and use `vmap` to compare inhibition strengths and initial conditions.
- `brainunit`: enforce consistent units for time constants, coupling strengths, firing rates, and external drive.

## Researcher approval (2026-11-02)

Use the recommended sweep retaining 100%, 75%, 50%, and 25% of baseline inhibitory coupling. I delegate all remaining unspecified model and simulation settings to you, approve locking the resulting specification, and authorize continuing through the complete simulation, independent Codex review, and visualization.

Original researcher reply: 采用推荐扫描，其余设置由你决定并继续。
