import asyncio
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
import aiohttp
import requests
from tqdm.asyncio import tqdm

logger = logging.getLogger("HTTPClient")

class HTTPClient:
    """
    Robust HTTP client for both asynchronous parallel downloads and 
    synchronous API queries. Supports rate limiting, retries with 
    exponential backoff, range-based download resuming, and progress tracking.
    """
    def __init__(
        self,
        user_agent: str = "FoodKG-Acquisition/1.0",
        rate_limit_delay: float = 0.2,
        max_retries: int = 2,
        backoff_factor: float = 1.5,
        timeout: int = 15
    ):
        self.user_agent = user_agent
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout
        self.last_request_time = 0.0
        self.lock = asyncio.Lock()

    def _sync_rate_limit(self) -> None:
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    async def _async_rate_limit(self) -> None:
        async with self.lock:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.rate_limit_delay:
                await asyncio.sleep(self.rate_limit_delay - elapsed)
            self.last_request_time = time.time()

    def get_sync(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> bytes:
        """
        Synchronous GET request with retry logic and rate limiting.
        Fast-fails on 403 / 404 client errors.
        """
        self._sync_rate_limit()
        
        req_headers = {"User-Agent": self.user_agent}
        if headers:
            req_headers.update(headers)
            
        req_timeout = timeout or self.timeout
        
        retries = 0
        backoff = 0.5
        while True:
            try:
                response = requests.get(url, params=params, headers=req_headers, timeout=req_timeout)
                response.raise_for_status()
                return response.content
            except Exception as e:
                # Fast fail on 403 Forbidden or 404 Not Found
                if hasattr(e, 'response') and e.response is not None and e.response.status_code in (403, 404):
                    logger.warning(f"Sync GET {url} returned HTTP {e.response.status_code}. Fast-failing attempt.")
                    raise e

                retries += 1
                if retries > self.max_retries:
                    logger.error(f"Failed sync GET to {url} after {self.max_retries} attempts: {e}")
                    raise e
                
                wait_time = backoff
                if hasattr(e, 'response') and e.response is not None and e.response.status_code == 429:
                    wait_time = max(wait_time, 5.0)
                    logger.warning(f"Rate limited (429) on sync GET {url}. Retrying in {wait_time}s...")
                else:
                    logger.warning(f"Sync GET {url} failed: {e}. Retrying in {wait_time}s (Attempt {retries}/{self.max_retries})...")
                
                time.sleep(wait_time)
                backoff *= self.backoff_factor

    async def download_file_async(
        self,
        url: str,
        dest_path: Path,
        session: aiohttp.ClientSession,
        headers: Optional[Dict[str, str]] = None
    ) -> Path:
        await self._async_rate_limit()

        dest_path = Path(dest_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        req_headers = {"User-Agent": self.user_agent}
        if headers:
            req_headers.update(headers)

        file_mode = "wb"
        existing_size = 0
        if dest_path.exists():
            existing_size = dest_path.stat().st_size
            if existing_size > 0:
                req_headers["Range"] = f"bytes={existing_size}-"
                file_mode = "ab"

        retries = 0
        backoff = 0.5
        
        while True:
            try:
                async with session.get(url, headers=req_headers, timeout=self.timeout) as response:
                    if response.status in (403, 404):
                        response.raise_for_status()

                    if response.status == 206:
                        total_size = int(response.headers.get("Content-Length", 0)) + existing_size
                    elif response.status == 200:
                        file_mode = "wb"
                        existing_size = 0
                        total_size = int(response.headers.get("Content-Length", 0))
                    elif response.status == 416:
                        return dest_path
                    else:
                        response.raise_for_status()
                        total_size = int(response.headers.get("Content-Length", 0))

                    chunk_size = 8192
                    with open(dest_path, file_mode) as f:
                        with tqdm(
                            total=total_size,
                            initial=existing_size,
                            unit="B",
                            unit_scale=True,
                            desc=dest_path.name,
                            leave=False
                        ) as pbar:
                            async for chunk in response.content.iter_chunked(chunk_size):
                                f.write(chunk)
                                pbar.update(len(chunk))
                    
                    return dest_path

            except Exception as e:
                if isinstance(e, aiohttp.ClientResponseError) and e.status in (403, 404):
                    logger.warning(f"Download {url} returned HTTP {e.status}. Fast-failing.")
                    raise e

                retries += 1
                if retries > self.max_retries:
                    logger.error(f"Failed downloading {url} after {self.max_retries} retries: {e}")
                    raise e
                
                wait_time = backoff
                await asyncio.sleep(wait_time)
                backoff *= self.backoff_factor

    async def download_parallel(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Optional[Path]]:
        connector = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=connector, raise_for_status=True) as session:
            async_tasks = []
            for t in tasks:
                async_tasks.append(
                    self.download_file_async(
                        url=t['url'],
                        dest_path=t['dest_path'],
                        session=session,
                        headers=t.get('headers')
                    )
                )
            
            results = await asyncio.gather(*async_tasks, return_exceptions=True)
            
            paths = []
            for r, task in zip(results, tasks):
                if isinstance(r, Exception):
                    logger.error(f"Parallel download failed for {task['url']}: {r}")
                    paths.append(None)
                else:
                    paths.append(r)
            return paths
