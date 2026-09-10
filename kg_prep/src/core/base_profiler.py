import os
import yaml
import json
import logging
from pathlib import Path
import pandas as pd
from typing import Dict, Any, List

from src.core.mime_detector import detect_mime_type, classify_by_mime
from src.core.quality_assessor import check_utf8_validity, audit_tabular_data, check_broken_json, check_broken_xml

logger = logging.getLogger("core.base_profiler")

class BaseProfiler:
    """
    Base configuration-driven Dataset Explorer & Profiler.
    Reusable for structured, semi-structured, and unstructured pipelines.
    """
    def __init__(self, config_path: Path, domain: str):
        self.config_path = config_path
        self.domain = domain
        self.config = self.load_config()
        
        # Resolve raw directory/directories
        self.raw_dirs = []
        scanner_conf = self.config.get("scanner", {})
        if "raw_dir" in scanner_conf:
            self.raw_dirs.append(Path(scanner_conf["raw_dir"]))
        elif "raw_dirs" in scanner_conf:
            self.raw_dirs.extend([Path(d) for d in scanner_conf["raw_dirs"]])
            
        self.output_dir = Path(scanner_conf.get("output_dir", f"reports/{self.domain}"))
        self.allowed_extensions = scanner_conf.get("allowed_extensions", [])
        
        # Initialize registries
        self.inventory: List[Dict[str, Any]] = []
        self.profiles: Dict[str, Dict[str, Any]] = {}
        
    def load_config(self) -> Dict[str, Any]:
        """Loads configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def scan_files(self) -> pd.DataFrame:
        """Scan raw directories recursively and build inventory."""
        self.inventory = []
        logger.info(f"Scanning raw files for domain: {self.domain}...")
        
        for raw_dir in self.raw_dirs:
            if not raw_dir.exists():
                logger.warning(f"Raw directory does not exist: {raw_dir}")
                continue
                
            for root, _, files in os.walk(raw_dir):
                for file in files:
                    file_path = Path(root, file)
                    suffix = file_path.suffix.lower()
                    
                    if self.allowed_extensions and suffix not in self.allowed_extensions:
                        continue
                        
                    # Calculate basic file metadata
                    mime = detect_mime_type(file_path)
                    classification = classify_by_mime(mime, file_path)
                    
                    # Compute SHA256 (simple block-based)
                    sha256 = self._calculate_sha256(file_path)
                    
                    # Resolve Dataset Name from path (e.g. structured/foodb -> FooDB)
                    dataset_name = file_path.parent.name.capitalize()
                    
                    self.inventory.append({
                        "File Name": file,
                        "Dataset Name": dataset_name,
                        "Extension": suffix[1:] if suffix else "unknown",
                        "MIME Type": mime,
                        "Size (Bytes)": file_path.stat().st_size,
                        "Parent Folder": str(file_path.parent.relative_to(raw_dir.parent.parent)),
                        "Last Modified": pd.to_datetime(file_path.stat().st_mtime, unit='s').strftime('%Y-%m-%d %H:%M:%S'),
                        "SHA256 Hash": sha256,
                        "Local Path": str(file_path.as_posix()),
                        "Classification": classification
                    })
                    
        cols = ["File Name", "Dataset Name", "Extension", "MIME Type", "Size (Bytes)", "Parent Folder", "Last Modified", "SHA256 Hash", "Local Path", "Classification"]
        df = pd.DataFrame(self.inventory, columns=cols)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_dir / "inventory.csv", index=False)
        logger.info(f"Saved inventory of {len(df)} files to {self.output_dir / 'inventory.csv'}")
        return df

    def _calculate_sha256(self, file_path: Path) -> str:
        import hashlib
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(65536), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return "N/A"

    def profile_all(self):
        """Profile each dataset file (Schema, Entities, Relationships, and Quality)."""
        logger.info(f"Profiling datasets for domain {self.domain}...")
        self.profiles = {}
        
        for item in self.inventory:
            file_path = Path(item["Local Path"])
            dataset_name = item["Dataset Name"]
            
            if dataset_name not in self.profiles:
                self.profiles[dataset_name] = {
                    "dataset_name": dataset_name,
                    "total_files": 0,
                    "total_size_bytes": 0,
                    "formats": set(),
                    "files": []
                }
                
            self.profiles[dataset_name]["total_files"] += 1
            self.profiles[dataset_name]["total_size_bytes"] += item["Size (Bytes)"]
            self.profiles[dataset_name]["formats"].add(item["Extension"])
            
            # Subclasses override detect_schema to fill file-specific schemas
            schema_data = self.detect_schema(file_path, item["MIME Type"])
            quality_data = self.assess_quality(file_path, item["MIME Type"])
            entities, relationships = self.detect_candidates(schema_data)
            
            self.profiles[dataset_name]["files"].append({
                "file_name": item["File Name"],
                "local_path": item["Local Path"],
                "mime_type": item["MIME Type"],
                "size_bytes": item["Size (Bytes)"],
                "schema": schema_data,
                "quality": quality_data,
                "candidate_entities": entities,
                "candidate_relationships": relationships
            })

    def detect_schema(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Generic schema detector. Subclasses must override with format-specific parsing."""
        return {"columns": [], "nested_fields": [], "type": "Generic"}

    def assess_quality(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Runs basic quality assessments based on file types."""
        is_utf8 = check_utf8_validity(file_path)
        is_broken = False
        
        if mime_type == "application/json":
            is_broken = check_broken_json(file_path)
        elif mime_type == "application/rdf+xml":
            is_broken = check_broken_xml(file_path)
            
        return {
            "valid_utf8": is_utf8,
            "broken_format": is_broken,
            "completeness": 1.0,
            "consistency": 1.0,
            "duplicate_records": 0,
            "readiness_score": 0.0 if is_broken else 1.0
        }

    def detect_candidates(self, schema_data: Dict[str, Any]) -> tuple:
        """Keyword matching engine for scoring candidate entities and relationships."""
        entity_conf = self.config.get("candidate_entities", {})
        rel_conf = self.config.get("candidate_relationships", [])
        
        detected_entities = []
        fields = schema_data.get("columns", []) + schema_data.get("nested_fields", [])
        
        # Entity matching
        for field in fields:
            field_lower = str(field).lower()
            best_match = None
            best_score = 0.0
            
            for ent_type, ent_rules in entity_conf.items():
                keywords = ent_rules.get("keywords", [])
                weight = ent_rules.get("weight", 1.0)
                
                # Check exact or substring overlap
                for kw in keywords:
                    if kw == field_lower:
                        score = 1.0 * weight
                    elif kw in field_lower:
                        score = 0.8 * weight
                    elif field_lower in kw:
                        score = 0.5 * weight
                    else:
                        score = 0.0
                        
                    if score > best_score:
                        best_score = score
                        best_match = ent_type
                        
            if best_match and best_score >= 0.5:
                detected_entities.append({
                    "field": field,
                    "candidate_entity": best_match,
                    "confidence": round(best_score, 2)
                })
                
        # Relationship matching
        detected_relationships = []
        entity_types = [e["candidate_entity"] for e in detected_entities]
        
        for rule in rel_conf:
            source = rule["source"]
            target = rule["target"]
            indicators = rule.get("co_occurrence_indicators", [])
            
            if source in entity_types and target in entity_types:
                # Find matching fields
                source_fields = [e["field"] for e in detected_entities if e["candidate_entity"] == source]
                target_fields = [e["field"] for e in detected_entities if e["candidate_entity"] == target]
                
                # Base confidence from product of entity confidences
                conf_s = max(e["confidence"] for e in detected_entities if e["candidate_entity"] == source)
                conf_t = max(e["confidence"] for e in detected_entities if e["candidate_entity"] == target)
                confidence = conf_s * conf_t
                
                detected_relationships.append({
                    "source_entity": source,
                    "target_entity": target,
                    "source_fields": source_fields,
                    "target_fields": target_fields,
                    "relationship_type": f"{source.upper().replace(' ', '_')}_TO_{target.upper().replace(' ', '_')}",
                    "confidence": round(confidence, 2)
                })
                
        return detected_entities, detected_relationships

    def generate_configs(self):
        """Generate downstream YAML and JSON configuration blueprints."""
        logger.info(f"Generating pipeline configurations for domain {self.domain}...")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. dataset_registry.yaml
        registry = {}
        for ds_name, ds_info in self.profiles.items():
            registry[ds_name] = {
                "classification": self.domain.capitalize(),
                "total_files": ds_info["total_files"],
                "total_size_bytes": ds_info["total_size_bytes"],
                "formats": list(ds_info["formats"]),
                "local_path": str(Path(ds_info["files"][0]["local_path"]).parent.as_posix())
            }
        with open(self.output_dir / "dataset_registry.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(registry, f, default_flow_style=False)
            
        # 2. parser_config.yaml
        parser_config = {}
        for ds_name, ds_info in self.profiles.items():
            parser_config[ds_name] = {"files": {}}
            for f_info in ds_info["files"]:
                mime = f_info["mime_type"]
                suffix = Path(f_info["file_name"]).suffix.lower()
                
                # Recommend Parser
                if suffix in [".csv", ".tsv"]:
                    parser = "pandas"
                elif suffix in [".json", ".jsonl"]:
                    parser = "orjson"
                elif suffix in [".html", ".htm"]:
                    parser = "BeautifulSoup"
                elif suffix in [".owl", ".rdf"]:
                    parser = "rdflib"
                elif suffix in [".pdf"]:
                    parser = "pdfplumber"
                elif suffix in [".txt"]:
                    parser = "text_reader"
                else:
                    parser = "unknown"
                    
                parser_config[ds_name]["files"][f_info["file_name"]] = {
                    "parser": parser,
                    "mime_type": mime,
                    "encoding": "utf-8"
                }
        with open(self.output_dir / "parser_config.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(parser_config, f, default_flow_style=False)
            
        # 3. schema_mapping_template.yaml
        schema_mapping = {}
        for ds_name, ds_info in self.profiles.items():
            schema_mapping[ds_name] = {}
            for f_info in ds_info["files"]:
                f_name = f_info["file_name"]
                schema_mapping[ds_name][f_name] = {
                    "schema_type": f_info["schema"].get("type", "Generic"),
                    "mappings": {}
                }
                for ent in f_info["candidate_entities"]:
                    schema_mapping[ds_name][f_name]["mappings"][ent["field"]] = {
                        "target_entity": ent["candidate_entity"],
                        "confidence": ent["confidence"]
                    }
        with open(self.output_dir / "schema_mapping_template.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(schema_mapping, f, default_flow_style=False)
            
        # 4. entity_builder_plan.json
        builder_map = self.config.get("builder_mappings", {}).get("entity_builders", {})
        entity_plan = {}
        for ds_name, ds_info in self.profiles.items():
            entity_plan[ds_name] = {"builders": {}}
            for f_info in ds_info["files"]:
                for ent in f_info["candidate_entities"]:
                    ent_type = ent["candidate_entity"]
                    builder_class = builder_map.get(ent_type, "GenericEntityBuilder")
                    
                    if ent_type not in entity_plan[ds_name]["builders"]:
                        entity_plan[ds_name]["builders"][ent_type] = {
                            "builder_class": builder_class,
                            "fields": []
                        }
                    entity_plan[ds_name]["builders"][ent_type]["fields"].append(ent["field"])
        with open(self.output_dir / "entity_builder_plan.json", "w", encoding="utf-8") as f:
            json.dump(entity_plan, f, indent=4)
            
        # 5. relationship_builder_plan.json
        rel_map = self.config.get("builder_mappings", {}).get("relationship_builders", {})
        rel_plan = {}
        for ds_name, ds_info in self.profiles.items():
            rel_plan[ds_name] = {"relationships": []}
            for f_info in ds_info["files"]:
                for rel in f_info["candidate_relationships"]:
                    key = f"{rel['source_entity']} -> {rel['target_entity']}"
                    builder_class = rel_map.get(key, "GenericRelationshipBuilder")
                    
                    rel_plan[ds_name]["relationships"].append({
                        "relationship_type": rel["relationship_type"],
                        "builder_class": builder_class,
                        "source": {
                            "entity": rel["source_entity"],
                            "fields": rel["source_fields"]
                        },
                        "target": {
                            "entity": rel["target_entity"],
                            "fields": rel["target_fields"]
                        },
                        "confidence": rel["confidence"]
                    })
        with open(self.output_dir / "relationship_builder_plan.json", "w", encoding="utf-8") as f:
            json.dump(rel_plan, f, indent=4)

        logger.info("Configuration files generated.")

    def generate_reports(self):
        """Generates datasets_summary.csv and detailed markdown reports."""
        logger.info(f"Generating profiling reports for domain {self.domain}...")
        
        # 1. datasets_summary.csv
        summary_rows = []
        for ds_name, ds_info in self.profiles.items():
            avg_readiness = 0.0
            total_records = 0
            all_quality = [f["quality"] for f in ds_info["files"]]
            if all_quality:
                avg_readiness = sum(q.get("readiness_score", 0.0) for q in all_quality) / len(all_quality)
                total_records = sum(q.get("total_records", 0) for q in all_quality)
                
            summary_rows.append({
                "Dataset Name": ds_name,
                "Total Files": ds_info["total_files"],
                "Total Size (KB)": round(ds_info["total_size_bytes"] / 1024, 2),
                "Formats": ", ".join(ds_info["formats"]),
                "Approximate Records": total_records,
                "Readiness Score": round(avg_readiness, 4)
            })
        cols = ["Dataset Name", "Total Files", "Total Size (KB)", "Formats", "Approximate Records", "Readiness Score"]
        summary_df = pd.DataFrame(summary_rows, columns=cols)
        summary_df.to_csv(self.output_dir / "datasets_summary.csv", index=False)
        
        # 2. Markdown files under reports/{domain}/datasets/
        ds_report_dir = self.output_dir / "datasets"
        ds_report_dir.mkdir(parents=True, exist_ok=True)
        
        for ds_name, ds_info in self.profiles.items():
            report_lines = [
                f"# Dataset Profiling Report: {ds_name}",
                "",
                f"*   **Domain**: {self.domain.capitalize()}",
                f"*   **Total Files**: {ds_info['total_files']}",
                f"*   **Total Size**: {round(ds_info['total_size_bytes']/1024, 2)} KB",
                f"*   **Formats**: {', '.join(ds_info['formats'])}",
                "",
                "## Files Inspected",
                ""
            ]
            for f in ds_info["files"]:
                report_lines.extend([
                    f"### `{f['file_name']}`",
                    f"*   **Path**: `{f['local_path']}`",
                    f"*   **MIME Type**: `{f['mime_type']}`",
                    f"*   **Size**: {round(f['size_bytes']/1024, 2)} KB",
                    "",
                    "#### Schema Details",
                    f"*   **Schema Type**: {f['schema'].get('type', 'Generic')}",
                ])
                if f["schema"].get("columns"):
                    report_lines.append(f"*   **Columns**: {', '.join(map(str, f['schema']['columns']))}")
                if f["schema"].get("nested_fields"):
                    report_lines.append(f"*   **Nested JSON Paths**: {', '.join(map(str, f['schema']['nested_fields']))}")
                if f["schema"].get("pages"):
                    report_lines.append(f"*   **PDF Pages**: {f['schema']['pages']}")
                    report_lines.append(f"*   **Digital Document**: {f['schema'].get('is_digital', True)}")
                    
                report_lines.extend([
                    "",
                    "#### Data Quality",
                    f"*   **Readiness Score**: {f['quality'].get('readiness_score', 1.0)}",
                    f"*   **Valid UTF-8**: {f['quality'].get('valid_utf8', True)}",
                    f"*   **Broken Format**: {f['quality'].get('broken_format', False)}",
                    f"*   **Duplicate Rows**: {f['quality'].get('duplicate_records', 0)}",
                ])
                if f["quality"].get("empty_columns"):
                    report_lines.append(f"*   **Empty Columns**: {', '.join(f['quality']['empty_columns'])}")
                if f["quality"].get("mixed_type_columns"):
                    report_lines.append(f"*   **Mixed Type Columns**: {', '.join(f['quality']['mixed_type_columns'])}")
                if f["quality"].get("unit_inconsistencies"):
                    report_lines.append(f"*   **Unit Inconsistencies**: `{json.dumps(f['quality']['unit_inconsistencies'])}`")
                    
                report_lines.extend([
                    "",
                    "#### Candidate Entities Mapping",
                ])
                if f["candidate_entities"]:
                    for ent in f["candidate_entities"]:
                        report_lines.append(f"*   Field `{ent['field']}` $\\rightarrow$ **{ent['candidate_entity']}** (Confidence: {ent['confidence']})")
                else:
                    report_lines.append("*   No entities detected.")
                    
                report_lines.extend([
                    "",
                    "#### Candidate Relationships Mapping",
                ])
                if f["candidate_relationships"]:
                    for rel in f["candidate_relationships"]:
                        report_lines.append(f"*   **{rel['relationship_type']}**: `{rel['source_entity']}` ({', '.join(rel['source_fields'])}) $\\rightarrow$ `{rel['target_entity']}` ({', '.join(rel['target_fields'])}), Confidence: {rel['confidence']}")
                else:
                    report_lines.append("*   No relationships detected.")
                report_lines.append("\n---")
                
            with open(ds_report_dir / f"{ds_name}_report.md", "w", encoding="utf-8") as rf:
                rf.write("\n".join(report_lines))
        logger.info("Markdown reports generated.")
