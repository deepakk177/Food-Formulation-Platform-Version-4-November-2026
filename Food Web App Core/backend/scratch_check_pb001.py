import pandas as pd

df = pd.read_csv("outputs/formulation_benchmark/06_dynamic_subgraph_ingredients.csv")
pb1 = df[df["product_brief_id"] == "PB001"]
print(f"Total PB001 rows: {len(pb1)}")
for _, r in pb1.iterrows():
    print(f"  {r['ingredient_id']}: {r['ingredient_name']} ({r['category']}) - {r['functional_roles']}")
