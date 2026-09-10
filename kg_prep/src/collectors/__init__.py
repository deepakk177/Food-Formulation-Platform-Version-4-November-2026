from .foodb import FooDBCollector
from .usda import USDAFDCCollector
from .recipe1m import Recipe1MCollector
from .nutrition5k import Nutrition5KCollector
from .gsfa_xml import GSFAXMLCollector
from .flavordb import FlavorDBCollector
from .gsfa_html import GSFAHTMLCollector
from .spec_sheets import SpecSheetsCollector
from .product_labels import ProductLabelsCollector
from .ins import INSCollector
from .codex import CodexCollector
from .fssai import FSSAICollector
from .research import ResearchPapersCollector
from .patents import PatentsCollector
from .combase import ComBaseCollector
from .nectar import NectarCollector
from .texture import TextureCollector
from .sustainability import SustainabilityCollector
from .scoring_models import ScoringModelsCollector
from .foodcom import FoodComCollector

COLLECTOR_REGISTRY = {
    "foodb": FooDBCollector,
    "usda_fdc": USDAFDCCollector,
    "recipe1m": Recipe1MCollector,
    "nutrition5k": Nutrition5KCollector,
    "gsfa_xml": GSFAXMLCollector,
    "flavordb": FlavorDBCollector,
    "gsfa_html": GSFAHTMLCollector,
    "specification_sheets": SpecSheetsCollector,
    "product_labels": ProductLabelsCollector,
    "ins": INSCollector,
    "codex": CodexCollector,
    "fssai": FSSAICollector,
    "research_papers": ResearchPapersCollector,
    "patents": PatentsCollector,
    "combase": ComBaseCollector,
    "nectar": NectarCollector,
    "texture": TextureCollector,
    "sustainability": SustainabilityCollector,
    "scoring_models": ScoringModelsCollector,
    "foodcom": FoodComCollector,
}

__all__ = ["COLLECTOR_REGISTRY"]
