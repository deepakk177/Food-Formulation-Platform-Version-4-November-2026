import sqlite3
from pathlib import Path

db_path = Path("tcs_food_formulator_kg.db")
print("DB exists:", db_path.exists())
if db_path.exists():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name, protein, fat, carbs, energy FROM ingredients LIMIT 5")
    for r in c.fetchall():
        print(r)
    print("--- Searching Fava, Sugar, Pea ---")
    c.execute("SELECT name, protein, fat, carbs, energy FROM ingredients WHERE name LIKE '%Fava%' OR name LIKE '%Sugar%' OR name LIKE '%Pea%'")
    for r in c.fetchall():
        print(r)
