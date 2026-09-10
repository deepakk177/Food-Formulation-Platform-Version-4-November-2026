# Dataset Profiling Report: Usda_fdc

*   **Domain**: Structured
*   **Total Files**: 1
*   **Total Size**: 0.25 KB
*   **Formats**: zip

## Files Inspected

### `FoodData_Central_csv_2024-04-18.zip`
*   **Path**: `data/raw/structured/usda_fdc/FoodData_Central_csv_2024-04-18.zip`
*   **MIME Type**: `application/zip`
*   **Size**: 0.25 KB

#### Schema Details
*   **Schema Type**: ZIP containing CSV
*   **Columns**: fdc_id, data_type, description, food_category_id, publication_date

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `food_category_id` $\rightarrow$ **Ingredient** (Confidence: 0.8)

#### Candidate Relationships Mapping
*   No relationships detected.

---