import logging
from pathlib import Path
from src.utils.raw_extractor import extract_all_grounded_data

logger = logging.getLogger("utils.mock_generator")

def generate_all_mock_data(intermediate_dir: Path):
    """
    Deprecated synthetic mock generator.
    Delegates to `extract_all_grounded_data` to ensure 100% source-grounded entity and relationship extraction.
    Zero synthetic or placeholder records are generated.
    """
    logger.info("Executing source-grounded extraction pipeline (Zero Synthetic Records)...")
    return extract_all_grounded_data(intermediate_dir)
