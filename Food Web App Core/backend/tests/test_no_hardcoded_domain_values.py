"""
Automated Hard-Code Regression Test Suite
Scans the backend and frontend codebases to ensure no forbidden hardcoded domain values exist:
- Hardcoded shelf life numbers (e.g., shelf_life = 9, shelf_life = 12)
- Hardcoded compatibility scores (e.g., compatibility_score = 95, 90)
- Hardcoded regulatory scores (e.g., regulatory_score = 98)
- Hardcoded completeness scores (e.g., completeness_score = 90.0)
- Hardcoded fallback ingredient lists (e.g., fallbackComponents)
- Hardcoded cost constants (e.g., cost_per_kg = 8.74, 10.0)
- Hardcoded process parameters (e.g., 3000 RPM, 85°C for 2 min)
"""

import os
import re
import pytest

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.abspath(os.path.join(BACKEND_DIR, "..", "frontend", "src"))

FORBIDDEN_BACKEND_PATTERNS = [
    (r"\bshelf_life\s*=\s*\d+\b", "Hardcoded shelf life integer assigned directly without dynamic/model computation"),
    (r"\bcompatibility_score\s*=\s*(?:90|95|98|100)\b", "Hardcoded compatibility score"),
    (r"\bregulatory_score\s*=\s*(?:90|95|98|100)\b", "Hardcoded regulatory score"),
    (r"\bcompleteness_score\s*=\s*90(?:\.0)?\b", "Hardcoded completeness score 90.0"),
    (r"\bcost_per_kg\s*=\s*(?:8\.74|10(?:\.0)?)\b", "Hardcoded cost per kg constant"),
    (r"3000\s*RPM", "Hardcoded 3000 RPM processing parameter"),
    (r"85°C\s*for\s*2\s*min", "Hardcoded 85°C process template"),
]

FORBIDDEN_FRONTEND_PATTERNS = [
    (r"fallbackComponents", "Hardcoded 14-ingredient fallback components array"),
    (r"35\.5g\s*Protein", "Hardcoded 35.5g protein fallback"),
    (r"\$8\.74", "Hardcoded $8.74 cost constant"),
    (r"defaultActivities\s*:\s*ActivityItem\[\]", "Fabricated mock default activities array"),
    (r"Gluten-Free\s*Sandwich\s*Bread", "Fabricated mock compliance audit records"),
]

def test_no_hardcoded_values_in_backend():
    """Verify backend Python files do not contain forbidden hardcoded constants."""
    exclude_dirs = {"__pycache__", ".pytest_cache", "tests", "venv", ".git"}
    violations = []

    for root, dirs, files in os.walk(BACKEND_DIR):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, BACKEND_DIR)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                for pattern, description in FORBIDDEN_BACKEND_PATTERNS:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_no = content[:match.start()].count("\n") + 1
                        violations.append(f"{rel_path}:{line_no} -> {description} (match: '{match.group()}')")

    assert not violations, "Found forbidden hardcoded values in backend:\n" + "\n".join(violations)

def test_no_hardcoded_values_in_frontend():
    """Verify frontend TypeScript/React files do not contain forbidden mock fallbacks."""
    violations = []
    if not os.path.exists(FRONTEND_DIR):
        pytest.skip(f"Frontend directory not found at {FRONTEND_DIR}")

    for root, dirs, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith((".tsx", ".ts")):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, FRONTEND_DIR)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                for pattern, description in FORBIDDEN_FRONTEND_PATTERNS:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_no = content[:match.start()].count("\n") + 1
                        violations.append(f"{rel_path}:{line_no} -> {description} (match: '{match.group()}')")

    assert not violations, "Found forbidden hardcoded values in frontend:\n" + "\n".join(violations)

if __name__ == "__main__":
    print("Running hard-coded regression tests...")
    test_no_hardcoded_values_in_backend()
    print("✓ Backend scanned: 0 hardcoded violations found.")
    test_no_hardcoded_values_in_frontend()
    print("✓ Frontend scanned: 0 hardcoded violations found.")
    print("ALL HARD-CODE REGRESSION CHECKS PASSED SUCCESSFULLY!")
