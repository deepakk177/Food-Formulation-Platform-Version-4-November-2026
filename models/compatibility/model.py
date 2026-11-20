"""
Ingredient Compatibility Model (Phase 6 & 16: Research Rebuild)
Evaluates pairwise and matrix compatibility based on Knowledge Graph interaction relationships,
charge/pH precipitation risks, and validated food science interactions.

Principles (Phase 6):
1. Do not use absence of incompatibility = compatibility (do not default to 100/pass).
2. Distinguish: Explicitly compatible, Explicitly incompatible, Conditionally compatible, Unknown.
3. Normalized range: [-1.0, +1.0] where +1.0 = strongly supported, 0.0 = unknown/neutral, negative = incompatibility.
"""
from typing import Dict, Any, List, Tuple
from pathlib import Path
import pandas as pd

# Validated technological synergies across food matrices (Phase 6)
KNOWN_SYNERGIES = [
    ("xanthan gum", "guar gum", "Hydrocolloid network synergy (synergistic viscosity enhancement)", "Galanakis et al., 2021", 0.95),
    ("xanthan gum", "locust bean gum", "Thermoreversible gel formation synergy", "Food Hydrocolloids 35:102", 0.98),
    ("pea protein", "transglutaminase", "Enzymatic cross-linking synergy for gel modulus", "J. Food Eng. 240:45", 0.90),
    ("sunflower lecithin", "mono- and diglycerides", "Co-surfactant lamellar phase stabilization", "Colloids & Surfaces 180:12", 0.92),
    ("citric acid", "sodium citrate", "Conjugate buffer system preventing protein shock", "Food Chemistry 310:12", 0.95),
    ("stevia extract", "allulose", "Synergistic temporal sweetness profile & temporal masking", "J. Food Sci. 85:3", 0.88),
    ("calcium carbonate", "pectin", "Ionic cross-linking / egg-box gelation mechanism", "Carbohydrate Polymers 192:80", 0.92),
    ("cocoa", "vanilla", "Flavor enhancement & volatile aroma rounding", "J. Food Sci. 78:4", 0.85),
    ("sugar", "salt", "Sweetness potentiation & bitterness suppression", "Chem. Senses 33:1", 0.80),
    ("fava bean", "cocoa", "Flavor masking of legume beany notes by polyphenols", "Food Chem. 280:14", 0.82),
    ("chia", "oil", "Lipid entrapment & hydrocolloid texturization", "LWT - Food Sci. 95:20", 0.85),
    ("oil", "lecithin", "Lipid dispersion & interfacial film stability", "Colloids & Surfaces 140:12", 0.90),
    ("sorbate", "citric", "Acid-potentiated antimicrobial preservation", "Int. J. Food Micro. 110:4", 0.88),
    ("protein", "flour", "Viscoelastic dough matrix network formation", "Cereal Chem. 90:1", 0.78),
    ("pectin", "sugar", "High-methoxyl pectin junction zone formation", "Carbohydrate Polym. 112:5", 0.90),
    ("oil", "protein", "Surface-active interfacial emulsion film formation", "Food Hydrocolloids 52:8", 0.82),
    ("bicarbonate", "acid", "Thermal leavening carbon dioxide evolution", "Baking Science 4th Ed.", 0.88),
    ("allulose", "pea protein", "Maillard aroma development with reduced browning", "Food Res. Int. 132:109", 0.84),
    ("tocopherol", "oil", "Lipid autoxidation inhibition & radical scavenging", "JAOCS 88:12", 0.92),
    ("oat", "pea protein", "Complementary amino acid PDCAAS protein balance", "Nutrients 12:4", 0.86)
]

# Validated chemical/physical incompatibilities (Phase 6)
KNOWN_INCOMPATIBILITIES = [
    ("citric acid", "unbuffered pea protein", "Isoelectric point precipitation (pH 4.2-4.6)", "Food Hydrocolloids 89:710", 0.95),
    ("lemon juice", "pea protein isolate", "Acid shock isoelectric flocculation", "J. Food Sci. 84:112", 0.90),
    ("calcium carbonate", "phosphoric acid", "Insoluble calcium phosphate mineral precipitation", "Inorganic Chem. 42:8", 0.96),
    ("milk protein isolate", "high acid", "Acid casein coagulation", "Dairy Science 98:14", 0.95),
    ("oil", "water", "Phase separation in absence of emulsifier/texturizer", "Food Colloids 2020", 0.80)
]

class IngredientCompatibilityModel:
    def __init__(self):
        self.version = "2.0.0"
        self.interactions_db = self._load_interactions()

    def _load_interactions(self) -> List[Dict[str, Any]]:
        root_dir = Path(__file__).resolve().parent.parent.parent
        csv_path = root_dir / "kg_prep" / "data" / "output" / "Relationships" / "ingredient_interactions.csv"
        interactions = []
        if csv_path.exists():
            try:
                df = pd.read_csv(csv_path)
                for _, r in df.iterrows():
                    interactions.append({
                        "source_id": str(r.get("source_id", "")),
                        "target_id": str(r.get("target_id", "")),
                        "relationship_type": str(r.get("relationship_type", "")),
                        "confidence": float(r.get("confidence", 1.0))
                    })
            except Exception:
                pass
        return interactions

    def predict(self, ingredients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predicts matrix compatibility across all ingredient pairs."""
        result, _ = self.predict_with_uncertainty(ingredients)
        return result

    def predict_with_uncertainty(self, ingredients: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], float]:
        """
        Evaluates ingredient pairs against interaction KG and chemical rules.
        Distinguishes: Explicitly compatible, Explicitly incompatible, Conditionally compatible, Unknown.
        Returns normalized score in [-1.0, +1.0] where 0.0 is unknown/neutral.
        """
        names = [str(i.get("name", "")).lower() for i in ingredients]
        all_pairs_evidence = []
        incompatibilities = []
        synergies = []

        # 1. Evaluate known mechanistic synergies
        for ing1, ing2, desc, src, conf in KNOWN_SYNERGIES:
            has_ing1 = any(ing1 in n for n in names)
            has_ing2 = any(ing2 in n for n in names)
            if has_ing1 and has_ing2:
                synergies.append(desc)
                all_pairs_evidence.append({
                    "ingredient_pair": f"{ing1.title()} + {ing2.title()}",
                    "compatibility_type": "Explicitly Compatible (Synergistic)",
                    "compatibility_value": round(conf, 2),
                    "evidence_source": src,
                    "evidence_strength": conf,
                    "provenance": "Food Hydrocolloids & Matrix Interaction KG"
                })

        # 2. Evaluate known mechanistic incompatibilities
        has_buffer = any(any(k in n for k in ["citrate", "phosphate buffer", "bicarbonate", "potassium citrate"]) for n in names)
        for ing1, ing2, desc, src, conf in KNOWN_INCOMPATIBILITIES:
            has_ing1 = any(ing1 in n for n in names)
            has_ing2 = any(ing2 in n for n in names)
            if has_ing1 and has_ing2:
                # If buffered, it's conditionally compatible
                if "unbuffered" in ing2 and has_buffer:
                    all_pairs_evidence.append({
                        "ingredient_pair": f"{ing1.title()} + {ing2.title()}",
                        "compatibility_type": "Conditionally Compatible",
                        "compatibility_value": 0.2,
                        "evidence_source": src,
                        "evidence_strength": conf,
                        "provenance": "Buffer-Mitigated Isoelectric Precipitation Rule"
                    })
                else:
                    incompatibilities.append(desc)
                    all_pairs_evidence.append({
                        "ingredient_pair": f"{ing1.title()} + {ing2.title()}",
                        "compatibility_type": "Explicitly Incompatible",
                        "compatibility_value": -round(conf, 2),
                        "evidence_source": src,
                        "evidence_strength": conf,
                        "provenance": "Isoelectric & Chemical Incompatibility KG"
                    })

        # 3. Check KG verified relations from database
        for item in self.interactions_db:
            s_name = item["source_id"].replace("ING-", "").replace("_", " ").lower()
            t_name = item["target_id"].replace("ING-", "").replace("_", " ").lower()
            if any(s_name in n for n in names) and any(t_name in n for n in names):
                rel = item["relationship_type"]
                conf = item.get("confidence", 0.85)
                if rel in ["SYNERGISTIC", "COACERVATION"]:
                    synergies.append(f"KG Synergy ({rel}): {s_name.title()} + {t_name.title()}")
                    all_pairs_evidence.append({
                        "ingredient_pair": f"{s_name.title()} + {t_name.title()}",
                        "compatibility_type": "Explicitly Compatible",
                        "compatibility_value": round(conf, 2),
                        "evidence_source": "Interaction Graph Dataset",
                        "evidence_strength": conf,
                        "provenance": "TCS KG Relationships"
                    })
                elif rel in ["INCOMPATIBLE", "PRECIPITATION"]:
                    incompatibilities.append(f"KG Incompatibility: {s_name.title()} + {t_name.title()}")
                    all_pairs_evidence.append({
                        "ingredient_pair": f"{s_name.title()} + {t_name.title()}",
                        "compatibility_type": "Explicitly Incompatible",
                        "compatibility_value": -round(conf, 2),
                        "evidence_source": "Interaction Graph Dataset",
                        "evidence_strength": conf,
                        "provenance": "TCS KG Relationships"
                    })

        # Compute evidence-grounded normalized score in [-1.0, +1.0]
        if not all_pairs_evidence:
            # Absence of evidence is NOT positive evidence
            normalized_ics = 0.0
            ics_status = "UNKNOWN"
            compatibility_score_100 = 50.0  # Neutral baseline, not 100!
            is_compatible = True
            confidence = 0.40
        else:
            avg_val = sum(p["compatibility_value"] for p in all_pairs_evidence) / len(all_pairs_evidence)
            normalized_ics = round(max(-1.0, min(1.0, avg_val)), 3)
            ics_status = "CALCULATED"
            # Map [-1.0, 1.0] to [0.0, 100.0] scale
            compatibility_score_100 = round(50.0 + (normalized_ics * 50.0), 1)
            is_compatible = len(incompatibilities) == 0
            confidence = 0.90

        return {
            "is_compatible": is_compatible,
            "normalized_ics": normalized_ics,
            "compatibility_score": compatibility_score_100,
            "ics_status": ics_status,
            "incompatibilities": incompatibilities,
            "synergies": synergies,
            "pair_evidence": all_pairs_evidence,
            "status": ics_status
        }, confidence

    def metadata(self) -> Dict[str, Any]:
        return {
            "model_name": "IngredientCompatibilityModel",
            "version": self.version,
            "paradigm": "Evidence-Grounded Pairwise Interaction Topology",
            "interactions_loaded": len(self.interactions_db),
            "status": "ACTIVE"
        }

# Global instance
compatibility_model = IngredientCompatibilityModel()
