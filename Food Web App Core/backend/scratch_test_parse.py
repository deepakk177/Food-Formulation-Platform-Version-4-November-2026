import sys
from pathlib import Path
sys.path.insert(0, r"Food Web App Core/backend")
sys.path.insert(0, r".")

from requirements_extractor import product_brief_parser

brief_text = "Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at least 8% almond content, at most 28% sugar, creamy melt, caramelized nut and vanilla flavor, 12-month shelf life, and free from dairy ingredients."
brief = product_brief_parser.parse(brief_text)

print(f"Product: {brief.product_name} ({brief.category})")
print(f"Total constraints: {len(brief.constraint_items)}")
for ci in brief.constraint_items:
    print(f"  {ci.constraint_id:<10} | {ci.type:<22} | {ci.parameter:<25} | {ci.operator:<10} | {str(ci.target_value):<15} | Unit: {str(ci.unit):<6} | {ci.hard_or_soft:<6} | Prio: {ci.priority}")

cg = brief.constraint_graph
print(f"\nConstraint Graph: {len(cg['nodes'])} nodes, {len(cg['edges'])} edges")
for n in cg['nodes']:
    print(f"  Node: {n['id']} ({n['type']}) -> {n['value']} [{n.get('hard_or_soft')}]")
