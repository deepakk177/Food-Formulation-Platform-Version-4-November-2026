"""
Unit Tests for Pipeline V2 HTTP Acquisition Client.

Runs against an isolated local HTTP server fixture.
Zero external network calls.
"""

import http.server
import os
import socket
import tempfile
import threading
import time
from pathlib import Path
import pytest

from pipeline_v2.core.http_client import HttpAcquisitionClient
from pipeline_v2.core.exceptions import (
    HTTPStatusError,
    RateLimitExceededError,
    DownloadTimeoutError,
    ContentTypeError,
    InterruptedDownloadError,
)


class MockServerHandler(http.server.BaseHTTPRequestHandler):
    """Custom HTTP handler to test client download edge cases."""

    rate_limit_hits = 0

    def do_GET(self):
        if self.path == "/valid_file.csv":
            content = b"col_a,col_b\n1,2\n3,4\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        elif self.path == "/html_error_page":
            html_content = b"<html><body>403 Forbidden Access Restricted</body></html>"
            self.send_response(200)  # Cloudflare/gateways sometimes return 200 with HTML portal
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_content)))
            self.end_headers()
            self.wfile.write(html_content)

        elif self.path == "/not_found":
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

        elif self.path == "/rate_limited":
            MockServerHandler.rate_limit_hits += 1
            if MockServerHandler.rate_limit_hits <= 2:
                self.send_response(429)
                self.send_header("Retry-After", "0")
                self.end_headers()
                self.wfile.write(b"Rate limited")
            else:
                content = b"Recovered after 429 retry"
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)

        elif self.path == "/persistent_429":
            self.send_response(429)
            self.send_header("Retry-After", "0")
            self.end_headers()
            self.wfile.write(b"Always rate limited")

        elif self.path == "/truncated_stream":
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", "1000")  # Claim 1000 bytes
            self.end_headers()
            self.wfile.write(b"Short partial bytes only")  # Send only 24 bytes

        elif self.path == "/slow_timeout":
            time.sleep(0.5)
            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Too late")
            except OSError:
                pass

        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        # Silence standard HTTP server console output during tests
        pass


@pytest.fixture(scope="module")
def local_http_server():
    """Starts a local HTTP server on an open ephemeral port in a daemon thread."""
    server_address = ("127.0.0.1", 0)  # Port 0 selects an available port
    httpd = http.server.HTTPServer(server_address, MockServerHandler)
    port = httpd.server_port
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()


def test_successful_streamed_download(local_http_server):
    """Tests normal chunked download with atomic file placement."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dest_path = Path(tmpdir) / "output.csv"
        client = HttpAcquisitionClient(rate_limit_delay_seconds=0.01)

        result = client.download_file(
            url=f"{local_http_server}/valid_file.csv",
            destination_path=dest_path,
            expected_content_types=["text/csv"],
        )

        assert result.exists()
        assert result.read_bytes() == b"col_a,col_b\n1,2\n3,4\n"
        # Verify no .tmp files remain
        tmp_files = list(Path(tmpdir).glob("*.tmp*"))
        assert len(tmp_files) == 0
        client.close()


def test_http_404_not_found(local_http_server):
    """Verifies that HTTP 404 raises HTTPStatusError and creates no file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dest_path = Path(tmpdir) / "missing.csv"
        client = HttpAcquisitionClient(rate_limit_delay_seconds=0.01)

        with pytest.raises(HTTPStatusError) as exc_info:
            client.download_file(
                url=f"{local_http_server}/not_found",
                destination_path=dest_path,
            )

        assert exc_info.value.status_code == 404
        assert not dest_path.exists()
        client.close()


def test_html_error_page_rejection(local_http_server):
    """Verifies rejection of HTML pages when binary/structured data is expected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dest_path = Path(tmpdir) / "download.zip"
        client = HttpAcquisitionClient(rate_limit_delay_seconds=0.01)

        with pytest.raises(ContentTypeError, match="received HTML page"):
            client.download_file(
                url=f"{local_http_server}/html_error_page",
                destination_path=dest_path,
                disallow_html=True,
            )

        assert not dest_path.exists()
        client.close()


def test_rate_limiting_retry_and_recovery(local_http_server):
    """Verifies that client handles HTTP 429 by waiting and retrying."""
    MockServerHandler.rate_limit_hits = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        dest_path = Path(tmpdir) / "rate_limit_ok.bin"
        client = HttpAcquisitionClient(rate_limit_delay_seconds=0.01)

        result = client.download_file(
            url=f"{local_http_server}/rate_limited",
            destination_path=dest_path,
        )

        assert result.exists()
        assert result.read_bytes() == b"Recovered after 429 retry"
        client.close()


def test_persistent_rate_limit_exhaustion(local_http_server):
    """Verifies RateLimitExceededError when 429 retries are exhausted."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dest_path = Path(tmpdir) / "persistent_429.bin"
        client = HttpAcquisitionClient(rate_limit_delay_seconds=0.01)

        with pytest.raises(RateLimitExceededError):
            client.download_file(
                url=f"{local_http_server}/persistent_429",
                destination_path=dest_path,
            )

        assert not dest_path.exists()
        client.close()


def test_interrupted_or_truncated_stream(local_http_server):
    """Verifies that stream byte count mismatch raises InterruptedDownloadError and cleans up temp files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dest_path = Path(tmpdir) / "truncated.bin"
        client = HttpAcquisitionClient(rate_limit_delay_seconds=0.01)

        with pytest.raises(InterruptedDownloadError):
            client.download_file(
                url=f"{local_http_server}/truncated_stream",
                destination_path=dest_path,
            )

        assert not dest_path.exists()
        # Ensure temporary files are cleaned up
        assert len(list(Path(tmpdir).glob("*.tmp*"))) == 0
        client.close()


def test_download_timeout(local_http_server):
    """Verifies that short timeout raises DownloadTimeoutError."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dest_path = Path(tmpdir) / "timed_out.bin"
        # Configure very short read timeout (0.1s) and max_retries=0
        client = HttpAcquisitionClient(connect_timeout=0.2, read_timeout=0.1, max_retries=0, rate_limit_delay_seconds=0.01)

        with pytest.raises(DownloadTimeoutError):
            client.download_file(
                url=f"{local_http_server}/slow_timeout",
                destination_path=dest_path,
            )

        assert not dest_path.exists()
        client.close()
