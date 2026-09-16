# Testing Patterns

**Analysis Date:** 2026-09-16

## Test Frameworks

**Backend & Data Pipelines:**
- Runner: `pytest` (v7.4+)
- Configuration: Standard pytest discovery, root markers in test directories
- Execution:
  ```bash
  # Run all backend unit and regression tests
  cd "Food Web App Core/backend"
  python -m pytest tests/ -v

  # Run specific regression suite
  python -m pytest tests/test_regressions.py -v

  # Run KG pipeline tests
  cd "kg_prep"
  python -m pytest tests/ -v
  ```

**Frontend:**
- Framework: Next.js standard linting & TypeScript verification
- Commands:
  ```bash
  cd "Food Web App Core/frontend"
  npm run lint
  ```

## Test Directory Organization

**Backend Tests (`Food Web App Core/backend/tests/`):**
- `test_formulation_engine.py`: Unit tests for percentage calculation, nutrition balance, and allergen filtering.
- `test_pipeline.py`: Pipeline execution flow, step sequencing, and error propagation.
- `test_regressions.py`: Regression tests ensuring previous bugfixes remain stable across pipeline versions.
- `test_end_to_end_pipeline.py`: Comprehensive test from product brief input to final formulation schema validation.
- `test_complete_formulation.py`: Verification that generated formulations meet 100% weight sum, valid nutritional bounds, and regulatory compliance.

**Knowledge Graph Tests (`kg_prep/tests/`):**
- `test_collectors.py`: Network scrapers, rate limiters, and payload parsing tests.
- `test_profiler_modular.py`: Data normalization, unit conversion, and deduplication verification.

## Testing Patterns & Best Practices

**Isolation & Mocking:**
- Unit tests use mock ingredient databases or lightweight local SQLite instances rather than requiring a live external Neo4j cluster.
- External API calls to Groq/LLMs are mocked during automated CI runs to ensure reproducible assertions and deterministic pass/fail states.

**Regression Testing:**
- When a hard-coded defect or calculation anomaly is resolved, a corresponding test case is added to `test_regressions.py` asserting that dynamic calculations produce valid results across multiple product categories (e.g. beverages, protein bars, plant-based dairy).

---

*Testing analysis: 2026-09-16*
