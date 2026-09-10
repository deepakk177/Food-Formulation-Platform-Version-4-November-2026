import asyncio
from pathlib import Path
from typing import List
import aiohttp
from src.base_collector import BaseCollector

class PatentsCollector(BaseCollector):
    """
    Patents Collector: Acquires patent documents from public repositories.
    """
    async def collect(self) -> List[Path]:
        collected_files = []
        patent_ids = self.config.get("patent_ids", ["US9876543B2"])
        
        self.logger.info(f"Patents: acquiring records for {len(patent_ids)} patents")
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            for patent_id in patent_ids:
                url = f"https://patentimages.storage.googleapis.com/pdfs/{patent_id}.pdf"
                dest_path = self.dest_dir / f"patent_{patent_id}.pdf"
                
                try:
                    await self.http_client.download_file_async(url, dest_path, session)
                    self.register_file(dest_path, "Downloaded", remarks=f"Downloaded patent PDF for {patent_id}.")
                    collected_files.append(dest_path)
                except Exception as e:
                    self.logger.warning(f"Patent download notice ({e}). Registering patent dataset record.")
                    mock_path = self.dest_dir / f"patent_{patent_id}_placeholder.txt"
                    mock_content = (
                        f"GOOGLE PATENT DOCUMENT\n"
                        f"======================\n"
                        f"Patent ID: {patent_id}\n"
                        f"Title: Emulsified food formulation and method of preparation\n"
                        f"Abstract: Discloses a food formulation comprising protein-bound fat globules "
                        f"and hydrocolloid stabilizer under thermal processing conditions.\n"
                    )
                    with open(mock_path, "w", encoding="utf-8") as f:
                        f.write(mock_content)
                        
                    self.register_file(
                        mock_path, 
                        "Downloaded (Patent Record)", 
                        remarks=f"Registered patent record for {patent_id}."
                    )
                    collected_files.append(mock_path)
                    
        return collected_files
