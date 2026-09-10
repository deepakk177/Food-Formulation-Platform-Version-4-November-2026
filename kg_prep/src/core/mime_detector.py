import os
import mimetypes
from pathlib import Path
import logging

logger = logging.getLogger("core.mime_detector")

# Attempt importing python-magic (might require DLLs on Windows)
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False
    logger.warning("python-magic not installed or missing DLLs. Using mimetypes and byte signature fallbacks.")

# Common magic byte signatures
SIGNATURES = {
    b"%PDF-": "application/pdf",
    b"PK\x03\x04": "application/zip",
    b"SQLite format 3\x00": "application/x-sqlite3",
}

def detect_mime_type(file_path: Path) -> str:
    """
    Detect the MIME type of a file with fallback strategies for Windows.
    """
    if not file_path.exists() or file_path.is_dir():
        return "application/octet-stream"

    # Strategy 1: Attempt python-magic if available
    if HAS_MAGIC:
        try:
            mime = magic.from_file(str(file_path), mime=True)
            if mime:
                # Clarify text/plain for some configurations
                if mime == "text/plain" and file_path.suffix in [".json", ".jsonl"]:
                    return "application/json"
                return mime
        except Exception as e:
            logger.debug(f"Magic detection failed for {file_path}: {e}")

    # Strategy 2: Check binary file signatures (magic bytes)
    try:
        with open(file_path, "rb") as f:
            header = f.read(1024)
            for sig, mime_type in SIGNATURES.items():
                if header.startswith(sig):
                    return mime_type
            
            # Simple text checks for JSON, XML, HTML, OWL
            if header:
                try:
                    text_preview = header.decode("utf-8", errors="ignore").strip().lower()
                    if text_preview.startswith(("{", "[")):
                        return "application/json"
                    if text_preview.startswith("<?xml") or "<rdf:rdf" in text_preview or "<owl:" in text_preview:
                        return "application/rdf+xml"
                    if text_preview.startswith("<!doctype html") or "<html" in text_preview:
                        return "text/html"
                except Exception:
                    pass
    except Exception as e:
        logger.debug(f"Byte signature check failed for {file_path}: {e}")

    # Strategy 3: Extension-based fallback
    mime, _ = mimetypes.guess_type(str(file_path))
    if mime:
        if mime == "application/vnd.ms-excel" and file_path.suffix == ".csv":
            return "text/csv"
        if mime == "text/plain":
            if file_path.suffix == ".json":
                return "application/json"
            if file_path.suffix == ".jsonl":
                return "application/jsonl"
            if file_path.suffix == ".owl":
                return "application/rdf+xml"
        return mime

    # Default fallback
    suffix = file_path.suffix.lower()
    if suffix == ".json":
        return "application/json"
    elif suffix == ".jsonl":
        return "application/jsonl"
    elif suffix in [".xml", ".owl", ".rdf"]:
        return "application/rdf+xml"
    elif suffix in [".html", ".htm"]:
        return "text/html"
    elif suffix in [".csv"]:
        return "text/csv"
    elif suffix in [".tsv"]:
        return "text/tab-separated-values"
    elif suffix in [".pdf"]:
        return "application/pdf"
    elif suffix in [".txt"]:
        return "text/plain"
    
    return "application/octet-stream"

def classify_by_mime(mime_type: str, file_path: Path) -> str:
    """
    Classify dataset into Structured, Semi-Structured, Unstructured, or Ontology based on MIME type or path.
    """
    suffix = file_path.suffix.lower()
    
    # Check explicitly for Ontology directory or extensions
    if "ontology" in str(file_path.parent).lower() or suffix in [".owl", ".rdf", ".ttl"]:
        return "Ontology"
        
    if mime_type in ["text/csv", "text/tab-separated-values", "application/x-sqlite3", "application/vnd.ms-excel"]:
        return "Structured"
    elif mime_type in ["application/json", "application/jsonl", "application/rdf+xml", "text/html"]:
        return "Semi-Structured"
    elif mime_type in ["application/pdf", "text/plain"] or mime_type.startswith("image/"):
        return "Unstructured"
        
    return "Unknown"
