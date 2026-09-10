from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

class Recipe1MCollector(BaseCollector):
    """
    Recipe1M+ Collector: Since Recipe1M+ requires academic registration and approval,
    this collector registers the source in Manual Mode and creates the directory.
    """
    async def collect(self) -> List[Path]:
        remarks = (
            "Manual Download Required: Requires login and license agreement approval. "
            "Please register at http://im2recipe.csail.mit.edu/ to request access. "
            "Once approved, download 'layer1.json' and 'layer2.json' and place them "
            f"under the local directory: {self.dest_dir}"
        )
        return self.mark_manual(remarks=remarks)
