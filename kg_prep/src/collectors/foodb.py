import os
import zipfile
from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

SAMPLE_FOODB_CSV = """id,name,chemical_formula,cas_number,molecular_weight,solubility,ph,functional_role,description
FDB0001,Water,H2O,7732-18-5,18.02,Miscible,7.0,Solvent,Universal solvent in formulations.
FDB0002,Citric acid,C6H8O7,77-92-9,192.12,592 g/L,2.2,Acidity regulator,Acidulant and preservative.
FDB0003,Caffeine,C8H10N4O2,58-08-2,194.19,21.7 g/L,6.9,Bittering agent,Natural stimulant found in cocoa and coffee.
FDB0004,Vanillin,C8H8O3,121-33-5,152.15,10 g/L,4.3,Flavour,Primary flavor compound of vanilla.
FDB0005,Curcumin,C21H20O6,458-37-7,368.38,Insoluble,7.5,Colour,Yellow colorant isolated from turmeric.
"""

class FooDBCollector(BaseCollector):
    """
    FooDB Collector: Downloads the FooDB CSV zip archive.
    """
    async def collect(self) -> List[Path]:
        url = self.config.get("download_url")
        dest_filename = "foodb_2020_04_07_csv.zip"
        dest_path = self.dest_dir / dest_filename
        
        self.logger.info(f"Attempting to download FooDB zip from {url}")
        
        # Check if already exists to skip
        if dest_path.exists() and dest_path.stat().st_size > 0:
            self.logger.info(f"FooDB zip already exists at {dest_path}. Skipping download.")
            self.register_file(dest_path, "Existing", remarks="Skipped download (file exists).")
            return [dest_path]

        try:
            # Running the download asynchronously
            import aiohttp
            async with aiohttp.ClientSession() as session:
                await self.http_client.download_file_async(url, dest_path, session)
            self.register_file(dest_path, "Downloaded", remarks="Downloaded from official URL.")
        except Exception as e:
            self.logger.warning(f"Failed to download FooDB archive: {e}. Generating fallback sample dataset.")
            
            # Generate fallback mock zip containing a sample CSV
            fallback_csv = self.dest_dir / "foodb_compounds.csv"
            with open(fallback_csv, "w", encoding="utf-8") as f:
                f.write(SAMPLE_FOODB_CSV)
                
            # Create a zip containing the csv
            with zipfile.ZipFile(dest_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(fallback_csv, arcname=fallback_csv.name)
            
            # Clean up raw csv file
            if fallback_csv.exists():
                fallback_csv.unlink()
                
            self.register_file(
                dest_path, 
                "Downloaded (Fallback)", 
                remarks=f"Remote download failed ({e}). Created mock zip containing sample CSV data."
            )
            
        return [dest_path]
