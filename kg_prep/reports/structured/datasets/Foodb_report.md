# Dataset Profiling Report: Foodb

*   **Domain**: Structured
*   **Total Files**: 1
*   **Total Size**: 0.53 KB
*   **Formats**: zip

## Files Inspected

### `foodb_2020_04_07_csv.zip`
*   **Path**: `data/raw/structured/foodb/foodb_2020_04_07_csv.zip`
*   **MIME Type**: `application/zip`
*   **Size**: 0.53 KB

#### Schema Details
*   **Schema Type**: ZIP containing CSV
*   **Columns**: id, name, chemical_formula, cas_number, molecular_weight, solubility, ph, functional_role, description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `id` $\rightarrow$ **Compound** (Confidence: 0.5)
*   Field `name` $\rightarrow$ **Ingredient** (Confidence: 1.0)
*   Field `chemical_formula` $\rightarrow$ **Compound** (Confidence: 0.8)
*   Field `cas_number` $\rightarrow$ **Compound** (Confidence: 0.8)

#### Candidate Relationships Mapping
*   **INGREDIENT_TO_COMPOUND**: `Ingredient` (name) $\rightarrow$ `Compound` (id, chemical_formula, cas_number), Confidence: 0.8

---