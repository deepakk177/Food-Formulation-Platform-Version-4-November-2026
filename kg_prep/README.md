# Food Formulation Knowledge Graph — Data Acquisition Module

This module automates the collection and organization of raw datasets required to build the Food Formulation Knowledge Graph. It structures data into Structured, Semi-Structured, and Unstructured categories, adhering strictly to a raw-only acquisition model (no cleaning or extraction).

## Multi-Source Constraint Extraction Pipeline

The Food Formulation Knowledge Graph pipeline includes a dedicated, source-grounded constraint extraction engine designed for regulatory compliance, ingredient selection, formulation optimization, and explainable reasoning.

### Authority Hierarchy & Sources

| Authority Level | Source Category | Configured Sources | Output Constraint Types |
| :--- | :--- | :--- | :--- |
| **LEVEL 5** | Regulatory Authorities | Codex Alimentarius GSFA (CXS 192-1995), FSSAI Regulations (India), US FDA 21 CFR | `LEGAL_LIMIT`, `REGULATORY_REQUIREMENT`, `ADDITIVE_LIMIT`, `ADDITIVE_PERMISSION`, `ALLERGEN_REQUIREMENT` |
| **LEVEL 4** | Official Composition Standards | USDA FoodData Central, ICMR-NIN IFCT 2017, FoodOn Ontology | `COMPOSITION_REQUIREMENT`, `FOOD_STANDARD` |
| **LEVEL 3** | Peer-Reviewed Literature | PubMed, PMC, arXiv Open Access Research Papers | `TECHNOLOGICAL_LIMIT`, `PHYSICOCHEMICAL_LIMIT`, `STABILITY_LIMIT`, `LITERATURE_RECOMMENDATION` |
| **LEVEL 2** | Patents & Commercial | Google Patents, EPO Patents, Cargill/ADM/Tate&Lyle/Ingredion/IFF Technical Spec Sheets | `PATENT_FORMULATION_RANGE`, `SUPPLIER_RECOMMENDATION` |

---

### Constraint Node Schema (`Nodes/Constraints.csv`)

Every constraint extracted by the pipeline adheres to the canonical schema:

- `constraint_id`: Unique identifier (e.g. `CONST-GSFA-950-14_0`, `CONST-FSSAI-211-BEV`)
- `entity_id`: Target FoodAdditive or Ingredient ID (`ADD-INS-950`, `ING-FDC_173488`)
- `entity_name`: Canonical name of the target entity
- `constraint_type`: Categorical taxonomy (`LEGAL_LIMIT`, `ADDITIVE_LIMIT`, `COMPOSITION_REQUIREMENT`, etc.)
- `parameter`: Atomic parameter being constrained (`maximum_use_level`, `maximum_moisture`, `ph_range`, etc.)
- `operator`: Standardized operator (`=`, `>`, `<`, `>=`, `<=`, `RANGE`, `PRESENT`, `ABSENT`, `QUANTUM_SATIS`)
- `limit_value`: Raw textual limit value
- `limit_value_min`: Minimum numerical bound
- `limit_value_max`: Maximum numerical bound
- `normalized_value` / `normalized_unit`: Standardized unit representation
- `jurisdiction`: Regulatory jurisdiction (`India`, `Codex`, `US`, `Global`, `Commercial`)
- `regulation_id`: CITED regulatory or document reference ID
- `section` / `table`: Section, table, or page reference in source document
- `source_id`: Authority source ID (`SRC-CODEX`, `SRC-FSSAI`, `SRC-FDA`, `SRC-SCIENTIFIC-LITERATURE`)
- `evidence_id`: Primary evidence key linking to `Evidence.csv`
- `evidence_text`: Verbatim text span supporting the constraint claim
- `status`: Temporal versioning (`CURRENT`, `HISTORICAL`, `SUPERSEDED`)
- `validation_status`: Provenance audit status (`SOURCE_VERIFIED`, `CROSS_SOURCE_VERIFIED`, `VALIDATED`)

---

### Canonical Relationship Files

1. [`ingredient_has_constraint.csv`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/data/output/Relationships/ingredient_has_constraint.csv): Links canonical Ingredients to applicable constraints.
2. [`regulation_has_constraint.csv`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/data/output/Relationships/regulation_has_constraint.csv): Links official Regulations to extracted constraints.
3. [`foodadditive_allowed_in_foodcategory.csv`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/data/output/Relationships/foodadditive_allowed_in_foodcategory.csv): Maps Food Additives to permitted Food Categories.
4. [`product_has_constraint.csv`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/data/output/Relationships/product_has_constraint.csv): Links finished Food Products to formulation constraints.

---

### Audit Ledgers & Verification Outputs

- [`data/reports/constraint_lineage.csv`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/data/reports/constraint_lineage.csv): Complete field-by-field lineage for every constraint.
- [`data/reports/constraint_source_matrix.csv`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/data/reports/constraint_source_matrix.csv): Coverage matrix across sources, jurisdictions, and document types.
- [`data/reports/constraint_statistics.csv`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/data/reports/constraint_statistics.csv): Statistical summary by constraint type and confidence.
- [`data/reports/rejected_constraints.csv`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/data/reports/rejected_constraints.csv): Audit trail of any unverified or synthetic constraints rejected during validation.

---

### How to Run Pipeline & Reproducibility Tests

Run the full end-to-end extraction and validation pipeline:
```bash
python main.py --pipeline
```

Run the deterministic reproducibility test (asserts 100% SHA-256 hash match across runs):
```bash
python main.py --reproducibility-test
```

## Project Directory Structure

Once executed, raw datasets are saved into the following directory tree:
```
FoodKG/
│
├── data/
│   ├── raw/                       # Temporary downloads or shared buffers
│   │
│   ├── structured/
│   │   ├── foodb/                 # FooDB CSV/SQL archives
│   │   ├── usda_fdc/              # USDA FoodData Central CSV/JSON zips
│   │   ├── recipe1m/              # Recipe1M+ recipes JSON
│   │   ├── nutrition5k/           # Nutrition5K metadata & images
│   │   └── gsfa_xml/              # Codex GSFA XML standard
│   │
│   ├── semi_structured/
│   │   ├── flavordb/              # FlavorDB HTML and JSON profiles
│   │   ├── gsfa_html/             # Scraped Codex GSFA online HTML indexes
│   │   ├── product_labels/        # Open Food Facts Product Label HTML pages
│   │   └── specification_sheets/  # Ingredient manufacturer spec sheets
│   │
│   └── unstructured/
│       ├── ins/                   # Codex INS Numbering system PDF
│       ├── codex/                 # Codex General Standard for Food Additives PDF
│       ├── fssai/                 # FSSAI Regulations PDF
│       ├── research_papers/       # Open Access research papers (PDF)
│       └── patents/               # Google Patents (PDF)
│
├── config/
│   └── config.yaml                # Orchestration settings & source metadata
│
├── src/                           # Library code
│   ├── utils/
│   │   ├── checksum.py            # SHA256 integrity verification
│   │   └── http_client.py         # Asynchronous resilient HTTP client
│   ├── collectors/                # 14 data source collectors
│   ├── metadata_manager.py        # Centralized metadata.json database
│   └── orchestrator.py            # Core pipeline coordinator
│
└── main.py                        # Pipeline CLI entry point
```

## Datasets Overview & Requirements

| # | Dataset | Domain | Official Source | File Format | Mode | License | Reason for Inclusion |
|---|---------|--------|-----------------|-------------|------|---------|----------------------|
| 1 | FooDB | Structured | [fooDB.ca](https://foodb.ca/) | ZIP (CSV/SQL) | Automatic | Non-commercial Research | Essential ingredient chemical composition database. |
| 2 | USDA FDC | Structured | [fdc.nal.usda.gov](https://fdc.nal.usda.gov/) | ZIP (CSV/JSON) | Automatic | Public Domain | Comprehensive nutritional profiles for base foods. |
| 3 | Recipe1M+ | Structured | [im2recipe.csail.mit.edu](http://im2recipe.csail.mit.edu/) | JSON | **Manual** | Academic Use | Large scale recipe co-occurrences. |
| 4 | Nutrition5K | Structured | [GitHub Repo](https://github.com/google-research-datasets/Nutrition5k) | JSON/CSV | **Manual** | Academic Use | Mass, calorie, and nutrient values. |
| 5 | GSFA XML | Structured | [fao.org/gsfaonline](https://www.fao.org/gsfaonline/) | XML | **Manual** | Public Domain | Structured regulatory standards for food additives. |
| 6 | FlavorDB | Semi-structured | [cosylab.iiitd.edu.in](https://cosylab.iiitd.edu.in/flavordb2/) | HTML/JSON | Automatic | Academic Use Only | Flavor compounds and sensory descriptors. |
| 7 | GSFA Online | Semi-structured | [fao.org/gsfaonline](https://www.fao.org/gsfaonline/) | HTML | Automatic | Public Domain | Scraped food categories, additives, and INS mappings. |
| 8 | Spec Sheets | Semi-structured | Various | HTML/PDF | Automatic | Proprietary | Real-world ingredient technical specifications. |
| 9 | Product Labels | Semi-structured | [Open Food Facts](https://world.openfoodfacts.org/) | HTML | Automatic | ODbL | Retail product ingredient listings and barcodes. |
| 10 | INS System | Unstructured | [fao.org/fao-who-codexalimentarius](https://www.fao.org/fao-who-codexalimentarius/) | PDF | Automatic | Public Domain | Standard International Numbering System (CXG 36-1989). |
| 11 | Codex Standards | Unstructured | [fao.org/fao-who-codexalimentarius](https://www.fao.org/fao-who-codexalimentarius/) | PDF | Automatic | Public Domain | Codex General Standard for Food Additives (CXS 192-1995). |
| 12 | FSSAI | Unstructured | [fssai.gov.in](https://fssai.gov.in/) | PDF | Automatic | Public Domain | Indian national regulations for food additives. |
| 13 | Research Papers | Unstructured | PMC, arXiv | PDF | Automatic | Open Access | Research on synergistic formulation interactions. |
| 14 | Patents | Unstructured | Google Patents | PDF | Automatic | Public Domain | Patented industrial food formulation methods. |

---

## Instructions for Manually Downloading Restricted Datasets

Due to licensing, size, or registration barriers, the following datasets are not automatically downloaded. Follow these instructions to manually acquire them:

### 1. Recipe1M+
1. Navigate to the official website: http://im2recipe.csail.mit.edu/
2. Click **Request Dataset** and fill out the registration form.
3. Accept the Academic Research Use License.
4. Once your request is approved (typically via email), download the core files:
   - `layer1.json`
   - `layer2.json`
5. Create the directory `data/structured/recipe1m/` if it does not exist.
6. Copy both files into `data/structured/recipe1m/`.

### 2. Nutrition5K
1. Navigate to the Google Research dataset GitHub: https://github.com/google-research-datasets/Nutrition5k
2. Follow the directions to download the café dataset files from the public Google Cloud Storage bucket.
3. Obtain the metadata CSVs:
   - `dish_metadata_cafe1.csv`
   - `dish_metadata_cafe2.csv`
4. Place these CSVs under `data/structured/nutrition5k/`.

### 3. GSFA XML
1. Codex Alimentarius GSFA Online does not provide a public bulk XML download endpoint.
2. If you are an authorized partner or have custom XML files containing Codex food category standards, name the file `gsfa_standards.xml`.
3. Copy the file into `data/structured/gsfa_xml/`.

---

## Running the Data Acquisition Module

### Installation
Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

### CLI Commands

* **Acquire All Active Datasets (Runs automatic and marks manual):**
  ```bash
  python main.py --all
  ```

* **Acquire a Single Dataset (e.g. foodb):**
  ```bash
  python main.py --source foodb
  ```

* **Acquire all Datasets under a specific Domain (e.g. unstructured):**
  ```bash
  python main.py --domain unstructured
  ```

* **Use a custom configuration directory:**
  ```bash
  python main.py --all --config-dir custom_config/
  ```

## Output Logging & Cataloging

* **`data/metadata.json`**: Central JSON database containing dataset names, official source links, local download paths, raw file types, access modes, licenses, download timestamps, and current status.
* **`data/download_log.csv`**: A CSV logging ledger of all individual download operations. Columns: `Dataset`, `Official URL`, `Download URL`, `Filename`, `Timestamp`, `Status`, `Mode`, `Size`, `Remarks`.
* **`data_acquisition.log`**: Debugging file detailing rate limiting, backoff retries, and errors.
