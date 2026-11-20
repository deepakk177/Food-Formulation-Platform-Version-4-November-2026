import sqlite3

conn = sqlite3.connect("Food Web App Core/backend/tcs_food_formulator_kg.db")
c = conn.cursor()
c.execute("SELECT DISTINCT source FROM ingredients")
print("Sources:", c.fetchall())

c.execute("SELECT id, name, category, functional_role, protein, fat, carbs, cost_per_kg, vegan, dairy_free, allergens FROM ingredients WHERE source = 'Grounded Repository DB'")
grounded_rows = c.fetchall()
print(f"Total Grounded Repository DB ingredients: {len(grounded_rows)}")
for r in grounded_rows:
    print(r)
