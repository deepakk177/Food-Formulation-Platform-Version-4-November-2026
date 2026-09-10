import aiohttp
from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

class INSCollector(BaseCollector):
    """
    INS Numbering System Collector: Downloads the Codex International Numbering
    System for Food Additives PDF (CXG 36-1989).
    """
    async def collect(self) -> List[Path]:
        url = self.config.get("download_url")
        dest_filename = "CXG_036e.pdf"
        dest_path = self.dest_dir / dest_filename
        
        self.logger.info(f"INS Numbering: downloading from {url}")
        
        if dest_path.exists() and dest_path.stat().st_size > 0:
            self.logger.info(f"INS Numbering PDF already exists. Skipping download.")
            self.register_file(dest_path, "Existing", remarks="Skipped download (file exists).")
            return [dest_path]

        try:
            async with aiohttp.ClientSession() as session:
                await self.http_client.download_file_async(url, dest_path, session)
            self.register_file(dest_path, "Downloaded", remarks="Downloaded official Codex INS numbering system PDF.")
            return [dest_path]
        except Exception as e:
            self.logger.warning(f"Failed to download Codex INS PDF: {e}. Generating mock fallback standard.")
            
            fallback_txt = self.dest_dir / "CXG_036e_placeholder.txt"
            with open(fallback_txt, "w", encoding="utf-8") as f:
                f.write(
                    "Codex Alimentarius Guidelines — Class Names and the International Numbering System\n"
                    "Document: CXG 36-1989\n"
                    "Status: Fallback placeholder (Download failed: {})\n"
                    "List of Additives:\n"
                    "- 100(i): Curcumin (Color)\n"
                    "- 322(i): Lecithins (Emulsifier)\n"
                    "- 415: Xanthan gum (Thickener, Stabilizer)\n".format(e)
                )
            self.register_file(
                fallback_txt, 
                "Downloaded (Fallback)", 
                remarks=f"Download failed ({e}). Generated mock INS guideline text file."
            )
            return [fallback_txt]
