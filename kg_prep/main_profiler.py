import os
import shutil
import logging
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("main_profiler")

# Import profiler classes
from src.structured_processor.profiler.engine import StructuredProfiler
from src.semi_structured_processor.profiler.engine import SemiStructuredProfiler
from src.unstructured_processor.profiler.engine import UnstructuredProfiler
from src.core.visualizer import generate_all_visualizations

def run_restructuring():
    """Restructure raw datasets into data/raw/ and copy foodon.owl ontology on startup."""
    logger.info("Checking directory structure...")
    
    workspace_dir = Path(".")
    data_dir = workspace_dir / "data"
    raw_dir = data_dir / "raw"
    
    # If data/raw does not exist, but subfolders exist under data/ directly, move them
    if not raw_dir.exists():
        logger.info("Initializing raw data lake at data/raw/...")
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        # Subdirectories to move
        subdirs = ["structured", "semi_structured", "unstructured"]
        for sd in subdirs:
            src_sd = data_dir / sd
            dst_sd = raw_dir / sd
            if src_sd.exists() and not dst_sd.exists():
                logger.info(f"Moving {src_sd} to {dst_sd}...")
                shutil.move(str(src_sd), str(dst_sd))
                
        # Root files to move
        root_files = ["metadata.json", "download_log.csv"]
        for rf in root_files:
            src_f = data_dir / rf
            dst_f = raw_dir / rf
            if src_f.exists() and not dst_f.exists():
                logger.info(f"Moving {src_f} to {dst_f}...")
                shutil.move(str(src_f), str(dst_f))
                
    # Ensure ontology folder exists
    ontology_dir = raw_dir / "ontology"
    ontology_dir.mkdir(parents=True, exist_ok=True)
    
    owl_file = ontology_dir / "foodon.owl"
    if not owl_file.exists():
        # Search pipeline scratch directories for foodon.owl
        sources = [
            Path("c:/Users/asus/.gemini/antigravity/scratch/extraction_scrapper_pipeline/raw/process/FoodProcessOntology/foodon.owl"),
            Path("c:/Users/asus/.gemini/antigravity/scratch/Data Extraction Pipeline/raw_data/FoodOn/foodon.owl")
        ]
        copied = False
        for src in sources:
            if src.exists():
                logger.info(f"Copying ontology from {src} to {owl_file}...")
                shutil.copy(str(src), str(owl_file))
                copied = True
                break
                
        if not copied:
            logger.warning("foodon.owl not found in search paths. Generating mock OWL file for testing...")
            # Create a simple mock owl
            mock_owl = """<?xml version="1.0"?>
<rdf:RDF xmlns="http://purl.obolibrary.org/obo/foodon.owl#"
     xml:base="http://purl.obolibrary.org/obo/foodon.owl"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
    <owl:Ontology rdf:about="http://purl.obolibrary.org/obo/foodon.owl"/>
    
    <owl:Class rdf:about="http://purl.obolibrary.org/obo/FOODON_00000001">
        <rdfs:label xml:lang="en">ingredient</rdfs:label>
    </owl:Class>
    <owl:Class rdf:about="http://purl.obolibrary.org/obo/FOODON_00000002">
        <rdfs:label xml:lang="en">food product</rdfs:label>
        <rdfs:subClassOf rdf:resource="http://purl.obolibrary.org/obo/FOODON_00000001"/>
    </owl:Class>
    <owl:ObjectProperty rdf:about="http://purl.obolibrary.org/obo/derives_from"/>
</rdf:RDF>"""
            with open(owl_file, "w", encoding="utf-8") as f:
                f.write(mock_owl)
                
    logger.info("Directory restructuring complete.")

def merge_and_save_global_reports(profilers: list):
    """Combine the three sub-reports into unified tables in reports/."""
    logger.info("Merging sub-profiler reports into global summaries...")
    global_reports_dir = Path("reports")
    global_reports_dir.mkdir(parents=True, exist_ok=True)
    
    inventories = []
    summaries = []
    
    parser_recs = []
    entity_cands = []
    rel_cands = []
    kg_contribs = []
    val_reports = []
    mod_recs = []
    
    for p in profilers:
        # Load inventories
        p_inv_file = p.output_dir / "inventory.csv"
        if p_inv_file.exists() and p_inv_file.stat().st_size > 0:
            try:
                inventories.append(pd.read_csv(p_inv_file))
            except Exception as e:
                logger.warning(f"Failed to read inventory {p_inv_file}: {e}")
            
        # Load summaries
        p_sum_file = p.output_dir / "datasets_summary.csv"
        if p_sum_file.exists() and p_sum_file.stat().st_size > 0:
            try:
                summaries.append(pd.read_csv(p_sum_file))
            except Exception as e:
                logger.warning(f"Failed to read summary {p_sum_file}: {e}")
            
        # Compile detail metrics from profiler profiles in-memory
        for ds_name, ds_info in p.profiles.items():
            # Module classification recommendation
            if p.domain == "structured":
                mod_name = "Module 2: Structured Processor"
            elif p.domain == "semi_structured":
                # Special cases for OWL
                if "owl" in ds_info["formats"]:
                    mod_name = "Module 5: Ontology / Knowledge Fusion"
                else:
                    mod_name = "Module 3: Semi-Structured Processor"
            else:
                mod_name = "Module 4: Unstructured Processor"
                
            mod_recs.append({
                "Dataset Name": ds_name,
                "Recommended Module": mod_name,
                "Size (KB)": round(ds_info["total_size_bytes"] / 1024, 2)
            })
            
            node_types = set()
            rel_types = set()
            
            for f_info in ds_info["files"]:
                # Parsers
                parser_recs.append({
                    "Dataset Name": ds_name,
                    "File Name": f_info["file_name"],
                    "Recommended Parser": "pandas" if f_info["file_name"].endswith((".csv", ".tsv")) else
                                          "orjson" if f_info["file_name"].endswith((".json", ".jsonl")) else
                                          "BeautifulSoup" if f_info["file_name"].endswith((".html", ".htm")) else
                                          "rdflib" if f_info["file_name"].endswith((".owl", ".rdf")) else
                                          "pdfplumber" if f_info["file_name"].endswith(".pdf") else "text_reader",
                    "MIME Type": f_info["mime_type"]
                })
                
                # Entities
                for ent in f_info["candidate_entities"]:
                    entity_cands.append({
                        "Dataset Name": ds_name,
                        "File Name": f_info["file_name"],
                        "Field": ent["field"],
                        "Candidate Entity": ent["candidate_entity"],
                        "Confidence": ent["confidence"]
                    })
                    node_types.add(ent["candidate_entity"])
                    
                # Relationships
                for rel in f_info["candidate_relationships"]:
                    rel_cands.append({
                        "Dataset Name": ds_name,
                        "File Name": f_info["file_name"],
                        "Source Entity": rel["source_entity"],
                        "Target Entity": rel["target_entity"],
                        "Relationship Type": rel["relationship_type"],
                        "Confidence": rel["confidence"]
                    })
                    rel_types.add(rel["relationship_type"])
                    
                # Validation Details
                val_reports.append({
                    "Dataset Name": ds_name,
                    "File Name": f_info["file_name"],
                    "Completeness": f_info["quality"].get("completeness", 1.0),
                    "Consistency": f_info["quality"].get("consistency", 1.0),
                    "Readiness Score": f_info["quality"].get("readiness_score", 1.0),
                    "Issues Detected": f_info["quality"].get("broken_format", False) or f_info["quality"].get("ocr_required", False)
                })
                
            kg_contribs.append({
                "Dataset Name": ds_name,
                "Possible Node Types": ", ".join(node_types) if node_types else "None",
                "Possible Relationship Types": ", ".join(rel_types) if rel_types else "None",
                "Confidence": round(sum(f["confidence"] for f in f_info["candidate_entities"])/len(f_info["candidate_entities"]), 2) if f_info["candidate_entities"] else 0.0
            })

    # Save merged dataframes
    if inventories:
        pd.concat(inventories, ignore_index=True).to_csv(global_reports_dir / "inventory.csv", index=False)
    if summaries:
        pd.concat(summaries, ignore_index=True).to_csv(global_reports_dir / "datasets_summary.csv", index=False)
        
    pd.DataFrame(parser_recs).to_csv(global_reports_dir / "parser_recommendations.csv", index=False)
    pd.DataFrame(entity_cands).to_csv(global_reports_dir / "entity_candidates.csv", index=False)
    pd.DataFrame(rel_cands).to_csv(global_reports_dir / "relationship_candidates.csv", index=False)
    pd.DataFrame(kg_contribs).to_csv(global_reports_dir / "kg_contribution.csv", index=False)
    pd.DataFrame(val_reports).to_csv(global_reports_dir / "validation_report.csv", index=False)
    pd.DataFrame(mod_recs).to_csv(global_reports_dir / "module_recommendation.csv", index=False)
    
    logger.info("Global report consolidation complete.")

def main():
    # 1. Directory Restructuring
    run_restructuring()
    
    # 2. Instantiate Profilers
    logger.info("Initializing Sub-Profilers...")
    structured_prof = StructuredProfiler(Path("config/structured_profiler.yaml"))
    semi_structured_prof = SemiStructuredProfiler(Path("config/semi_structured_profiler.yaml"))
    unstructured_prof = UnstructuredProfiler(Path("config/unstructured_profiler.yaml"))
    
    profilers = [structured_prof, semi_structured_prof, unstructured_prof]
    
    classification_counts = {
        "Structured": 0,
        "Semi-Structured": 0,
        "Unstructured": 0,
        "Ontology": 0
    }
    
    # 3. Execute individual profiling pipelines
    for p in profilers:
        p.scan_files()
        p.profile_all()
        p.generate_configs()
        p.generate_reports()
        
        # Accumulate classification metrics for visualizations
        for item in p.inventory:
            cls = item["Classification"]
            if cls in classification_counts:
                classification_counts[cls] += 1
                
    # 4. Merge reports into global reporting directory
    merge_and_save_global_reports(profilers)
    
    # 5. Generate visual charts
    logger.info("Generating visual reports...")
    generate_all_visualizations(classification_counts, Path("reports"))
    
    logger.info("[SUCCESS] Automated modular dataset profiling execution complete.")

if __name__ == "__main__":
    main()
