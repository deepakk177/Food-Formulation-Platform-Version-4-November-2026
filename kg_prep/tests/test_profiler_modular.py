import pytest
from pathlib import Path
import json
import yaml

from src.core.mime_detector import detect_mime_type, classify_by_mime
from src.structured_processor.profiler.engine import StructuredProfiler
from src.semi_structured_processor.profiler.engine import SemiStructuredProfiler
from src.unstructured_processor.profiler.engine import UnstructuredProfiler
from main_profiler import run_restructuring

def test_mime_detection(tmp_path):
    # Test JSON detection
    json_file = tmp_path / "test.json"
    json_file.write_text('{"key": "value"}', encoding="utf-8")
    assert detect_mime_type(json_file) == "application/json"
    assert classify_by_mime("application/json", json_file) == "Semi-Structured"

    # Test CSV detection
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\nval1,val2", encoding="utf-8")
    assert detect_mime_type(csv_file) == "text/csv"
    assert classify_by_mime("text/csv", csv_file) == "Structured"

    # Test OWL detection
    owl_file = tmp_path / "test.owl"
    owl_file.write_text('<?xml version="1.0"?><rdf:RDF xmlns="http://purl.obolibrary.org/obo/foodon.owl#"></rdf:RDF>', encoding="utf-8")
    assert detect_mime_type(owl_file) == "application/rdf+xml"
    assert classify_by_mime("application/rdf+xml", owl_file) == "Ontology"

def test_structured_profiler(tmp_path):
    # Setup mock structured config
    config_path = tmp_path / "structured_config.yaml"
    config_data = {
        "scanner": {
            "raw_dir": str(tmp_path),
            "output_dir": str(tmp_path / "reports"),
            "allowed_extensions": [".csv"]
        },
        "candidate_entities": {
            "Ingredient": {"keywords": ["col1", "ingredient"], "weight": 1.0}
        },
        "candidate_relationships": [],
        "builder_mappings": {
            "entity_builders": {"Ingredient": "IngredientBuilder"},
            "relationship_builders": {}
        }
    }
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config_data, f)

    # Create dummy CSV
    csv_dir = tmp_path / "foodb"
    csv_dir.mkdir()
    dummy_csv = csv_dir / "compounds.csv"
    dummy_csv.write_text("col1,col2\nval1,val2\nval3,val4", encoding="utf-8")

    # Run profiler
    profiler = StructuredProfiler(config_path)
    inv = profiler.scan_files()
    assert len(inv) == 1
    
    profiler.profile_all()
    assert "Foodb" in profiler.profiles
    
    profiler.generate_configs()
    profiler.generate_reports()
    
    # Assert generated files
    assert (tmp_path / "reports" / "dataset_registry.yaml").exists()
    assert (tmp_path / "reports" / "parser_config.yaml").exists()
    assert (tmp_path / "reports" / "schema_mapping_template.yaml").exists()
    assert (tmp_path / "reports" / "entity_builder_plan.json").exists()
    assert (tmp_path / "reports" / "relationship_builder_plan.json").exists()
    assert (tmp_path / "reports" / "datasets_summary.csv").exists()
    assert (tmp_path / "reports" / "datasets" / "Foodb_report.md").exists()

def test_semi_structured_profiler(tmp_path):
    # Setup mock semi-structured config
    config_path = tmp_path / "semi_structured_config.yaml"
    config_data = {
        "scanner": {
            "raw_dirs": [str(tmp_path / "semi_structured"), str(tmp_path / "ontology")],
            "output_dir": str(tmp_path / "reports"),
            "allowed_extensions": [".json", ".owl"]
        },
        "candidate_entities": {
            "Flavor": {"keywords": ["flavor"], "weight": 1.0}
        },
        "candidate_relationships": [],
        "builder_mappings": {
            "entity_builders": {"Flavor": "FlavorBuilder"},
            "relationship_builders": {}
        }
    }
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config_data, f)

    # Create directories
    (tmp_path / "semi_structured" / "flavordb").mkdir(parents=True)
    (tmp_path / "ontology").mkdir(parents=True)
    
    # Create dummy JSON
    dummy_json = tmp_path / "semi_structured" / "flavordb" / "entity_1.json"
    dummy_json.write_text('{"flavor": "sweet", "details": {"molecule": "vanillin"}}', encoding="utf-8")
    
    # Create dummy OWL
    dummy_owl = tmp_path / "ontology" / "foodon.owl"
    dummy_owl.write_text('<?xml version="1.0"?><rdf:RDF xmlns="http://purl.obolibrary.org/obo/foodon.owl#"><owl:Class rdf:about="http://purl.obolibrary.org/obo/FOODON_00000001"/></rdf:RDF>', encoding="utf-8")

    # Run profiler
    profiler = SemiStructuredProfiler(config_path)
    inv = profiler.scan_files()
    assert len(inv) == 2
    
    profiler.profile_all()
    profiler.generate_configs()
    profiler.generate_reports()
    
    assert (tmp_path / "reports" / "dataset_registry.yaml").exists()

def test_unstructured_profiler(tmp_path):
    # Setup mock unstructured config
    config_path = tmp_path / "unstructured_config.yaml"
    config_data = {
        "scanner": {
            "raw_dir": str(tmp_path),
            "output_dir": str(tmp_path / "reports"),
            "allowed_extensions": [".txt"]
        },
        "candidate_entities": {
            "Regulation": {"keywords": ["standard", "regulation"], "weight": 1.0}
        },
        "candidate_relationships": [],
        "builder_mappings": {
            "entity_builders": {"Regulation": "RegulationBuilder"},
            "relationship_builders": {}
        }
    }
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config_data, f)

    # Create dummy TXT
    txt_dir = tmp_path / "codex"
    txt_dir.mkdir()
    dummy_txt = txt_dir / "CXS_192e.txt"
    dummy_txt.write_text("STANDARD FOR FOOD ADDITIVES\nScope of the standard regulation.", encoding="utf-8")

    # Run profiler
    profiler = UnstructuredProfiler(config_path)
    inv = profiler.scan_files()
    assert len(inv) == 1
    
    profiler.profile_all()
    profiler.generate_configs()
    profiler.generate_reports()
    
    assert (tmp_path / "reports" / "dataset_registry.yaml").exists()
