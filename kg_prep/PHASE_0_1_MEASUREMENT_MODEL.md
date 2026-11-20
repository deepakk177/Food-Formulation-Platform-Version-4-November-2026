# PHASE 0.1 / 0.2: QUANTITATIVE MEASUREMENT & COMMERCIAL COST MODEL

**Document Version:** 2.0.0 (Phase 0.2 Revision)  
**Status:** FROZEN & RATIFIED  
**Scope:** A unified quantitative measurement architecture covering nutritional, physical, rheological, regulatory, and commercial pricing models.

---

## 1. Architectural Philosophy: The Anti-Corruption Principle

In food science data engineering, a major source of system failure is **dimensional corruption**—the blind conversion or comparison of incompatible physical units, or the loss of measurement context.

### Examples of Prohibited Dimensional Corruptions
1. **Blind Percentage Normalization**: Converting `5.0%` moisture (w/w) to `50,000 mg/kg` and treating it as a toxicological limit, or converting `15% Daily Value` (DV) of calcium to grams without reference to the statutory standard.
2. **Dimensionless Quantity Mutilation**: Treating `pH 3.5` or `Water Activity (Aw) 0.65` as masses or concentrations.
3. **Loss of Rheological Context**: Stating that a hydrocolloid has `viscosity: 2500 cP` without stating the solution concentration (e.g., `1.0% w/w in deionized water`), temperature (`25°C`), spindle type, and shear rate (`20 rpm`).
4. **Nutrient Basis Erasure**: Equating protein content expressed on a **dry weight basis (DWB)** with protein on an **as-is / wet weight basis (WWB)**. In plant proteins, this difference causes a 6–12% error in mass balance.

---

## 2. The Unified Measurement Envelope

Every quantitative observation in the Knowledge Graph—whether a nutrient level, a regulatory limit, an ingredient cost, a viscosity measurement, or a batch inclusion—is encapsulated by the standard **Quantitative Measurement Envelope**:

```json
{
  "measurement_id": "MEAS-VISC-ING-0012-01",
  "entity_id": "ING-XANTHAN-GUM-FOODON",
  "parameter_name": "apparent_viscosity",
  "physical_dimension": "DYNAMIC_VISCOSITY",
  
  "value_numeric": 1450.0,
  "value_min": 1300.0,
  "value_max": 1600.0,
  "value_text": "1300 - 1600 cP",
  "operator": "BETWEEN",
  
  "unit_original": "cP",
  "unit_canonical": "mPa.s",
  "conversion_factor": 1.0,
  
  "measurement_basis": "1.0% w/w aqueous solution, 1% KCl",
  "measurement_method": "Brookfield LV, Spindle #3, 60 rpm",
  "conditions": {
    "temperature_celsius": 25.0,
    "ph": 7.0,
    "shear_rate_sec_inv": 73.4
  },
  
  "source_dataset_id": "SRC-CARGILL-SPEC",
  "dataset_version": "2024-Q1",
  "source_document_id": "TDS-XANTHAN-200-MESH",
  "source_location": "Page 1, Table: Rheological Specifications",
  "extraction_timestamp": "2026-11-16T12:00:00Z",
  "valid_from": "2024-01-01",
  "valid_until": "2025-12-31",
  "evidence_type": "MANUFACTURER_TDS",
  "extraction_confidence": 0.98,
  "evidence_quality": "INDUSTRY_SELF_REPORTED",
  "verification_status": "SOURCE_VERIFIED"
}
```

---

## 3. Dimensional Taxonomies and Strict Normalization Rules

| Physical Dimension | Canonical Base Unit | Allowable Source Units | Conversion Rules | Prohibited Transformations |
|---|---|---|---|---|
| **Mass** | Gram (`g`) | `kg`, `mg`, `mcg`, `ug`, `oz`, `lb`, `ton` | $1\text{ kg} = 1000\text{ g}$<br>$1\text{ mg} = 10^{-3}\text{ g}$<br>$1\text{ mcg} = 10^{-6}\text{ g}$<br>$1\text{ lb} = 453.59237\text{ g}$ | Never convert to concentration without known batch or serving mass. |
| **Mass Concentration** | Milligram per kilogram (`mg/kg`) | `ppm`, `g/kg`, `mg/100g`, `g/100g`, `ppb`, `ug/g` | $1\text{ ppm} = 1.0\text{ mg/kg}$<br>$1\text{ g/kg} = 1000\text{ mg/kg}$<br>$1\text{ g/100g} = 10,000\text{ mg/kg}$<br>$1\text{ ppb} = 0.001\text{ mg/kg}$ | Never convert dimensionless ratio or % DV to concentration without explicit target mass. |
| **Volume** | Milliliter (`mL`) | `L`, `uL`, `fl_oz`, `gal`, `cup`, `tbsp`, `tsp` | $1\text{ L} = 1000\text{ mL}$<br>$1\text{ uL} = 10^{-3}\text{ mL}$<br>$1\text{ fl oz} = 29.5735\text{ mL}$ | Never convert volume to mass without explicit specific gravity / density. |
| **Temperature** | Degrees Celsius (`°C`) | `°C`, `°F`, `K` | $T_C = (T_F - 32) \times \frac{5}{9}$<br>$T_C = T_K - 273.15$ | Never perform scalar multiplication without affine offset. |
| **Dynamic Viscosity** | Millipascal-second (`mPa·s`) | `cP`, `Pa·s`, `mPa·s`, `P` | $1\text{ cP} = 1.0\text{ mPa·s}$<br>$1\text{ Pa·s} = 1000\text{ mPa·s}$ | Never compare viscosities measured at different shear rates or concentrations. |
| **Pressure** | Bar (`bar`) | `bar`, `psi`, `kPa`, `MPa`, `atm` | $1\text{ psi} = 0.0689476\text{ bar}$<br>$1\text{ MPa} = 10.0\text{ bar}$<br>$1\text{ kPa} = 0.01\text{ bar}$ | Never convert to gauge pressure without atmospheric pressure reference. |
| **Water Activity** | Dimensionless (`Aw`) | Ratio `0.00` to `1.00` | Dimensionless equilibrium relative humidity ($Aw = \frac{ERH\%}{100}$) | Never convert $Aw$ directly to moisture percentage (requires sorption isotherm). |
| **pH** | Dimensionless (`pH`) | Scale `0.0` to `14.0` | Negative logarithm of hydronium ion activity ($-\log_{10}[H_3O^+]$) | Never average pH linearly; hydrogen ion concentrations must be averaged exponentially. |
| **Energy** | Kilocalories (`kcal`) | `kcal`, `kJ` | $1\text{ kcal} = 4.184\text{ kJ}$ | Atwater factors must only be applied to validated proximate macros. |
| **Percentage** | Percentage (`%`) | `% w/w`, `% w/v`, `% v/v`, `% dry solids`, `% DV` | Must preserve explicit basis qualifier. | Never strip basis suffix. `% w/w` $\neq$ `% w/v` $\neq$ `% DV`. |

---

## 4. The Commercial Cost & Pricing Model

### A. Strict Separation of Price Types
The Knowledge Graph strictly distinguishes four pricing tiers:

1. **`COMMODITY_MANDI`**: Wholesale mandi or commodity exchange price for raw, unformulated agricultural goods (e.g., AGMARKNET wheat, soy, sugar prices; USDA AMS market news). Expressed per quintal or metric ton.
2. **`SUPPLIER_QUOTATION`**: A formal commercial quote issued by a specific ingredient supplier (e.g., Cargill quote for *De-oiled Soy Lecithin Grade A*). Bound to a specific `supplier_id`, quote validity window, and Minimum Order Quantity (MOQ).
3. **`MANUFACTURER_CATALOG`**: Published list price in an ingredient manufacturer's catalog.
4. **`GRADE_SPECIFIC_PRICE`**: Pricing explicitly bound to an `IngredientGrade` (e.g., *Pea Protein Isolate 85%* priced at \$7.50/kg vs. *Pea Protein Concentrate 60%* priced at \$3.80/kg).

> **ABSOLUTE INVARIANT**: Wholesale agricultural mandi prices (e.g., AGMARKNET) must **NEVER** be represented as manufacturer or supplier ingredient quotations.

### B. Cost Record Schema (`Nodes/CostRecords.csv`)

```sql
CREATE TABLE IF NOT EXISTS cost_records (
    cost_record_id VARCHAR PRIMARY KEY,
    ingredient_id VARCHAR NOT NULL,
    ingredient_grade_id VARCHAR,
    supplier_id VARCHAR,
    price_type VARCHAR NOT NULL, -- COMMODITY_MANDI, SUPPLIER_QUOTATION, MANUFACTURER_CATALOG, GRADE_SPECIFIC
    price_value DOUBLE NOT NULL,
    currency VARCHAR NOT NULL,   -- ISO 4217 (USD, INR, EUR)
    pricing_unit VARCHAR NOT NULL, -- kg, MT, quintal, lb
    price_per_kg_usd DOUBLE,     -- Standardized conversion on price_date
    geographic_region VARCHAR NOT NULL, -- e.g. "India-MadhyaPradesh", "US-Midwest", "Global"
    market_center VARCHAR,       -- Mandi name or trading hub
    min_order_quantity DOUBLE,
    moq_unit VARCHAR,
    price_date VARCHAR NOT NULL, -- ISO 8601 YYYY-MM-DD
    valid_until VARCHAR,         -- Expiration date of quote
    source_dataset_id VARCHAR NOT NULL,
    source_record_id VARCHAR NOT NULL,
    evidence_type VARCHAR NOT NULL,
    extraction_confidence DOUBLE NOT NULL,
    verification_status VARCHAR NOT NULL
);
```

### C. Zero Imputation Policy in Cost Evaluation
- If an ingredient lacks a verified quotation or commodity price, its cost is explicitly `NULL`.
- The formulation backend evaluates total cost only across components with valid pricing. If any ingredient has a missing cost, the formulation cost status is flagged as `COST_PARTIAL` or `COST_UNKNOWN`.
- Fabricated fallback prices (e.g., the legacy `$12.50/kg` constant) are strictly prohibited.
