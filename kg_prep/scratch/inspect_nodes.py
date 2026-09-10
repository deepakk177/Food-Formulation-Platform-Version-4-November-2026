import json
import pandas as pd
from pathlib import Path

nodes_dir = Path(r"c:\Users\asus\.gemini\antigravity\scratch\FOOD FORMULATION PLATFORM\kg_prep\data\output\Nodes")
schema_map = {}

for f in sorted(nodes_dir.glob("*.csv")):
    df = pd.read_csv(f, nrows=5)
    node_type = f.stem
    cols = list(df.columns)
    pk = "ID" if "ID" in cols else (cols[0] if cols else "")
    name_field = "Name" if "Name" in cols else ("canonical_name" if "canonical_name" in cols else ("entity_name" if "entity_name" in cols else pk))
    src_field = "Source" if "Source" in cols else ("source_id" if "source_id" in cols else "")
    
    schema_map[node_type] = {
        "node_type": node_type,
        "csv_file": f.name,
        "primary_key": pk,
        "canonical_name_field": name_field,
        "source_id_field": src_field,
        "all_columns": cols,
        "sample_count": len(df)
    }

print(json.dumps(schema_map, indent=2))
with open(r"c:\Users\asus\.gemini\antigravity\scratch\FOOD FORMULATION PLATFORM\kg_prep\data\output\schema_map.json", "w") as out_f:
    json.dump(schema_map, out_f, indent=4)
