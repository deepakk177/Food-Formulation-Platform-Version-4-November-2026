import aiohttp
from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

class GSFAXMLCollector(BaseCollector):
    """
    GSFA XML Collector: Downloads GSFA XML if a custom URL is configured.
    Defaults to Manual Mode since Codex GSFA does not offer a public bulk XML.
    """
    async def collect(self) -> List[Path]:
        url = self.config.get("download_url")
        
        if not url:
            remarks = (
                "Manual Download Required: Codex Alimentarius GSFA Online does not offer "
                "a public bulk XML export link. Standard data is accessible via search "
                "on https://www.fao.org/gsfaonline/ or by downloading Codex standard CXS 192-1995 PDF. "
                "If you have a custom XML feed, configure 'download_url' in config/config.yaml."
            )
            return self.mark_manual(remarks=remarks)
            
        dest_path = self.dest_dir / "gsfa_standards.xml"
        self.logger.info(f"Attempting custom GSFA XML download from {url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                await self.http_client.download_file_async(url, dest_path, session)
            self.register_file(dest_path, "Downloaded", remarks="Downloaded from custom GSFA XML URL.")
            return [dest_path]
        except Exception as e:
            self.logger.warning(f"Failed to download custom GSFA XML: {e}. Reverting to Manual tracking.")
            remarks = f"Failed to download custom XML from {url}: {e}. Reverted to Manual."
            return self.mark_manual(remarks=remarks)
