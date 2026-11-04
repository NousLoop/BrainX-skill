"""Figure provenance, including preserved unaccepted figures."""
import json
from pathlib import Path
import hashlib


def main():
    run=Path("runs/production-02"); source=json.loads((run/"manifest.json").read_text())
    original=Path("iterations/iteration-1/FIGURE_MANIFEST.md").read_text()
    sections=[original,"\n# Iteration 2 figure evidence\n"]
    for mode in ["diagnostic","final"]:
        out=Path("figures")/(mode+"-iteration-2")
        if not out.is_dir(): continue
        for name,question in [("traces","Compare E/I gamma, proxy and phase-dependent envelope."),
            ("nesting","Compare PSD, known-phase amplitude profile and cycle rotations."),
            ("scan","Retain all discrete depth/gain outcomes and invalid settings.")]:
            path=out/(name+".png")
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            sections.append(f'''## {out}/{name}.png and .pdf
- Work type: create; evidence mode: {mode}; question: {question}
- Acceptance: {'independent review iteration 2 PASS; accepted illustrative scope' if mode=='final' else 'provisional, unaccepted diagnostic at export; preserved'}.
- Source run: production-02; source files runs/production-02/raw/trajectories.npz (SHA256 {source['raw/trajectories.npz']['sha256']}) and raw/derived.npz (SHA256 {source['raw/derived.npz']['sha256']}); config/environment/complete manifest in same run.
- Variables/axes: E/I time × IC × condition, dimensionless activity; time seconds; proxy/envelope a.u.; PSD a.u.²/Hz; known theta phase radians; grid m rows × g columns. View order proxy, no_theta, E, E_minus_I.
- Transformations: 2 s transient discarded, 1 kHz point sampling; order-4 zero-phase Butterworth 25–100 Hz and Hilbert; each edge 0.5 s removed for metrics; native Welch nperseg=2000; 18 mean-amplitude phase bins. No additional curve smoothing. R/ΔR/fraction/peak values come directly from exported metrics.
- Sample unit: deterministic IC sensitivity, n=3; first IC g=1,m=0/0.75 for traces/nesting (3–3.5 s trace); all 3 IC arithmetic mean for 5×5 grid; no CIs/biological inference. 199 per-cycle phase rotations, seed 20261103, complete edge cycles removed.
- Controls: same mean input, initial conditions, solver, phase reference and observation mapping. Same fixed axes across paired panels. Grid uses discrete cells without interpolation; × current band/timing invalid, ○ matched m=0 autonomous gamma invalid. Continuous values of invalid points are preserved.
- Source/output: figures.py; PNG 200 dpi and vector PDF. Traces 12×8 in; nesting 15×4 in; scan 16×4 in. PNG SHA256 {digest}.
- Render/source checks: PNG opened visually; nonblank, legible, no overlap/clipping; paired axes and all 25 coordinates agree with source. R 0.000272/0.501625 and carrier 43.5 Hz independently compared with metrics; null/invalid points visible. Final mode uses same evidence/encodings after PASS.
''')
    Path("FIGURE_MANIFEST.md").write_text("\n".join(sections))


if __name__=="__main__":main()
