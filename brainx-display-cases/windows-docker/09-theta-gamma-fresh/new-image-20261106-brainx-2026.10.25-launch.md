# BrainX 2026.10.25 baseline launch

- Run name is `new-image-20261106-brainx-2026.10.25`. Windows Git Bash started the evaluator on 2026-11-06 at 08:38:04 Asia/Shanghai.
- [PyPI release metadata](https://pypi.org/pypi/BrainX/json) identified `2026.10.25` as the latest release on 2026-11-06. The wheel and source distribution were published on 2026-10-25 and neither was yanked. [Release page](https://pypi.org/project/BrainX/2026.10.25/)
- Reused `brainx-eval:2026.10.25-py312` on Docker Desktop `desktop-linux` 29.9.2. Image ID `sha256:8cc3d09f69ae914034abf22e0bcd10db36f8344588ad0b691062454ebff648cf`. Platform `linux/amd64`.
- The local BuildKit layer history matches the repository Dockerfile's pinned BrainX CPU install, Node and Codex installation steps, and login-shell virtualenv setup. The Dockerfile at checkout `3758d24f10c45fc2e7e9521b68f4b9ef8755376d` has Git blob ID `6def27f4b68eaf98f0490278f65b67736759220f`. Container checks reported BrainX 2026.10.25, Python 3.12.16, Codex CLI 0.166.0 and Node 22.23.4. `pip check` passed.
- The launcher sourced the ignored `brainx-eval.env`, which already selected the versioned tag. The running evaluator's image ID matched the inspected ID. The configured model was `codex/gpt-6.1-sol` through `magpie-local`, with reviewer transport `app-server-stdio` and environment-based authentication. The launcher passed the login-shell import, in-container Magpie/shim catalog and reviewer MCP checks.
- The launcher received the original 634-byte prompt with SHA-256 `c3ad8eb63e3c056e581717baf55f8c35f2f6ba690af75767201a57f934b58246`. It created an empty workspace with no case inputs or seed. The mount set excludes the historical run directory.
- This record captures launch. The harness writes the run directory and `harness-metadata.txt` after the evaluator exits. Scientific acceptance requires the new run's own independent verdict.

## Retry on 2026-11-06

The first evaluator exited with code 1 after repeated upstream EOF/502 errors before any modeling work. The failed archive was deleted on request. At 09:03:32 Asia/Shanghai, Windows Git Bash launched a fresh retry under the same run name, using the same image ID and original prompt. The harness preflight passed, and the evaluator received a model response and completed tool calls. This entry records startup only.
