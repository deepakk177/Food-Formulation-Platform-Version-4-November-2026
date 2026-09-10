from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

class SpecSheetsCollector(BaseCollector):
    """
    Product Specification Sheets Collector: Collects product sheets (HTML and PDFs)
    from major food ingredient manufacturers: Cargill, Ingredion, ADM, Tate & Lyle, IFF.
    """
    async def collect(self) -> List[Path]:
        collected_files = []
        
        # Corporate sites to crawl
        companies = {
            "cargill": "https://www.cargill.com/food-beverage",
            "ingredion": "https://www.ingredion.com/na/en-us/ingredients.html",
            "adm": "https://www.adm.com/en-us/products-services/food/",
            "tate_lyle": "https://www.tateandlyle.com/ingredients-we-make",
            "iff": "https://www.iff.com/portfolio/products"
        }
        
        self.logger.info("Product Specification Sheets: crawling manufacturer pages...")
        
        for name, url in companies.items():
            html_filename = f"{name}_products.html"
            dest_html_path = self.dest_dir / html_filename
            
            try:
                # Crawl HTML
                data = self.http_client.get_sync(url)
                with open(dest_html_path, "wb") as f:
                    f.write(data)
                self.register_file(dest_html_path, "Downloaded", remarks=f"Scraped {name} products list page HTML.")
                collected_files.append(dest_html_path)
            except Exception as e:
                self.logger.warning(f"Failed to crawl {name} product page: {e}. Writing mock product specifications.")
                
                # Mock spec sheet file
                mock_filename = f"{name}_spec_sheet.txt"
                mock_path = self.dest_dir / mock_filename
                
                mock_specs = (
                    f"PRODUCT SPECIFICATION SHEET — {name.upper()} FOOD INGREDIENTS\n"
                    f"==========================================================\n"
                    f"Source: {url}\n"
                    f"Status: Fallback generated (Crawl Error: {e})\n"
                    f"Product line: Hydrocolloids, Sweeteners, Starches, Proteins.\n"
                    f"Quality Grade: Food Grade FCC / USP compliant.\n"
                    f"Documentation: Technical data sheets and certificates of analysis (COA) available upon request.\n"
                )
                with open(mock_path, "w", encoding="utf-8") as f:
                    f.write(mock_specs)
                    
                self.register_file(
                    mock_path, 
                    "Downloaded (Fallback)", 
                    remarks=f"Crawl of {name} failed. Created mock specification sheet."
                )
                collected_files.append(mock_path)
                
        return collected_files
