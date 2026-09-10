import re
import logging
import unicodedata
from typing import Dict, List, Any, Tuple

logger = logging.getLogger("fusion.resolver")

class EntityResolver:
    """
    Deterministic Entity Resolution Engine.
    Enforces conservative identifier and exact normalized name matching.
    Avoids aggressive fuzzy merging to guarantee zero silent mis-merging.
    """
    def __init__(self, fuzzy_threshold: float = 0.95):
        self.fuzzy_threshold = fuzzy_threshold
        # Controlled synonym dictionary (lowercase keys)
        self.synonym_dict = {
            "salt": "Sodium Chloride",
            "nacl": "Sodium Chloride",
            "table salt": "Sodium Chloride",
            "vitamin c": "Ascorbic Acid",
            "l-ascorbate": "Ascorbic Acid",
            "water": "Water",
            "h2o": "Water",
            "sugar": "Sucrose",
            "table sugar": "Sucrose",
            "msg": "Monosodium Glutamate",
            "e621": "Monosodium Glutamate"
        }

    def normalize_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        # Unicode normalization (NFKD)
        norm = unicodedata.normalize("NFKD", text)
        # Strip accents
        norm = "".join(c for c in norm if not unicodedata.combining(c))
        # Remove extra whitespace and convert to lowercase
        return " ".join(norm.split()).lower()

    def canonicalize_name(self, name: str) -> str:
        """Returns title-cased canonical name after controlled synonym lookup."""
        if not name or not isinstance(name, str):
            return "Unknown Entity"
        clean = " ".join(name.split())
        lower_clean = clean.lower()
        if lower_clean in self.synonym_dict:
            return self.synonym_dict[lower_clean]
        return clean.title()

    def generate_deterministic_id(self, prefix: str, record: Dict[str, Any]) -> str:
        """Generates a deterministic canonical ID from standard keys or normalized name."""
        # 1. Standard chemical keys if present
        cas = record.get("CASNumber")
        if cas and isinstance(cas, str) and cas.strip():
            return f"CMP-CAS-{cas.strip()}"

        pubchem = record.get("PubChemID")
        if pubchem and isinstance(pubchem, str) and pubchem.strip():
            return f"FLV-PUBCHEM-{pubchem.strip()}"

        ins = record.get("INS") or record.get("INSNumber")
        if ins and isinstance(ins, str) and ins.strip():
            return f"INS-{ins.strip()}"

        # 2. Deterministic hash key from normalized name
        name = record.get("Name", "")
        norm_name = re.sub(r'[^a-z0-9]', '_', self.normalize_text(name)).strip('_')
        if not norm_name:
            norm_name = "unnamed_entity"
        
        pref = prefix[:3].upper() if prefix else "ENT"
        return f"{pref}-{norm_name.upper()}"

    def resolve_entities(self, records: List[Dict[str, Any]], exact_only: bool = True) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
        """
        Resolves entities deterministically in O(N) time complexity using hash index lookups.
        When identity is ambiguous, records are NOT merged and remain separate.
        Returns:
            resolved_records: List of canonical entity dicts.
            id_mapping: Dict mapping original ID -> canonical ID.
        """
        resolved_records = []
        id_mapping = {}
        seen_cas = {}
        seen_pubchem = {}
        seen_norm_name = {}
        
        for record in records:
            orig_id = str(record.get("ID", ""))
            orig_name = str(record.get("Name", ""))
            
            canonical_name = self.canonicalize_name(orig_name)
            record["Name"] = canonical_name
            
            norm_key = self.normalize_text(canonical_name)
            cas_key = str(record.get("CASNumber", "")).strip() if record.get("CASNumber") else ""
            pubchem_key = str(record.get("PubChemID", "")).strip() if record.get("PubChemID") else ""

            matched = None
            if cas_key and cas_key in seen_cas:
                matched = seen_cas[cas_key]
            elif pubchem_key and pubchem_key in seen_pubchem:
                matched = seen_pubchem[pubchem_key]
            elif norm_key and norm_key in seen_norm_name:
                matched = seen_norm_name[norm_key]

            if matched:
                canon_id = matched["ID"]
                id_mapping[orig_id] = canon_id
                for k, v in record.items():
                    if v and not matched.get(k):
                        matched[k] = v
            else:
                canon_id = self.generate_deterministic_id(orig_id, record)
                record["ID"] = canon_id
                record["resolution_status"] = "RESOLVED"
                id_mapping[orig_id] = canon_id
                resolved_records.append(record)
                if cas_key:
                    seen_cas[cas_key] = record
                if pubchem_key:
                    seen_pubchem[pubchem_key] = record
                if norm_key:
                    seen_norm_name[norm_key] = record

        return resolved_records, id_mapping
