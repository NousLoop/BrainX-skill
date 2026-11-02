"""Verify provider auth against a loopback sink using only a dummy credential.

Run with the evaluation image's Python and codex on PATH. No real API call is
made; configuration, endpoint, credentials, and working directory are isolated.
"""
import http.server
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading

DUMMY_KEY = "dummy-key-for-smoke-test"


class Handler(http.server.BaseHTTPRequestHandler):
    received = []

    def do_POST(self):
        self.received.append(self.headers.get("Authorization"))
        body = b'{"error":{"message":"smoke-test-unauthorized"}}'
        self.send_response(401)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def main():
    Handler.received = []
    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        with tempfile.TemporaryDirectory(prefix="brainx-auth-smoke-") as temp:
            root = Path(temp)
            home = root / "codex-home"
            home.mkdir()
            # Preserve the committed provider/auth bytes; omit the unrelated MCP
            # registration and replace only its endpoint for this offline check.
            # The base_url is matched by pattern so the check stays correct no
            # matter which endpoint the template freezes.
            template = Path(__file__).with_name("minimal-eval-config.toml").read_text()
            config = re.sub(
                r'base_url\s*=\s*"[^"]*"',
                f'base_url = "http://127.0.0.1:{server.server_port}/v1"',
                template.split("[mcp_servers.codex]", 1)[0],
            )
            (home / "config.toml").write_text(config)
            env = {k: v for k, v in os.environ.items()
                   if not k.startswith(("OPENAI_", "CODEX_"))}
            env.update(CODEX_HOME=str(home), HOME=str(root),
                       OPENAI_API_KEY=DUMMY_KEY)
            try:
                subprocess.run(
                    [os.environ.get("BRAINX_AUTH_TEST_CODEX", "codex"), "exec", "--ephemeral", "--skip-git-repo-check",
                     "--ignore-rules", "--sandbox", "read-only",
                     "reply with exactly: OK"],
                    cwd=root, env=env, stdin=subprocess.DEVNULL,
                    capture_output=True, text=True, timeout=45,
                )
            except (subprocess.TimeoutExpired, OSError) as exc:
                print(f"FAIL: codex did not complete ({type(exc).__name__})")
                return 1
        if Handler.received and all(
            auth == f"Bearer {DUMMY_KEY}" for auth in Handler.received
        ):
            print("PASS: provider auth delivered the dummy key to the local sink")
            return 0
        print("FAIL: no request arrived or Authorization did not match the dummy key")
        return 1
    finally:
        server.shutdown()
        server.server_close()
        worker.join()


if __name__ == "__main__":
    raise SystemExit(main())
