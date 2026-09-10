from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

class GSFAHTMLCollector(BaseCollector):
    """
    GSFA Online HTML Scraper: Crawls Codex GSFA online sections
    (Food Categories, Food Additives, INS Numbers, Provisions)
    and saves the raw HTML pages.
    """
    async def collect(self) -> List[Path]:
        collected_files = []
        base_url = "https://www.fao.org/gsfaonline"
        
        # Core pages to scrape
        pages_to_scrape = {
            "gsfa_home.html": f"{base_url}/index.jsp",
            "gsfa_categories.html": f"{base_url}/foods/index.html",
            "gsfa_additives.html": f"{base_url}/additives/index.html",
            "gsfa_ins.html": f"{base_url}/additives/ins.html",
        }
        
        self.logger.info("GSFA Online Scraper: Crawling GSFA online pages...")
        
        for filename, url in pages_to_scrape.items():
            dest_path = self.dest_dir / filename
            try:
                data = self.http_client.get_sync(url)
                with open(dest_path, "wb") as f:
                    f.write(data)
                self.register_file(dest_path, "Downloaded", remarks=f"Scraped GSFA HTML page from {url}")
                collected_files.append(dest_path)
            except Exception as e:
                self.logger.warning(f"Failed to scrape GSFA page '{filename}' from {url}: {e}. Creating mock placeholder.")
                
                # Mock fallback HTML
                mock_content = (
                    f"<html><head><title>Mock {filename}</title></head>"
                    f"<body><h1>GSFA Online {filename}</h1><p>Source URL: {url}</p>"
                    f"<p>Failed to retrieve remote resource. Placeholder generated.</p></body></html>"
                )
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(mock_content)
                self.register_file(
                    dest_path, 
                    "Downloaded (Fallback)", 
                    remarks=f"Scrape failed ({e}). Created mock HTML file for {filename}."
                )
                collected_files.append(dest_path)
                
        return collected_files
