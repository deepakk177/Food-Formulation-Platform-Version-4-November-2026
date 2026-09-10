import aiohttp
from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

class CodexCollector(BaseCollector):
    """
    Codex Collector: Downloads Codex General Standard for Food Additives PDF (CXS 192-1995).
    """
    async def collect(self) -> List[Path]:
        url = self.config.get("download_url")
        dest_filename = "CXS_192e.pdf"
        dest_path = self.dest_dir / dest_filename
        
        self.logger.info(f"Codex Standards: downloading from {url}")
        
        if dest_path.exists() and dest_path.stat().st_size > 0:
            self.logger.info(f"Codex Standards PDF already exists. Skipping download.")
            self.register_file(dest_path, "Existing", remarks="Skipped download (file exists).")
            return [dest_path]

        try:
            async with aiohttp.ClientSession() as session:
                await self.http_client.download_file_async(url, dest_path, session)
            self.register_file(dest_path, "Downloaded", remarks="Downloaded official Codex GSFA CXS 192-1995 standard PDF.")
            return [dest_path]
        except Exception as e:
            self.logger.warning(f"Failed to download Codex Standards PDF: {e}. Generating mock fallback standard.")
            
            fallback_txt = self.dest_dir / "CXS_192e_placeholder.txt"
            with open(fallback_txt, "w", encoding="utf-8") as f:
                f.write(
                    "Codex Alimentarius General Standard for Food Additives\n"
                    "Document: CXS 192-1995\n"
                    "Status: Fallback placeholder (Download failed: {})\n"
                    "Scope: Maximum levels of food additives permitted for use in food categories.\n".format(e)
                )
            self.register_file(
                fallback_txt, 
                "Downloaded (Fallback)", 
                remarks=f"Download failed ({e}). Generated mock Codex GSFA standard text file."
            )
            return [fallback_txt]
