# Archived display cases (macOS era)

All 23 numbered cases produced on macOS (Seatbelt isolation or the earlier
codex 0.147 harness) live here, with their original category structure:

- `creative-experiment-verification/` — 01, 05 (macOS runs), 06, 08
- `paper-reproductions/` — 09, 13, 14, 15
- `speed-and-performance/` — 03, 07, 10, 12
- `use-the-skill-for-training/` — 02, 11
- `16`–`23` — uncategorized top-level cases

## Comparability

None of these runs are comparable with anything under `../windows-docker/`.
Environment, codex CLI version, and reviewer transport all differ. Treat this
directory as frozen evidence: refinement loops that closed here stay closed,
and reopened cases must start a new baseline under `../windows-docker/`.

Case 15 is retained only at `paper-reproductions/15-grid-cell-theta-sweep/`,
including its run2 diagnosis. The identical top-level subset was removed on
2026-11-03.

`refinement-eval.sb.in` is the archived macOS-era Seatbelt sandbox profile the
old harness filled and passed to `sandbox-exec`. No current script reads it;
Docker mount-set isolation replaced it on every platform.
