"""
Pipeline V2 FoodOn Extractor Module.

Performs streaming extraction of genuine RDF/XML FoodOn classes from foodon.owl.
Preserves native class identifiers, labels, definitions, synonyms, parent classes,
deprecation flags, and external database cross-references.

Invariants:
- Does NOT classify every class as an ingredient (preserves native source_entity_type='OWL_CLASS').
- Does NOT discard non-ingredient concepts.
- Does NOT invent or fabricate relationships.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Union, Generator

from pipeline_v2.core.exceptions import CorruptedAssetError, AssetNotFoundError
from pipeline_v2.core.logging_config import setup_logger
from pipeline_v2.models.source_record_models import (
    SourceRecord,
    ExtractionStatus,
    ExtractionBatchResult,
)


class FoodonExtractor:
    """Streaming extractor for FoodOn OWL ontology files."""

    SOURCE_ID = "SRC-FOODON"
    DATASET_ID = "DSK-FOODON-2024-03"

    # RDF / OWL XML Namespaces
    RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"
    RDF_RESOURCE = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"

    def __init__(self, execution_id: Optional[str] = None):
        self.logger = setup_logger("foodon_extractor", execution_id=execution_id)

    def extract_records(
        self,
        owl_file_path: Union[str, Path],
        raw_asset_id: str,
        max_records: Optional[int] = None,
    ) -> ExtractionBatchResult:
        """
        Parses foodon.owl in a memory-safe streaming fashion.
        Returns ExtractionBatchResult containing list of source-native SourceRecord models.
        """
        path = Path(owl_file_path)
        if not path.exists():
            raise AssetNotFoundError(f"FoodOn OWL file not found: {path}")

        result = ExtractionBatchResult(
            source_id=self.SOURCE_ID,
            dataset_id=self.DATASET_ID,
            asset_id=raw_asset_id,
        )

        record_count = 0
        try:
            # iterparse on closing tags
            context = ET.iterparse(str(path), events=("end",))
            for event, elem in context:
                if not elem.tag.endswith("Class"):
                    continue

                about = elem.attrib.get(self.RDF_ABOUT)
                if not about:
                    elem.clear()
                    continue

                result.total_records_discovered += 1

                # Extract labels
                labels = [c.text.strip() for c in elem if c.tag.endswith("label") and c.text]
                primary_name = labels[0] if labels else about.split("/")[-1]

                # Extract definitions (IAO_0000115)
                definitions = [
                    c.text.strip() for c in elem if c.tag.endswith("IAO_0000115") and c.text
                ]
                definition = definitions[0] if definitions else None

                # Extract parent classes (rdfs:subClassOf with rdf:resource)
                parent_iris = []
                subclass_expressions = []
                for c in elem:
                    if c.tag.endswith("subClassOf"):
                        res = c.attrib.get(self.RDF_RESOURCE)
                        if res:
                            parent_iris.append(res)
                        else:
                            # Anonymous restriction or blank node expression
                            try:
                                subclass_expressions.append(ET.tostring(c, encoding="unicode"))
                            except Exception:
                                pass

                # Extract synonyms
                synonyms = []
                for c in elem:
                    tag_name = c.tag.split("}")[-1]
                    if "Synonym" in tag_name and c.text:
                        synonyms.append(c.text.strip())

                # Extract external cross-references (hasDbXref)
                db_xrefs = []
                for c in elem:
                    if c.tag.endswith("hasDbXref") and c.text:
                        db_xrefs.append(c.text.strip())

                # Check deprecation
                is_deprecated = any(
                    c.text == "true" for c in elem if c.tag.endswith("deprecated")
                )

                # Extract replacement identifiers (IAO_0100001: term replaced by)
                replacement_iris = []
                for c in elem:
                    if c.tag.endswith("IAO_0100001"):
                        repl = c.attrib.get(self.RDF_RESOURCE) or c.text
                        if repl:
                            replacement_iris.append(repl.strip())

                # Format native identifier
                # e.g. http://purl.obolibrary.org/obo/FOODON_00001002 -> FOODON:00001002
                native_curie = about.split("/")[-1].replace("_", ":")

                payload = {
                    "about_iri": about,
                    "curie": native_curie,
                    "label": primary_name,
                    "all_labels": labels,
                    "definition": definition,
                    "parent_iris": parent_iris,
                    "subclass_expressions": subclass_expressions,
                    "synonyms": synonyms,
                    "database_cross_references": db_xrefs,
                    "is_deprecated": is_deprecated,
                    "replacement_iris": replacement_iris,
                }

                # Validation & Quality filter
                if not primary_name or primary_name.startswith("http"):
                    status = ExtractionStatus.REQUIRES_REVIEW
                    result.total_records_review += 1
                else:
                    status = ExtractionStatus.EXTRACTED
                    result.total_records_extracted += 1

                source_record = SourceRecord(
                    source_id=self.SOURCE_ID,
                    dataset_id=self.DATASET_ID,
                    source_record_id=native_curie,
                    source_entity_type="OWL_CLASS",
                    original_identifier=about,
                    original_name=primary_name,
                    original_fields=payload,
                    raw_asset_id=raw_asset_id,
                    source_location=f"{path.name}#{about.split('/')[-1]}",
                    extraction_status=status,
                    metadata={"curie_prefix": native_curie.split(":")[0]},
                )

                result.records.append(source_record)
                record_count += 1

                elem.clear()

                if max_records and record_count >= max_records:
                    break

        except ET.ParseError as pe:
            self.logger.error(f"XML parse error in {path}: {pe}")
            result.errors.append({"error": "XML_PARSE_ERROR", "details": str(pe)})
            raise CorruptedAssetError(f"FoodOn OWL file corrupted or truncated: {pe}")

        self.logger.info(
            f"Extracted {len(result.records)} FoodOn records from {path.name} "
            f"(Discovered: {result.total_records_discovered}, Extracted: {result.total_records_extracted})"
        )
        return result

    def stream_records(
        self,
        owl_file_path: Union[str, Path],
        raw_asset_id: str,
        chunk_size: int = 5000,
        max_records: Optional[int] = None,
    ) -> Generator[List[SourceRecord], None, None]:
        """
        Streams FoodOn classes in chunks of chunk_size to maintain constant O(1) memory.
        Yields List[SourceRecord] per chunk.
        """
        path = Path(owl_file_path)
        if not path.exists():
            raise AssetNotFoundError(f"FoodOn OWL file not found at {path}")

        current_chunk: List[SourceRecord] = []
        record_count = 0

        try:
            for event, elem in ET.iterparse(str(path), events=("end",)):
                if not elem.tag.endswith("Class"):
                    continue

                about = elem.attrib.get(self.RDF_ABOUT)
                if not about:
                    elem.clear()
                    continue

                # Extract labels
                labels = [c.text.strip() for c in elem if c.tag.endswith("label") and c.text]
                primary_name = labels[0] if labels else about.split("/")[-1]

                definitions = [
                    c.text.strip() for c in elem if c.tag.endswith("IAO_0000115") and c.text
                ]
                definition = definitions[0] if definitions else None

                parent_iris = []
                subclass_expressions = []
                for c in elem:
                    if c.tag.endswith("subClassOf"):
                        res = c.attrib.get(self.RDF_RESOURCE)
                        if res:
                            parent_iris.append(res)
                        else:
                            try:
                                subclass_expressions.append(ET.tostring(c, encoding="unicode"))
                            except Exception:
                                pass

                synonyms = []
                for c in elem:
                    tag_name = c.tag.split("}")[-1]
                    if "Synonym" in tag_name and c.text:
                        synonyms.append(c.text.strip())

                db_xrefs = []
                for c in elem:
                    if c.tag.endswith("hasDbXref") and c.text:
                        db_xrefs.append(c.text.strip())

                is_deprecated = any(
                    c.text == "true" for c in elem if c.tag.endswith("deprecated")
                )

                replacement_iris = []
                for c in elem:
                    if c.tag.endswith("IAO_0100001"):
                        repl = c.attrib.get(self.RDF_RESOURCE) or c.text
                        if repl:
                            replacement_iris.append(repl.strip())

                native_curie = about.split("/")[-1].replace("_", ":")

                payload = {
                    "about_iri": about,
                    "curie": native_curie,
                    "label": primary_name,
                    "all_labels": labels,
                    "definition": definition,
                    "parent_iris": parent_iris,
                    "subclass_expressions": subclass_expressions,
                    "synonyms": synonyms,
                    "database_cross_references": db_xrefs,
                    "is_deprecated": is_deprecated,
                    "replacement_iris": replacement_iris,
                }

                status = (
                    ExtractionStatus.REQUIRES_REVIEW
                    if (not primary_name or primary_name.startswith("http"))
                    else ExtractionStatus.EXTRACTED
                )

                source_record = SourceRecord(
                    source_id=self.SOURCE_ID,
                    dataset_id=self.DATASET_ID,
                    source_record_id=native_curie,
                    source_entity_type="OWL_CLASS",
                    original_identifier=about,
                    original_name=primary_name,
                    original_fields=payload,
                    raw_asset_id=raw_asset_id,
                    source_location=f"{path.name}#{about.split('/')[-1]}",
                    extraction_status=status,
                    metadata={"curie_prefix": native_curie.split(":")[0]},
                )

                current_chunk.append(source_record)
                record_count += 1
                elem.clear()

                if len(current_chunk) >= chunk_size:
                    yield current_chunk
                    current_chunk = []

                if max_records and record_count >= max_records:
                    break

            if current_chunk:
                yield current_chunk

        except ET.ParseError as pe:
            self.logger.error(f"XML parse error in {path}: {pe}")
            raise CorruptedAssetError(f"FoodOn OWL file corrupted or truncated: {pe}")
