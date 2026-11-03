"""Local HTTP regression tests; no credentials or model calls required."""

import http.client
import http.server
import importlib.util
import json
from pathlib import Path
import threading
import unittest


spec = importlib.util.spec_from_file_location(
    "shim", Path(__file__).with_name("magpie-models-shim.py"))
shim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shim)

EVENT = b"data: first\n\n"


class Upstream(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == "/v1/models":
            body = json.dumps({"data": [{"id": "codex/" +
                shim.load_catalog()["models"][0]["slug"]}]}).encode()
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/empty":
            self.send_response(204)
            self.end_headers()
            return
        self.send_response(200)
        if self.path == "/chunked":
            self.send_header("Transfer-Encoding", "chunked")
        elif self.path != "/close":
            self.send_header("Content-Length", str(len(EVENT) + 4))
        else:
            self.send_header("Connection", "close")
            self.close_connection = True
        self.end_headers()
        if self.path == "/chunked":
            self.wfile.write(b"%x\r\n%s\r\n" % (len(EVENT), EVENT))
        else:
            self.wfile.write(EVENT)
        self.wfile.flush()
        # Hold the rest until the client receives the first event. This
        # deterministically catches buffering until 8192 bytes or EOF.
        self.server.release.wait(3)
        if self.path == "/chunked":
            self.wfile.write(b"4\r\ndone\r\n0\r\n\r\n")
        else:
            self.wfile.write(b"done")
        self.wfile.flush()


class ProxyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.upstream = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Upstream)
        cls.upstream.release = threading.Event()
        shim.UPSTREAM_HOST = "127.0.0.1"
        shim.UPSTREAM_PORT = cls.upstream.server_port
        cls.proxy = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), shim.ShimHandler)
        for server in (cls.upstream, cls.proxy):
            threading.Thread(target=server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        for server in (cls.proxy, cls.upstream):
            server.shutdown()
            server.server_close()

    def test_streaming_and_message_completion(self):
        for path in ("/length", "/chunked", "/close"):
            with self.subTest(path=path):
                self.upstream.release.clear()
                conn = http.client.HTTPConnection(
                    "127.0.0.1", self.proxy.server_port, timeout=1)
                try:
                    conn.request("GET", path)
                    response = conn.getresponse()
                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.read(len(EVENT)), EVENT)
                    self.upstream.release.set()
                    self.assertEqual(response.read(), b"done")
                    if path != "/close":
                        # The same downstream connection remains usable.
                        conn.request("GET", "/empty")
                        empty = conn.getresponse()
                        self.assertEqual(empty.status, 204)
                        self.assertEqual(empty.read(), b"")
                finally:
                    self.upstream.release.set()
                    conn.close()

    def test_models_translation_has_length(self):
        conn = http.client.HTTPConnection(
            "127.0.0.1", self.proxy.server_port, timeout=1)
        try:
            conn.request("GET", "/v1/models")
            response = conn.getresponse()
            body = response.read()
            self.assertEqual(int(response.getheader("Content-Length")), len(body))
            self.assertTrue(json.loads(body)["models"][0]["slug"].startswith("codex/"))
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
