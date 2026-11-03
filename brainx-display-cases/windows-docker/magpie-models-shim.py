#!/usr/bin/env python3
"""Magpie /v1/models shim for codex CLI compatibility.

magpie (127.0.0.1:3425) serves an OpenAI-style /v1/models listing. codex-cli's
models manager does NOT consume that shape: its refresh link expects its own
private catalog schema (top-level {"models": [...]} with ~50 required fields
per entry — slug, context_window, supported_reasoning_levels,
truncation_policy, shell_type, visibility, ...). Any OpenAI-style payload,
fat or slim, fails to decode ("failed to decode models response: Data at
line 1 column N") and retries every ~4.5 minutes.

This shim listens on SHIM_PORT (default 3426) and transparently proxies every
request to UPSTREAM_HOST:UPSTREAM_PORT (default 127.0.0.1:3425) with headers,
body, and status preserved. Two rewrites exist:

  1. GET /v1/models: the response is translated into codex's own catalog
     format using codex-model-catalog-0.166.json (downloaded from the official
     rust-v0.166.0 tag of openai/codex; the schema is version-locked, do not
     substitute another tag) as the entry template:

  for each model id magpie lists (e.g. "codex/gpt-6.1-sol"), the official
  catalog entry with the matching slug (after stripping the "codex/" prefix)
  is copied verbatim and its slug is replaced by magpie's full id, so codex's
  --model "codex/gpt-6.1-sol" matches the entry while requests still carry
  magpie's routed id.

  2. Response framing reconstruction (every other endpoint). resp.read*()
  returns decoded bytes: upstream Transfer-Encoding chunking is already
  stripped by http.client. The proxy therefore re-adds a correct message
  boundary downstream: Content-Length is forwarded verbatim when upstream
  sent one; chunked framing is re-encoded when upstream was chunked; and a
  response with neither (close-delimited) is terminated by closing the
  connection. Without one of the three the HTTP/1.1 client cannot detect the
  end of the message and hangs until its read timeout.

No model entry is invented, added, or removed: only ids magpie actually
serves appear. Every other endpoint — including the official-source
/v1/responses passthrough — passes through untouched.

Bodies are streamed with resp.read1() (a single underlying socket read) so
small SSE events are forwarded as they arrive instead of being buffered
until 8192 bytes accumulate.

Point codex at the shim by setting the provider base_url to
http://host.docker.internal:3426/v1 (inside a container) or
http://127.0.0.1:3426/v1 (on the host). magpie itself keeps serving port
3425 for every other consumer unchanged.

If the catalog template file is missing or a magpie id has no official
counterpart, the original magpie response is passed through unchanged (the
refresh link keeps failing, but nothing else breaks).
"""

import http.client
import http.server
import json
import os
import sys
import threading

UPSTREAM_HOST = os.environ.get("MAGPIE_UPSTREAM_HOST", "127.0.0.1")
UPSTREAM_PORT = int(os.environ.get("MAGPIE_UPSTREAM_PORT", "3425"))
SHIM_HOST = os.environ.get("MAGPIE_SHIM_HOST", "0.0.0.0")
SHIM_PORT = int(os.environ.get("MAGPIE_SHIM_PORT", "3426"))

CATALOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "codex-model-catalog-0.166.json")

HOP_HEADERS = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade", "host", "content-length",
}

_catalog_cache = {"mtime": None, "doc": None}
_catalog_lock = threading.Lock()


def load_catalog():
    """Load and cache the official codex 0.166 catalog template."""
    try:
        st = os.stat(CATALOG_FILE)
    except OSError:
        return None
    with _catalog_lock:
        if _catalog_cache["doc"] is not None and _catalog_cache["mtime"] == st.st_mtime:
            return _catalog_cache["doc"]
        try:
            with open(CATALOG_FILE, "rb") as f:
                doc = json.load(f)
        except (ValueError, OSError):
            return None
        if not isinstance(doc.get("models"), list):
            return None
        _catalog_cache["mtime"] = st.st_mtime
        _catalog_cache["doc"] = doc
        return doc


def translate_models_payload(raw: bytes) -> bytes:
    """Translate magpie's OpenAI-style listing into codex's catalog format."""
    magpie_doc = json.loads(raw.decode("utf-8"))
    catalog = load_catalog()
    if catalog is None:
        return raw  # no template: pass through unchanged

    by_slug = {}
    for entry in catalog["models"]:
        slug = entry.get("slug")
        if isinstance(slug, str):
            by_slug[slug] = entry

    out = []
    for m in magpie_doc.get("data", []):
        if not isinstance(m, dict):
            continue
        mid = m.get("id")
        if not isinstance(mid, str):
            continue
        base = by_slug.get(mid[len("codex/"):] if mid.startswith("codex/") else mid)
        if base is None:
            sys.stderr.write("magpie-models-shim: no catalog entry for %r, "
                             "passing response through\n" % mid)
            return raw
        entry = dict(base)
        entry["slug"] = mid  # codex matches --model against this slug
        out.append(entry)

    return json.dumps({"models": out}, separators=(",", ":")).encode("utf-8")


class ShimHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "magpie-models-shim/2.1"

    def log_message(self, fmt, *args):  # keep console quiet-ish
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _proxy(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None

        fwd = {k: v for k, v in self.headers.items()
               if k.lower() not in HOP_HEADERS}
        conn = http.client.HTTPConnection(UPSTREAM_HOST, UPSTREAM_PORT,
                                          timeout=600)
        try:
            conn.request(self.command, self.path, body=body, headers=fwd)
            resp = conn.getresponse()
            is_models = (self.command == "GET"
                         and self.path.split("?", 1)[0].rstrip("/") == "/v1/models")
            if is_models:
                raw = resp.read()
                try:
                    out = translate_models_payload(raw)
                except (ValueError, UnicodeDecodeError):
                    out = raw  # not JSON: pass the original bytes through
                self.send_response(resp.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)
            else:
                self.send_response(resp.status)
                upstream_cl = None
                for k, v in resp.getheaders():
                    lk = k.lower()
                    if lk in HOP_HEADERS:
                        # Capture the upstream framing before dropping it:
                        # resp.read*() returns decoded bytes, so the boundary
                        # must be reconstructed below, not forwarded as-is.
                        if lk == "content-length":
                            upstream_cl = v
                        continue
                    self.send_header(k, v)
                body_expected = (self.command != "HEAD"
                                 and not 100 <= resp.status < 200
                                 and resp.status not in (204, 304))
                if resp.chunked and body_expected:
                    # Re-encode the chunk framing http.client already decoded.
                    self.send_header("Transfer-Encoding", "chunked")
                elif upstream_cl is not None and not resp.chunked:
                    self.send_header("Content-Length", upstream_cl)
                elif body_expected:
                    # No length and no chunking: connection close is the only
                    # valid HTTP/1.1 message boundary left.
                    self.close_connection = True
                    self.send_header("Connection", "close")
                self.end_headers()
                if not body_expected:
                    return
                # read1 = at most one blocking socket read: small SSE events
                # pass through immediately instead of accumulating 8192 bytes.
                body_read = resp.read1
                if resp.chunked:
                    while True:
                        chunk = body_read(8192)
                        if not chunk:
                            break
                        self.wfile.write(b"%x\r\n%s\r\n" % (len(chunk), chunk))
                        self.wfile.flush()
                    self.wfile.write(b"0\r\n\r\n")
                    self.wfile.flush()
                else:
                    while True:
                        chunk = body_read(8192)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        self.wfile.flush()
        except BrokenPipeError:
            pass
        finally:
            conn.close()

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = do_OPTIONS = _proxy


def main():
    if load_catalog() is None:
        sys.stderr.write("magpie-models-shim: WARNING: %s missing or invalid; "
                         "/v1/models will pass through untranslated\n"
                         % CATALOG_FILE)
    server = http.server.ThreadingHTTPServer((SHIM_HOST, SHIM_PORT), ShimHandler)
    server.daemon_threads = True
    sys.stderr.write(
        "magpie-models-shim/2.1: %s:%d -> %s:%d "
        "(GET /v1/models translated to codex catalog format; "
        "response framing reconstructed on every other endpoint)\n"
        % (SHIM_HOST, SHIM_PORT, UPSTREAM_HOST, UPSTREAM_PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
