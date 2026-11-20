"""
Pipeline V2 HTTP Acquisition Client.

Provides streaming, atomic downloads with exponential backoff, rate-limiting,
HTTP status validation, content-length verification, and MIME content-type validation.

Guarantees:
- Zero fake fallback file creation on failure.
- HTML error pages are rejected when expecting ZIP, CSV, JSON, or XML.
- Downloads write to a temporary file (.part/.tmp) and atomically replace target
  only after full integrity and size checks pass.
"""

import os
import shutil
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Set, Union
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pipeline_v2.core.exceptions import (
    NetworkAcquisitionError,
    HTTPStatusError,
    RateLimitExceededError,
    DownloadTimeoutError,
    ContentTypeError,
    InterruptedDownloadError,
)
from pipeline_v2.core.logging_config import setup_logger


class HttpAcquisitionClient:
    """Production-grade HTTP client for dataset acquisition."""

    DEFAULT_TIMEOUT = (10.0, 60.0)  # (connect_timeout, read_timeout) in seconds
    DEFAULT_CHUNK_SIZE = 65536  # 64 KB chunks
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 1.5

    # Content-types that indicate HTML error/landing pages
    HTML_MIME_TYPES: Set[str] = {
        "text/html",
        "application/xhtml+xml",
    }

    def __init__(
        self,
        connect_timeout: float = 10.0,
        read_timeout: float = 60.0,
        max_retries: int = MAX_RETRIES,
        backoff_factor: float = BACKOFF_FACTOR,
        rate_limit_delay_seconds: float = 0.5,
        execution_id: Optional[str] = None,
    ):
        self.timeout = (connect_timeout, read_timeout)
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.rate_limit_delay = rate_limit_delay_seconds
        self.last_request_time_by_host: Dict[str, float] = {}
        self.logger = setup_logger("http_client", execution_id=execution_id)

        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[500, 502, 503, 504],
            raise_on_status=False,
            respect_retry_after_header=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _enforce_rate_limit(self, url: str) -> None:
        """Ensures respectful request pacing per host."""
        host = urlparse(url).netloc
        if not host:
            return

        now = time.time()
        last_time = self.last_request_time_by_host.get(host, 0.0)
        elapsed = now - last_time
        if elapsed < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - elapsed
            time.sleep(sleep_time)
        self.last_request_time_by_host[host] = time.time()

    def download_file(
        self,
        url: str,
        destination_path: Union[str, Path],
        expected_content_types: Optional[List[str]] = None,
        disallow_html: bool = True,
        headers: Optional[Dict[str, str]] = None,
        source_id: Optional[str] = None,
    ) -> Path:
        """
        Streams a remote URL to destination_path atomically.

        Args:
            url: The HTTP/HTTPS URL to download.
            destination_path: Target path where the file will be saved.
            expected_content_types: Optional list of acceptable Content-Type substrings.
            disallow_html: If True, reject downloads whose Content-Type is HTML.
            headers: Custom HTTP headers (e.g. User-Agent).
            source_id: Optional source tracking identifier for logging.

        Returns:
            Path object pointing to the successfully downloaded file.

        Raises:
            HTTPStatusError: On 4xx/5xx HTTP errors.
            RateLimitExceededError: On HTTP 429 after retries.
            DownloadTimeoutError: On connection/read timeouts.
            ContentTypeError: When Content-Type fails validation or returns HTML unexpectedly.
            InterruptedDownloadError: If download terminates prematurely.
        """
        dest = Path(destination_path).resolve()
        dest.parent.mkdir(parents=True, exist_ok=True)
        temp_dest = dest.with_suffix(dest.suffix + f".tmp_{os.getpid()}")

        req_headers = {
            "User-Agent": "FoodFormulationKGPrep/2.0 (Scientific Food Science ETL)",
        }
        if headers:
            req_headers.update(headers)

        self.logger.info(
            f"Initiating streaming download for {source_id or 'unknown'} from {url} to {dest}"
        )

        # Retry loop for rate-limiting (429) and standard acquisition
        retries_429 = 0
        max_429_retries = 3

        while True:
            self._enforce_rate_limit(url)
            try:
                response = self.session.get(
                    url,
                    headers=req_headers,
                    stream=True,
                    timeout=self.timeout,
                )
            except requests.exceptions.Timeout as te:
                self._cleanup_temp(temp_dest)
                raise DownloadTimeoutError(
                    f"Connection or read timed out downloading {url}: {te}"
                )
            except requests.exceptions.RequestException as re:
                self._cleanup_temp(temp_dest)
                re_str = str(re).lower()
                if "timed out" in re_str or "timeout" in re_str:
                    raise DownloadTimeoutError(
                        f"Connection or read timed out downloading {url}: {re}"
                    )
                raise NetworkAcquisitionError(
                    f"Network request failed for {url}: {re}"
                )

            # Handle 429 Too Many Requests with exponential wait
            if response.status_code == 429:
                retries_429 += 1
                if retries_429 > max_429_retries:
                    self._cleanup_temp(temp_dest)
                    raise RateLimitExceededError(
                        f"HTTP 429 Too Many Requests from {url}. Retries exhausted.",
                        status_code=429,
                        url=url,
                    )
                # Parse Retry-After header or use exponential backoff
                retry_after = response.headers.get("Retry-After")
                wait_seconds = (
                    float(retry_after)
                    if retry_after and retry_after.isdigit()
                    else (self.backoff_factor**retries_429) * 2.0
                )
                self.logger.warning(
                    f"HTTP 429 received from {url}. Waiting {wait_seconds:.1f}s before retry ({retries_429}/{max_429_retries})."
                )
                time.sleep(wait_seconds)
                continue

            # Check HTTP Status
            if not response.ok:
                self._cleanup_temp(temp_dest)
                raise HTTPStatusError(
                    f"HTTP download failed with status {response.status_code} for {url}",
                    status_code=response.status_code,
                    url=url,
                )

            # Success status received: break retry loop
            break

        # Validate Content-Type
        raw_content_type = response.headers.get("Content-Type", "").lower()
        content_type_clean = raw_content_type.split(";")[0].strip()

        if disallow_html and content_type_clean in self.HTML_MIME_TYPES:
            self._cleanup_temp(temp_dest)
            raise ContentTypeError(
                f"Download rejected: Expected binary/structured data but received HTML page "
                f"(Content-Type: '{raw_content_type}') from {url}. Likely an error or login portal."
            )

        if expected_content_types:
            matches_expected = any(
                exp.lower() in content_type_clean for exp in expected_content_types
            )
            if not matches_expected:
                self._cleanup_temp(temp_dest)
                raise ContentTypeError(
                    f"Content-Type mismatch for {url}: received '{raw_content_type}', "
                    f"expected one of {expected_content_types}."
                )

        # Content-Length check setup
        header_length = response.headers.get("Content-Length")
        expected_bytes = int(header_length) if header_length and header_length.isdigit() else None

        # Stream chunks to temporary file
        bytes_written = 0
        try:
            with open(temp_dest, "wb") as f:
                for chunk in response.iter_content(chunk_size=self.DEFAULT_CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        bytes_written += len(chunk)
        except Exception as e:
            self._cleanup_temp(temp_dest)
            raise InterruptedDownloadError(
                f"Download stream interrupted for {url} after {bytes_written} bytes: {e}"
            )

        # Validate total bytes received against Content-Length if specified
        if expected_bytes is not None and bytes_written != expected_bytes:
            self._cleanup_temp(temp_dest)
            raise InterruptedDownloadError(
                f"Incomplete download for {url}: expected {expected_bytes} bytes, "
                f"received {bytes_written} bytes."
            )

        # Atomic replacement: move temporary file to final target
        try:
            # os.replace handles atomic overwrite on POSIX and Windows (Python 3.3+)
            os.replace(temp_dest, dest)
        except OSError as e:
            self._cleanup_temp(temp_dest)
            raise NetworkAcquisitionError(
                f"Failed to atomically place downloaded file at {dest}: {e}"
            )

        self.logger.info(
            f"Successfully downloaded {bytes_written} bytes from {url} to {dest}"
        )
        return dest

    @staticmethod
    def _cleanup_temp(temp_path: Path) -> None:
        """Safely removes temporary partial download file."""
        try:
            if temp_path.exists():
                temp_path.unlink()
        except OSError:
            pass

    def close(self) -> None:
        """Closes the underlying requests session."""
        self.session.close()

    def __enter__(self) -> "HttpAcquisitionClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
