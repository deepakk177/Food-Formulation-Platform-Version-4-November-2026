import sys
import traceback
from database import SessionLocal
from main import formulate_api

try:
    db = SessionLocal()
    res = formulate_api({"query": "Formulate a low-sodium, high-protein snack"}, db=db)
    print("SUCCESS PAYLOAD RECIPE NAME:", res["formulation"]["recipe_name"])
except Exception as e:
    print("EXCEPTIONAL ERROR DETECTED:")
    traceback.print_exc()
