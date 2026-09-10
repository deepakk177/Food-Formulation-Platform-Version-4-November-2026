import re
from pathlib import Path

owl_path = Path('data/raw/ontology/foodon.owl')
if owl_path.exists():
    text = owl_path.read_text(encoding='utf-8', errors='ignore')
    classes = re.findall(r'<owl:Class rdf:about="(http://purl.obolibrary.org/obo/FOODON_[0-9]+)">', text)
    print(f'Total FOODON classes found: {len(classes)}')
    
    labels = re.findall(r'<rdfs:label[^>]*>(.*?)</rdfs:label>', text)
    print(f'Total rdfs:label entries found: {len(labels)}')
    print('Sample labels (first 20):', labels[:20])
else:
    print('foodon.owl does not exist')
