import re
import xml.etree.ElementTree as ET
from pathlib import Path

owl_path = Path('data/raw/ontology/foodon.owl')
text = owl_path.read_text(encoding='utf-8', errors='ignore')

# Match owl:Class blocks with FOODON ID
pattern = re.compile(r'<owl:Class\s+rdf:about="(http://purl\.obolibrary\.org/obo/FOODON_\d+)">(.*?)</owl:Class>', re.DOTALL)
matches = pattern.findall(text)

print(f"Total FOODON food/ingredient classes: {len(matches)}")

extracted = []
for uri, block in matches:
    label_match = re.search(r'<rdfs:label[^>]*>(.*?)</rdfs:label>', block)
    syn_matches = re.findall(r'<oboInOwl:hasExactSynonym[^>]*>(.*?)</oboInOwl:hasExactSynonym>', block)
    if label_match:
        label = label_match.group(1).strip()
        foodon_id = uri.split("/")[-1]
        extracted.append({
            "foodon_id": foodon_id,
            "uri": uri,
            "label": label,
            "synonyms": "|".join(syn_matches)
        })

print(f"Successfully extracted {len(extracted)} labeled FoodOn entities.")
print("Sample extracted entities (10):")
for item in extracted[:10]:
    print(item)
