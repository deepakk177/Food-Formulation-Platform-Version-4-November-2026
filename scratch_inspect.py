import sqlite3
import json

conn = sqlite3.connect('Food Web App Core/backend/tcs_food_formulator_kg.db')
c = conn.cursor()

print("--- Cocoa Butter in ingredients table ---")
rows = c.execute("SELECT id, name, category, functional_role, vegan, dairy_free, gluten_free, allergens, cost_per_kg FROM ingredients WHERE name LIKE '%cocoa butter%'").fetchall()
for r in rows:
    print(r)

print("\n--- Total ingredients in ingredients table ---")
print(c.execute("SELECT COUNT(*) FROM ingredients").fetchone()[0])

print("\n--- Categories ---")
cats = c.execute("SELECT category, COUNT(*) FROM ingredients GROUP BY category ORDER BY COUNT(*) DESC LIMIT 15").fetchall()
for cat in cats:
    print(cat)
