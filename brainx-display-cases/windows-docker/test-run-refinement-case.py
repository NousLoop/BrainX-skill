"""Exercise launcher preflight failures with a fake Docker; no model calls."""
import hashlib
import http.server
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest


HERE = Path(__file__).resolve().parent
if os.name == 'nt':
    BASH = str(Path(shutil.which('git')).parent / 'bash.exe')
else:
    BASH = shutil.which('bash')


def shell_path(path):
    if os.name != 'nt':
        return str(path)
    return subprocess.check_output(
        [BASH, '-c', 'cygpath -u "$1"', 'sh', str(path)], text=True).strip()


FAKE_DOCKER = '''#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$FAKE_LOG"
case "$1" in
  info)
    test "${DAEMON_DOWN:-0}" != 1 || exit 1
    if test "$#" -gt 1; then printf '%s\\n' "${FAKE_MEMORY:-33526239232}"; fi ;;
  image)
    test "${IMAGE_MISSING:-0}" != 1 || exit 1
    if [[ "$*" == *Architecture* ]]; then echo linux/amd64; else echo sha256:test; fi ;;
  ps) test "${FAKE_BUSY:-0}" != 1 || echo another-container ;;
  run)
    # Match the container command, not filenames present in every mount list.
    while test "$#" -gt 0 && test "$1" != sha256:test; do shift; done
    shift
    case "$*" in
      *urlopen*) echo catalog-probe >> "$FAKE_MARKERS"; exit "${CATALOG_EXIT:-0}" ;;
      *smoke-test-reviewer.py*) echo reviewer-probe >> "$FAKE_MARKERS"; exit 1 ;;
      *tomllib*) echo magpie-local ;;
      *'codex --version'*) echo 'codex-cli 0.166.0' ;;
      *'codex exec'*) echo forbidden-model-call >> "$FAKE_MARKERS"; exit 99 ;;
    esac ;;
esac
'''


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runner = self.root / 'run-refinement-case.sh'
        shutil.copy2(HERE / self.runner.name, self.runner)
        (self.root/'smoke-test-reviewer.py').write_text('')
        (self.root/'seccomp-reviewer.json').write_text('{}')
        self.repo = self.root/'repo'
        self.case = self.repo/'brainx-display-cases/windows-docker/05-alpha-rhythm'
        self.case.mkdir(parents=True)
        (self.repo/'brainx-display-cases/legacy-macos').mkdir()
        (self.repo/'skills/example').mkdir(parents=True)
        (self.repo/'skills/example/SKILL.md').write_text('example')
        (self.repo/'mcp-servers').mkdir()
        self.prompt = self.case/'prompt.md'
        shutil.copy2(HERE.parent/'legacy-macos/creative-experiment-verification/05-alpha-rhythm/prompt.md', self.prompt)
        self.config = self.root/'config.toml'
        self.config.write_text('model = "test-model"\n')
        self.bin = self.root/'bin'
        self.bin.mkdir()
        docker = self.bin/'docker'
        docker.write_text(FAKE_DOCKER, newline='\n')
        docker.chmod(0o755)
        self.log = self.root/'docker.log'
        self.markers = self.root/'markers'
        self.env = {k:v for k,v in os.environ.items() if not k.startswith('BRAINX_')}
        # Prefix inside Bash; Git Bash consumes the Windows PATH on startup.
        self.env.update(BRAINX_REPO=shell_path(self.repo),
                        BRAINX_EVAL_CONFIG=shell_path(self.config),
                        BRAINX_EVAL_MODEL='test-model', BRAINX_FROZEN_HARNESS='1',
                        OPENAI_API_KEY='dummy-test-key', TMPDIR=shell_path(self.root),
                        FAKE_LOG=shell_path(self.log), FAKE_MARKERS=shell_path(self.markers),
                        TEST_BIN=shell_path(self.bin))

    def run_launcher(self, run='control', **overrides):
        result = subprocess.run(
            [BASH, '-c', 'export PATH="$TEST_BIN:$PATH"; exec bash "$1" 05-alpha-rhythm "$2"',
             'sh', shell_path(self.runner), run],
            env=dict(self.env, **overrides), capture_output=True, text=True, timeout=20)
        self.assertNotEqual(result.returncode, 0)
        markers = self.markers.read_text() if self.markers.exists() else ''
        self.assertNotIn('forbidden-model-call', markers)
        return result.stdout + result.stderr, markers

    def variant(self):
        raw = self.prompt.read_bytes()
        return dict(BRAINX_EVAL_PROMPT=shell_path(self.prompt),
                    BRAINX_EXPECTED_PROMPT_BYTES=str(len(raw)),
                    BRAINX_EXPECTED_PROMPT_SHA256=hashlib.sha256(raw).hexdigest())

    def test_relative_prompt_rejected(self):
        output,_ = self.run_launcher(**dict(self.variant(), BRAINX_EVAL_PROMPT='relative.md'))
        self.assertIn('absolute POSIX path', output)
        self.assertFalse(self.log.exists())

    def test_variant_checkpoint_rejected(self):
        output,_ = self.run_launcher('run1', **self.variant())
        self.assertIn('descriptive name', output)

    def test_fingerprint_rejected_before_docker(self):
        self.prompt.write_text('changed')
        output,_ = self.run_launcher()
        self.assertIn('Prompt byte count changed', output)
        self.assertFalse(self.log.exists())

    def test_existing_run_rejected(self):
        (self.case/'control').mkdir()
        output,_ = self.run_launcher()
        self.assertIn('Refusing to overwrite', output)

    def test_relative_seed_rejected(self):
        output,_ = self.run_launcher(**dict(self.variant(), BRAINX_EVAL_WORKSPACE_SEED='relative'))
        self.assertIn('SEED must be an absolute', output)

    def test_daemon_and_image_errors(self):
        output,_ = self.run_launcher(DAEMON_DOWN='1')
        self.assertIn('Docker daemon unreachable', output)
        output,_ = self.run_launcher(IMAGE_MISSING='1')
        self.assertIn('Evaluation image missing', output)

    def test_catalog_failure_prevents_reviewer_and_model(self):
        output,markers = self.run_launcher(CATALOG_EXIT='1', FAKE_MEMORY='1073741824', FAKE_BUSY='1')
        self.assertIn('less than 8 GiB', output)
        self.assertIn('Other containers', output)
        self.assertIn('Start Magpie', output)
        self.assertEqual(markers.splitlines(), ['catalog-probe'])

    def test_reviewer_failure_prevents_model(self):
        output,markers = self.run_launcher()
        self.assertIn('Reviewer unavailable', output)
        self.assertEqual(markers.splitlines(), ['catalog-probe', 'reviewer-probe'])


class CatalogTests(unittest.TestCase):
    def check_catalog(self, status, catalog):
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                body = json.dumps(catalog).encode()
                self.send_response(status)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                config = Path(directory)/'config.toml'
                config.write_text('model_provider = "magpie-local"\n'
                                  '[model_providers.magpie-local]\n'
                                  f'base_url = "http://127.0.0.1:{server.server_port}/v1"\n')
                launcher = (HERE/'run-refinement-case.sh').read_text()
                probe = launcher.split("  docker_run_isolated python -c '\n", 1)[1]
                probe = probe.split("\n' \"$eval_model\"", 1)[0]
                probe = probe.replace('/codex-home/config.toml', config.as_posix())
                return subprocess.run([sys.executable, '-c', probe, 'test-model'],
                                      capture_output=True, text=True,
                                      env=dict(os.environ, NO_PROXY='*'), timeout=10)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_catalog_accepts_selected_model(self):
        result = self.check_catalog(200, {'models': [{'slug': 'test-model'}]})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_openai_listing_is_rejected(self):
        result = self.check_catalog(200, {'data': [{'id': 'test-model'}]})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('selected model absent', result.stderr)

    def test_http_error_is_rejected(self):
        result = self.check_catalog(503, {})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Magpie/shim preflight failed', result.stderr)


if __name__ == '__main__':
    unittest.main()
