from pathlib import Path
import logging
import pdfplumber
from typing import Dict, Any

from src.core.base_profiler import BaseProfiler

logger = logging.getLogger("unstructured.profiler")

class UnstructuredProfiler(BaseProfiler):
    def __init__(self, config_path: Path):
        super().__init__(config_path, "unstructured")

    def detect_schema(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Profile PDF layouts (pages, digital/scanned status, tables, sections) and plain text files."""
        suffix = file_path.suffix.lower()
        schema = {"columns": [], "nested_fields": [], "type": "Unstructured"}

        if suffix == ".pdf":
            try:
                # Open PDF with pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    page_count = len(pdf.pages)
                    schema["pages"] = page_count
                    
                    # Test if digital or scanned by checking text on first page
                    first_page = pdf.pages[0]
                    first_page_text = first_page.extract_text()
                    is_digital = bool(first_page_text and first_page_text.strip())
                    schema["is_digital"] = is_digital
                    
                    # Inspect first page for embedded tables
                    tables = first_page.extract_tables()
                    schema["embedded_tables_count"] = len(tables)
                    
                    # Extract document headers/sections from the first page text
                    headers = []
                    if is_digital:
                        lines = first_page_text.split("\n")
                        for line in lines[:10]:
                            line_strip = line.strip()
                            if len(line_strip) > 3 and (line_strip.isupper() or any(title in line_strip for title in ["Section", "Standard", "Regulation", "GUIDELINE"])):
                                headers.append(line_strip)
                    schema["document_headers"] = headers
                    
                    # Map headers to mock columns for candidate entity matching
                    schema["columns"] = ["document_text", "extracted_table_rows"] + [h.lower().replace(" ", "_") for h in headers]
                    schema["type"] = "Digital PDF Document" if is_digital else "Scanned PDF Document"
            except Exception as e:
                logger.error(f"Error profiling PDF file {file_path}: {e}")
                schema["type"] = "Broken PDF"
                
        elif suffix == ".txt":
            try:
                # Profile text headers and lines count
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                    
                headers = [line for line in lines[:15] if len(line) > 3 and (line.isupper() or line.startswith(("- ", "* ", "1.", "2.")))]
                schema["lines_count"] = len(lines)
                schema["document_headers"] = headers
                schema["columns"] = ["raw_text"] + [h.lower().replace(" ", "_") for h in headers]
                schema["type"] = "Plain Text Document"
            except Exception as e:
                logger.error(f"Error profiling text file {file_path}: {e}")
                
        return schema

    def assess_quality(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Audit unstructured quality, warning about scanned files that need OCR."""
        schema_data = self.detect_schema(file_path, mime_type)
        suffix = file_path.suffix.lower()
        
        is_digital = schema_data.get("is_digital", True)
        # If it's a PDF and not digital, warning OCR needed, lower readiness
        ocr_required = suffix == ".pdf" and not is_digital
        
        readiness = 1.0
        if ocr_required:
            readiness = 0.5  # OCR needed, not directly queryable
        elif schema_data.get("type") == "Broken PDF":
            readiness = 0.0
            
        return {
            "valid_utf8": True,
            "broken_format": schema_data.get("type") == "Broken PDF",
            "completeness": 1.0,
            "consistency": 1.0,
            "ocr_required": ocr_required,
            "readiness_score": readiness,
            "total_records": schema_data.get("pages", 1)
        }
