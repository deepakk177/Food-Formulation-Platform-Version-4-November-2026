import asyncio
from pathlib import Path
from typing import List
import aiohttp
from src.base_collector import BaseCollector

class ProductLabelsCollector(BaseCollector):
    """
    Product Labels Collector: Downloads raw product label HTML pages from Open Food Facts.
    Uses configured barcodes.
    """
    async def collect(self) -> List[Path]:
        collected_files = []
        barcodes = self.config.get("barcodes", ["3017620422003"])
        
        self.logger.info(f"Product Labels: crawling HTML pages for {len(barcodes)} products on Open Food Facts")
        
        async with aiohttp.ClientSession() as session:
            for barcode in barcodes:
                url = f"https://world.openfoodfacts.org/product/{barcode}"
                dest_path = self.dest_dir / f"product_{barcode}.html"
                
                try:
                    await self.http_client.download_file_async(url, dest_path, session)
                    self.register_file(dest_path, "Downloaded", remarks=f"Scraped Open Food Facts product label HTML for barcode {barcode}.")
                    collected_files.append(dest_path)
                except Exception as e:
                    self.logger.warning(f"Failed to crawl product label {barcode}: {e}. Creating mock label.")
                    
                    mock_content = (
                        f"<html><head><title>Mock Product Label - {barcode}</title></head>"
                        f"<body><h1>Product Label for Barcode: {barcode}</h1>"
                        f"<p>Source URL: {url}</p>"
                        f"<p>Failed to retrieve online data. Fallback created (Error: {e}).</p>"
                        f"<div>Ingredients: Water, Sugar, Vegetable Oil, Emulsifiers, Flavouring.</div></body></html>"
                    )
                    with open(dest_path, "w", encoding="utf-8") as f:
                        f.write(mock_content)
                        
                    self.register_file(
                        dest_path, 
                        "Downloaded (Fallback)", 
                        remarks=f"Crawl failed ({e}). Generated mock product label HTML."
                    )
                    collected_files.append(dest_path)
                    
                # Short delay to respect Open Food Facts terms of service
                await asyncio.sleep(self.system_config.get("rate_limit_delay", 1.0))
                
        return collected_files
