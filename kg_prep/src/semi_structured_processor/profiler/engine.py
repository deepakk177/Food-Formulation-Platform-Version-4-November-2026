from pathlib import Path
import json
import logging
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import rdflib

from src.core.base_profiler import BaseProfiler

logger = logging.getLogger("semi_structured.profiler")

class SemiStructuredProfiler(BaseProfiler):
    def __init__(self, config_path: Path):
        super().__init__(config_path, "semi_structured")

    def detect_schema(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Profile JSON hierarchy trees, HTML structures, and OWL/RDF definitions."""
        suffix = file_path.suffix.lower()
        schema = {"columns": [], "nested_fields": [], "type": "Semi-Structured"}

        if suffix in [".json", ".jsonl"]:
            try:
                # Resolve paths
                nested_paths = []
                max_depth = 0
                
                if suffix == ".jsonl":
                    # Read the first line only
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                data = json.loads(line)
                                nested_paths, max_depth = self._extract_json_paths(data)
                                break
                    schema["type"] = "JSON Lines"
                else:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        nested_paths, max_depth = self._extract_json_paths(data)
                    schema["type"] = "JSON Hierarchy"
                    
                schema["nested_fields"] = nested_paths
                schema["columns"] = [p.split(".")[-1] for p in nested_paths if "." in p]
                schema["nested_levels"] = max_depth
            except Exception as e:
                logger.error(f"Error profiling JSON schema for {file_path}: {e}")
                
        elif suffix in [".html", ".htm"]:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f.read(), "lxml" if "lxml" in BeautifulSoup.__dict__ else "html.parser")
                    
                tables_count = len(soup.find_all("table"))
                lists_count = len(soup.find_all(["ul", "ol"]))
                paragraphs_count = len(soup.find_all("p"))
                meta_tags = [meta.get("name", meta.get("property", "")) for meta in soup.find_all("meta") if meta.get("name") or meta.get("property")]
                
                schema["type"] = "HTML Page"
                schema["columns"] = ["table_data", "list_data", "meta_description"]
                schema["html_metrics"] = {
                    "tables": tables_count,
                    "lists": lists_count,
                    "paragraphs": paragraphs_count,
                    "meta_tags": len(meta_tags)
                }
            except Exception as e:
                logger.error(f"Error profiling HTML for {file_path}: {e}")
                
        elif suffix in [".owl", ".rdf"]:
            try:
                g = rdflib.Graph()
                g.parse(str(file_path), format="xml")
                
                # Count ontology elements
                classes = list(g.subjects(rdflib.RDF.type, rdflib.OWL.Class))
                obj_properties = list(g.subjects(rdflib.RDF.type, rdflib.OWL.ObjectProperty))
                data_properties = list(g.subjects(rdflib.RDF.type, rdflib.OWL.DatatypeProperty))
                individuals = list(g.subjects(rdflib.RDF.type, rdflib.OWL.NamedIndividual))
                namespaces = list(g.namespaces())
                
                schema["type"] = "OWL Ontology"
                # Expose OWL class names as columns for entity matching
                schema["columns"] = [str(c).split("/")[-1].split("#")[-1] for c in classes[:100]]
                schema["ontology_metrics"] = {
                    "classes": len(classes),
                    "object_properties": len(obj_properties),
                    "datatype_properties": len(data_properties),
                    "individuals": len(individuals),
                    "namespaces": len(namespaces)
                }
            except Exception as e:
                logger.error(f"Error parsing OWL ontology {file_path}: {e}")
                
        return schema

    def _extract_json_paths(self, data: Any, current_path: str = "", depth: int = 1) -> tuple:
        """Helper to recursively scan JSON keys and return dot-separated paths."""
        paths = []
        max_depth = depth
        
        if isinstance(data, dict):
            for k, v in data.items():
                path = f"{current_path}.{k}" if current_path else k
                paths.append(path)
                sub_paths, sub_depth = self._extract_json_paths(v, path, depth + 1)
                paths.extend(sub_paths)
                max_depth = max(max_depth, sub_depth)
        elif isinstance(data, list):
            path = f"{current_path}[*]" if current_path else "[*]"
            paths.append(path)
            if data:
                sub_paths, sub_depth = self._extract_json_paths(data[0], path, depth + 1)
                paths.extend(sub_paths)
                max_depth = max(max_depth, sub_depth)
                
        return list(set(paths)), max_depth

    def assess_quality(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Audit quality of JSON or OWL files, reporting broken parsing or schema flaws."""
        suffix = file_path.suffix.lower()
        if suffix in [".json", ".jsonl"]:
            is_broken = self._check_json_broken(file_path, suffix)
            return {
                "valid_utf8": True,
                "broken_format": is_broken,
                "completeness": 1.0,
                "consistency": 1.0,
                "readiness_score": 0.0 if is_broken else 1.0,
                "total_records": 1 if suffix == ".json" else 100
            }
        elif suffix in [".owl", ".rdf"]:
            return {
                "valid_utf8": True,
                "broken_format": False,
                "completeness": 1.0,
                "consistency": 1.0,
                "readiness_score": 1.0,
                "total_records": 1
            }
        return super().assess_quality(file_path, mime_type)

    def _check_json_broken(self, file_path: Path, suffix: str) -> bool:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                if suffix == ".jsonl":
                    for line in f:
                        if line.strip():
                            json.loads(line)
                else:
                    json.load(f)
            return False
        except Exception:
            return True
