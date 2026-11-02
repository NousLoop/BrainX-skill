"""Check the real reviewer MCP handshake and tools without calling a model."""
import json
import queue
from pathlib import Path
import subprocess
import sys
import tempfile
import threading


def check_sandbox():
    with tempfile.TemporaryDirectory(prefix=".brainx-reviewer-probe-", dir="/workspace") as temp:
        probe = Path(temp) / "probe.txt"
        probe.write_text("readable")
        code = """import errno, pathlib, sys
p = pathlib.Path(sys.argv[1])
assert p.read_text() == 'readable'
try:
    p.write_text('unexpected write')
except OSError as exc:
    if exc.errno not in (errno.EROFS, errno.EACCES, errno.EPERM): raise
else:
    raise RuntimeError('read-only sandbox permitted a write')
"""
        result = subprocess.run(
            ["codex", "-c", 'sandbox_mode="read-only"', "sandbox", sys.executable,
             "-c", code, str(probe)], capture_output=True, text=True, timeout=20,
        )
        if result.returncode != 0 or probe.read_text() != "readable":
            print("FAIL: reviewer sandbox cannot read evidence or enforce read-only access", file=sys.stderr)
            return False
        print("PASS: reviewer sandbox reads evidence and rejects writes")
        return True


def main():
    if not check_sandbox():
        return 1
    messages = queue.Queue()
    with tempfile.TemporaryFile(mode="w+") as stderr:
        process = subprocess.Popen(
            ["node", "/bundle/mcp-servers/codex/server.mjs"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
            text=True, bufsize=1,
        )

        def read_stdout():
            for line in process.stdout:
                messages.put(line)
            messages.put(None)

        threading.Thread(target=read_stdout, daemon=True).start()

        def send(message):
            process.stdin.write(json.dumps({"jsonrpc": "2.0", **message}) + "\n")
            process.stdin.flush()

        def receive(request_id):
            # Bound the whole wait, including unsolicited notifications.
            import time
            deadline = time.monotonic() + 20
            while True:
                line = messages.get(timeout=max(0, deadline - time.monotonic()))
                if line is None:
                    raise RuntimeError("reviewer exited before responding")
                response = json.loads(line)
                if response.get("id") == request_id:
                    if "error" in response:
                        raise RuntimeError("reviewer returned a protocol error")
                    return response["result"]

        try:
            send({"id": 1, "method": "initialize", "params": {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "brainx-preflight", "version": "1"},
            }})
            receive(1)
            send({"method": "notifications/initialized"})
            send({"id": 2, "method": "tools/list", "params": {}})
            names = {tool["name"] for tool in receive(2)["tools"]}
            if not {"codex", "codex-reply"}.issubset(names):
                raise RuntimeError("required reviewer tools are missing")
            print("PASS: reviewer MCP exposes codex and codex-reply")
            return 0
        except (RuntimeError, queue.Empty, ValueError, BrokenPipeError) as exc:
            # Do not dump child output: the inherited config may contain secrets.
            print(f"FAIL: reviewer MCP preflight ({type(exc).__name__})", file=sys.stderr)
            return 1
        finally:
            process.stdin.close()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            process.stdout.close()


if __name__ == "__main__":
    raise SystemExit(main())
