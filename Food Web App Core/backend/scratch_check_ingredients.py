import sqlite3
from pathlib import Path

db_path = Path("Food Web App Core/backend/tcs_food_formulator_kg.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT id, name, category, functional_role, protein, fat, cost_per_kg FROM ingredients WHERE name LIKE '%cocoa butter%' OR name LIKE '%almond%'")
rows = c.fetchall()
print(f"Total matching cocoa butter / almond: {len(rows)}")
for r in rows:
    if r[4] > 0 or r[5] > 0 or (r[6] is not None and r[6] > 0):
        print(r)
conn.close()
