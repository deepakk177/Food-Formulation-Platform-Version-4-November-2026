import aiohttp
from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

class FSSAICollector(BaseCollector):
    """
    FSSAI Collector: Downloads FSSAI food products standards and food additives regulations PDF.
    """
    async def collect(self) -> List[Path]:
        url = self.config.get("download_url")
        dest_filename = "FSSAI_Food_Products_Regulations.pdf"
        dest_path = self.dest_dir / dest_filename
        
        self.logger.info(f"FSSAI: downloading from {url}")
        
        if dest_path.exists() and dest_path.stat().st_size > 0:
            self.logger.info(f"FSSAI PDF already exists. Skipping download.")
            self.register_file(dest_path, "Existing", remarks="Skipped download (file exists).")
            return [dest_path]

        try:
            async with aiohttp.ClientSession() as session:
                await self.http_client.download_file_async(url, dest_path, session)
            self.register_file(dest_path, "Downloaded", remarks="Downloaded FSSAI regulations PDF.")
            return [dest_path]
        except Exception as e:
            self.logger.warning(f"Failed to download FSSAI PDF: {e}. Generating mock fallback regulatory doc.")
            
            fallback_txt = self.dest_dir / "FSSAI_Regulations_placeholder.txt"
            with open(fallback_txt, "w", encoding="utf-8") as f:
                f.write(
                    "Food Safety and Standards Authority of India (FSSAI)\n"
                    "Food Safety and Standards (Food Products Standards and Food Additives) Regulations\n"
                    "Status: Fallback placeholder (Download failed: {})\n"
                    "Scope: Standards for food products, limits for food additives, preservatives, colors, emulsifiers.\n".format(e)
                )
            self.register_file(
                fallback_txt, 
                "Downloaded (Fallback)", 
                remarks=f"Download failed ({e}). Generated mock FSSAI standard text file."
            )
            return [fallback_txt]
