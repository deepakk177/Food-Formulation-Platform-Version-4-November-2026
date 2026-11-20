"""
Fix dairy attributes in SQLite database for all animal dairy ingredients.
"""
import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "Food Web App Core" / "backend" / "tcs_food_formulator_kg.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Find and update all dairy butter and milk products that were incorrectly marked vegan or dairy_free
plant_exceptions = [
    "cocoa butter", "almond butter", "peanut butter", "shea butter", "fruit butter",
    "apple butter", "prune butter", "peach butter", "orange butter", "lemon butter",
    "maple butter", "soy nut butter", "sesame butter", "vegetable butter", "butterhead",
    "butterbur", "buttercup", "butternut", "butterfly", "butterfish", "peanut butter sandwich"
]

rows = c.execute("SELECT id, name FROM ingredients").fetchall()
updated_count = 0
for row_id, name in rows:
    name_l = name.lower()
    if ("butter" in name_l or "ghee" in name_l or "dairy" in name_l or "whey" in name_l or "casein" in name_l or "cheese" in name_l) and not any(p in name_l for p in plant_exceptions):
        c.execute("UPDATE ingredients SET vegan = 0, dairy_free = 0, allergens = 'Milk' WHERE id = ?", (row_id,))
        updated_count += 1

conn.commit()
print(f"Successfully corrected {updated_count} dairy ingredients in SQLite.")
conn.close()

