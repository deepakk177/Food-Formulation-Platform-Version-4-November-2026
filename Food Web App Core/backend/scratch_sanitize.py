with open("Food Web App Core/backend/exhaustive_search_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

replacements = {
    "\u03a0": "PRODUCT",
    "\u2192": "->",
    "\u00d7": "x",
    "\u00b1": "+/-",
    "\u2265": ">=",
    "\u2264": "<=",
    "\u201c": '"',
    "\u201d": '"',
    "\u2018": "'",
    "\u2019": "'",
    "\u2013": "-",
    "\u2014": "--"
}

for k, v in replacements.items():
    text = text.replace(k, v)

with open("Food Web App Core/backend/exhaustive_search_engine.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Sanitization complete. Any remaining non-ascii:")
for i, line in enumerate(text.splitlines(), 1):
    for ch in line:
        if ord(ch) > 127:
            print(f"Line {i}: ord={ord(ch)}")
