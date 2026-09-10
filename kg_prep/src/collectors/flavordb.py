import json
import asyncio
from pathlib import Path
from typing import List
import aiohttp
from src.base_collector import BaseCollector

class FlavorDBCollector(BaseCollector):
    """
    FlavorDB Collector: Crawls the FlavorDB2 website, downloads HTML pages, 
    and saves raw JSON responses for a sample of ingredient profiles.
    """
    async def collect(self) -> List[Path]:
        collected_files = []
        base_url = "https://cosylab.iiitd.edu.in/flavordb2"
        max_ids = self.config.get("max_ids_to_crawl", 20)
        
        self.logger.info(f"FlavorDB: starting crawl of landing page and up to {max_ids} entities.")
        
        # 1. Download Landing HTML
        home_html_path = self.dest_dir / "flavordb_home.html"
        try:
            home_data = self.http_client.get_sync(base_url)
            with open(home_html_path, "wb") as f:
                f.write(home_data)
            self.register_file(home_html_path, "Downloaded", remarks="Crawled FlavorDB2 landing page HTML.")
            collected_files.append(home_html_path)
        except Exception as e:
            self.logger.warning(f"Failed to crawl FlavorDB landing page: {e}")
            # Mock fallback if site is down
            with open(home_html_path, "w", encoding="utf-8") as f:
                f.write("<html><body>Mock FlavorDB landing page. Remote down.</body></html>")
            self.register_file(home_html_path, "Downloaded (Mock)", remarks=f"Crawl failed ({e}). Saved mock landing page.")
            collected_files.append(home_html_path)

        # 2. Download individual profiles
        async with aiohttp.ClientSession() as session:
            for idx in range(1, max_ids + 1):
                # We crawl two files for each entity: detail HTML and entities_json
                detail_url = f"{base_url}/entity_details?id={idx}"
                json_url = f"{base_url}/entities_json?id={idx}" # API endpoint
                
                # A. Detail HTML
                html_path = self.dest_dir / f"entity_{idx}.html"
                try:
                    await self.http_client.download_file_async(detail_url, html_path, session)
                    self.register_file(html_path, "Crawled", remarks=f"Crawled entity detail HTML for ID {idx}")
                    collected_files.append(html_path)
                except Exception as e:
                    self.logger.warning(f"Failed to crawl detail HTML for FlavorDB entity {idx}: {e}")
                
                # B. JSON response
                json_path = self.dest_dir / f"entity_{idx}.json"
                try:
                    await self.http_client.download_file_async(json_url, json_path, session)
                    self.register_file(json_path, "Crawled", remarks=f"Fetched entity profile JSON for ID {idx}")
                    collected_files.append(json_path)
                except Exception as e:
                    # In FlavorDB2, JSON URL may be under /entities_json or similar. If failing, create a stub JSON
                    self.logger.warning(f"Failed to fetch JSON for FlavorDB entity {idx}: {e}. Creating a fallback mock JSON.")
                    mock_json = {
                        "id": idx,
                        "name": f"Mock Ingredient {idx}",
                        "flavor_molecules": [{"molecule_name": f"Compound_{idx}", "pubchem_cid": 1000 + idx}],
                        "odor_descriptors": ["sweet", "fruity"]
                    }
                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(mock_json, f, indent=4)
                    self.register_file(json_path, "Crawled (Fallback)", remarks=f"API failed ({e}). Generated mock JSON profile.")
                    collected_files.append(json_path)
                
                # Short rate limit delay
                await asyncio.sleep(self.system_config.get("rate_limit_delay", 1.0))
                
        return collected_files
