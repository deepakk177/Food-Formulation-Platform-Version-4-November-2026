import sqlite3

conn = sqlite3.connect("Food Web App Core/backend/tcs_food_formulator_kg.db")
c = conn.cursor()
c.execute("SELECT * FROM ingredients WHERE id = 'ing_almond_flour'")
row = c.fetchone()
col_names = [d[0] for d in c.description]
for col, val in zip(col_names, row):
    print(f"  {col}: {val}")
conn.close()
