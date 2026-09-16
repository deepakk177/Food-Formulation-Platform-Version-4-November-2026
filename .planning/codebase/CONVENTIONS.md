# Coding Conventions

**Analysis Date:** 2026-09-16

## Naming Patterns

**Python Backend:**
- Files: `snake_case.py` (e.g., `pipeline_runner.py`, `candidate_engine.py`)
- Classes: `PascalCase` (e.g., `PipelineRunner`, `CandidateEngine`, `FormulationResponse`)
- Functions & Methods: `snake_case()` (e.g., `run_pipeline()`, `evaluate_constraints()`)
- Variables: `snake_case` (e.g., `candidate_ingredients`, `hard_constraints`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_BATCH_SIZE`, `JURISDICTIONS`)

**TypeScript Frontend:**
- Files: `PascalCase.tsx` for components (e.g., `FormulationResults.tsx`), `camelCase.ts` for stores/utilities (e.g., `useFormulationStore.ts`)
- Components: `PascalCase` (e.g., `ConstraintGraphView`, `FormulationCard`)
- Functions & Hooks: `camelCase` (e.g., `fetchFormulation()`, `useFormulationStore`)
- Interfaces & Types: `PascalCase` (e.g., `FormulationResult`, `IngredientItem`)

## Code Style & Formatting

**Python:**
- PEP 8 compliant indentation (4 spaces)
- Explicit type hinting using standard library `typing` and Pydantic models (`Food Web App Core/backend/schemas.py`)
- Docstrings on core service methods describing parameters, return types, and potential side-effects.

**TypeScript / React:**
- Strict typing with TypeScript 5.2 (`tsconfig.json`)
- React 18 functional components with typed props (`React.FC<Props>` or `(props: Props)`)
- Tailwind CSS utility classes organized logically (layout -> sizing -> typography -> colors -> states)

## Import Organization

**Python Backend:**
1. Standard library imports (e.g., `import os`, `import sys`, `from typing import Dict, List, Optional`)
2. Third-party packages (e.g., `from fastapi import FastAPI, HTTPException`, `import pandas as pd`, `from pydantic import BaseModel`)
3. Local application modules (e.g., `from schemas import FormulationRequest`, `from repository import IngredientRepository`)

**Frontend TypeScript:**
1. React and Next.js built-ins (`import React, { useState } from 'react'`, `import Link from 'next/link'`)
2. External UI / visualization libraries (`import { ResponsiveContainer } from 'recharts'`, `import { Shield, Sparkles } from 'lucide-react'`)
3. Internal stores, components, and types (`import { useFormulationStore } from '@/store/useFormulationStore'`)

## Error Handling & Logging

**Backend Error Strategy:**
- Critical operations are wrapped in `try/except` blocks with meaningful logging to avoid crashing the whole pipeline.
- If a secondary service (e.g. LLM synthesis or Neo4j) fails, the pipeline degrades gracefully by providing deterministic fallbacks and setting status flags in the output report.
- API endpoints catch domain exceptions and convert them to standard FastAPI `HTTPException` responses with actionable details.

**Frontend Error Strategy:**
- State stores track `loading`, `error`, and `success` states explicitly (`useFormulationStore.ts`).
- UI shows inline notification banners and actionable guidance when requests fail.

---

*Convention analysis: 2026-09-16*
