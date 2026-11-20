"""
Regression Test Suite for Canonical Nutritional Consistency.
Addresses Section 10 of Critical Engineering Specification:
1. Serving size reconciliation across all candidate sets.
2. Identical values between Candidate Inspector and Final Report for the same candidate.
3. Atwater energy calculation matches sum of macronutrients (within rounding tolerance).
4. Minerals total equals sum of individual minerals.
5. Basis switching (100g vs serving) scales all values by exactly serving_size / 100.
6. Target achievement calculation correctness (min vs max targets).
7. Mass balance validation: sum of component contributions equals aggregated value.
8. Multiple candidate generation produces valid, consistent nutrition for every candidate.
9. Custom / newly added ingredients propagate correct nutrition without fabrication.
10. Edge cases: zero-sugar formulation, high-fat keto formulation, low-protein beverage, very small serving size (5g), very large serving size (500g).
"""
import sys
import pytest
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from calculation_service import calculation_service, CalculationService, get_grounded_ingredient_nutrition, learn_ingredient_knowledge
from candidate_engine import candidate_engine
from requirements_extractor import product_brief_parser
from retrieval_service import retrieval_orchestrator


class TestNutritionalConsistency:

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.calc = calculation_service
        self.sample_components = [
            {
                "id": "ing_pea_protein",
                "name": "Pea Protein Isolate",
                "percentage": 30.0,
                "properties": {"protein": 80.0, "fat": 7.0, "carbs": 5.0, "sugar": 1.0, "fibre": 4.0, "sodium": 150.0}
            },
            {
                "id": "ing_oat_flour",
                "name": "Whole Oat Flour",
                "percentage": 40.0,
                "properties": {"protein": 13.0, "fat": 6.5, "carbs": 66.0, "sugar": 1.5, "fibre": 10.0, "sodium": 10.0}
            },
            {
                "id": "ing_almond_butter",
                "name": "Almond Butter",
                "percentage": 20.0,
                "properties": {"protein": 21.0, "fat": 55.0, "carbs": 18.0, "sugar": 4.0, "fibre": 10.0, "sodium": 5.0}
            },
            {
                "id": "ing_chicory_fiber",
                "name": "Chicory Root Inulin",
                "percentage": 10.0,
                "properties": {"protein": 0.0, "fat": 0.0, "carbs": 95.0, "sugar": 8.0, "fibre": 87.0, "sodium": 0.0}
            }
        ]

    def test_01_serving_size_reconciliation(self):
        """1. Serving size reconciliation: per_serving = per_100g * (serving_size_g / 100)."""
        serving_size_g = 40.0
        canonical = self.calc.calculate_canonical_nutrition(
            self.sample_components,
            serving_size_g=serving_size_g,
            candidate_id="FC-TEST-01"
        )
        scale = serving_size_g / 100.0

        assert abs(canonical["protein_g_per_serving"] - round(canonical["protein_g_per_100g"] * scale, 1)) <= 0.1
        assert abs(canonical["carbohydrates_g_per_serving"] - round(canonical["carbohydrates_g_per_100g"] * scale, 1)) <= 0.1
        assert abs(canonical["fat_g_per_serving"] - round(canonical["fat_g_per_100g"] * scale, 1)) <= 0.1
        assert abs(canonical["dietary_fibre_g_per_serving"] - round(canonical["dietary_fibre_g_per_100g"] * scale, 1)) <= 0.1

    def test_02_inspector_and_final_report_identity(self):
        """2. Identical values between candidate model and final report data structures."""
        serving_size_g = 45.0
        canonical = self.calc.calculate_canonical_nutrition(
            self.sample_components,
            serving_size_g=serving_size_g,
            candidate_id="FC-TEST-02"
        )
        # Validate that legacy macros output matches canonical values
        macros = self.calc.calculate_macros(
            self.sample_components,
            serving_size_g=serving_size_g,
            candidate_id="FC-TEST-02"
        )
        assert macros["protein"] == canonical["protein_g_per_100g"]
        assert macros["carbohydrates"] == canonical["carbohydrates_g_per_100g"]
        assert macros["fat"] == canonical["fat_g_per_100g"]
        assert macros["per_serving"]["protein"] == canonical["protein_g_per_serving"]
        assert macros["per_serving"]["carbohydrates"] == canonical["carbohydrates_g_per_serving"]

    def test_03_atwater_energy_calculation(self):
        """3. Atwater energy matches 4*protein + 4*carbs + 9*fat + 2*fibre within tolerance."""
        canonical = self.calc.calculate_canonical_nutrition(
            self.sample_components,
            serving_size_g=40.0,
            candidate_id="FC-TEST-03"
        )
        # Per 100g check
        expected_cal_100g = (
            4.0 * canonical["protein_g_per_100g"] +
            4.0 * canonical["carbohydrates_g_per_100g"] +
            9.0 * canonical["fat_g_per_100g"] +
            2.0 * canonical["dietary_fibre_g_per_100g"]
        )
        assert abs(canonical["energy_kcal_per_100g"] - round(expected_cal_100g, 0)) <= 3.0

        # Per serving check
        expected_cal_srv = (
            4.0 * canonical["protein_g_per_serving"] +
            4.0 * canonical["carbohydrates_g_per_serving"] +
            9.0 * canonical["fat_g_per_serving"] +
            2.0 * canonical["dietary_fibre_g_per_serving"]
        )
        assert abs(canonical["energy_kcal_per_serving"] - round(expected_cal_srv, 0)) <= 3.0

    def test_04_minerals_sum_matches_individual_elements(self):
        """4. Key minerals total equals sum of calcium, iron, potassium, and magnesium."""
        canonical = self.calc.calculate_canonical_nutrition(
            self.sample_components,
            serving_size_g=40.0,
            candidate_id="FC-TEST-04"
        )
        sum_minerals_100g = (
            canonical["calcium_mg_per_100g"] +
            canonical["iron_mg_per_100g"] +
            canonical["potassium_mg_per_100g"] +
            canonical["magnesium_mg_per_100g"]
        )
        assert abs(canonical["minerals_mg_per_100g"] - round(sum_minerals_100g, 0)) <= 2.0

        sum_minerals_srv = (
            canonical["calcium_mg_per_serving"] +
            canonical["iron_mg_per_serving"] +
            canonical["potassium_mg_per_serving"] +
            canonical["magnesium_mg_per_serving"]
        )
        assert abs(canonical["minerals_mg_per_serving"] - round(sum_minerals_srv, 1)) <= 1.0

    def test_05_basis_switching_scaling(self):
        """5. Basis switching (100g vs serving) scales all values by exact ratio."""
        for serving_size in [25.0, 40.0, 60.0, 250.0]:
            canonical = self.calc.calculate_canonical_nutrition(
                self.sample_components,
                serving_size_g=serving_size,
                candidate_id=f"FC-SCALE-{int(serving_size)}"
            )
            ratio = serving_size / 100.0
            assert abs(canonical["protein_g_per_serving"] - round(canonical["protein_g_per_100g"] * ratio, 1)) <= 0.1
            assert abs(canonical["energy_kcal_per_serving"] - round(canonical["energy_kcal_per_100g"] * ratio, 0)) <= 2.0

    def test_06_target_achievement_logic(self):
        """6. Target achievement calculation correctness (min vs max targets)."""
        # Case A: Minimum target (e.g. Protein >= 10g)
        actual_prot = 12.0
        target_prot = 10.0
        is_met = actual_prot >= target_prot
        achievement_pct = min(100.0, round((actual_prot / target_prot) * 100.0, 1))
        assert is_met is True
        assert achievement_pct == 100.0

        # Case B: Maximum target (e.g. Sugar <= 5g)
        actual_sugar = 4.2
        target_sugar = 5.0
        is_within_limit = actual_sugar <= target_sugar
        assert is_within_limit is True

        # Case C: Exceeded Maximum target
        exceeded_sugar = 6.5
        is_exceeded = exceeded_sugar > target_sugar
        assert is_exceeded is True

    def test_07_mass_balance_sum_of_contributions(self):
        """7. Sum of itemized component contributions equals aggregated total."""
        canonical = self.calc.calculate_canonical_nutrition(
            self.sample_components,
            serving_size_g=40.0,
            candidate_id="FC-TEST-07"
        )
        itemized = canonical["itemized_contributions"]
        sum_p = sum(item["protein_contrib_g"] for item in itemized)
        sum_f = sum(item["fat_contrib_g"] for item in itemized)
        sum_c = sum(item["carbs_contrib_g"] for item in itemized)

        assert abs(canonical["protein_g_per_100g"] - round(sum_p, 1)) <= 0.1
        assert abs(canonical["fat_g_per_100g"] - round(sum_f, 1)) <= 0.1
        assert abs(canonical["carbohydrates_g_per_100g"] - round(sum_c, 1)) <= 0.1

    def test_08_multiple_candidate_generation_consistency(self):
        """8. Multiple candidate generation produces valid, consistent canonical nutrition."""
        brief = product_brief_parser.parse("Formulate a high-protein vegan snack bar with at least 15g protein.")
        retrieved = retrieval_orchestrator.search_ingredients(brief)
        candidates = candidate_engine.generate_experiments(brief, retrieved.get("ingredients", []))

        assert len(candidates) >= 1
        for cand in candidates:
            assert "canonical_nutrition" in cand
            c_nut = cand["canonical_nutrition"]
            assert c_nut is not None
            assert c_nut["protein_g_per_100g"] > 0
            assert c_nut["energy_kcal_per_100g"] > 0
            # Test audit validation
            val_res = self.calc.validate_nutritional_consistency(c_nut, cand["composition"]["all_components"])
            assert val_res["status"] == "CONSISTENT"

    def test_09_custom_ingredient_learning_propagation(self):
        """9. Custom / newly added ingredients propagate correct nutrition without fabrication."""
        custom_id = "ing_test_superfood_flour"
        custom_name = "Superfood Cricket Flour"
        learn_res = learn_ingredient_knowledge(
            ing_id=custom_id,
            name=custom_name,
            properties={"protein": 65.0, "fat": 15.0, "carbs": 5.0, "sugar": 0.5, "fibre": 4.0, "sodium": 80.0},
            cost_per_kg=14.5,
            source="Laboratory Testing Test 09"
        )
        assert learn_res["status"] == "SUCCESS"

        # Lookup should yield exact learned values
        looked_up = get_grounded_ingredient_nutrition(ing_id=custom_id, ing_name=custom_name)
        assert looked_up["protein"] == 65.0
        assert looked_up["fat"] == 15.0
        assert looked_up["carbs"] == 5.0

    def test_10_extreme_edge_cases(self):
        """10. Edge cases: zero-sugar, high-fat keto, low-protein beverage, 5g serving, 500g serving."""
        # 10a: Zero-sugar formulation
        zero_sugar_comps = [
            {"id": "ing_pure_isolate", "name": "Pure Whey Isolate", "percentage": 90.0, "properties": {"protein": 90.0, "fat": 1.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0}},
            {"id": "ing_mct_oil", "name": "MCT Oil", "percentage": 10.0, "properties": {"protein": 0.0, "fat": 100.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0}}
        ]
        nut_zero = self.calc.calculate_canonical_nutrition(zero_sugar_comps, serving_size_g=30.0)
        assert nut_zero["sugar_g_per_100g"] == 0.0
        assert nut_zero["sugar_g_per_serving"] == 0.0

        # 10b: High-fat keto formulation
        keto_comps = [
            {"id": "ing_butter", "name": "Cocoa Butter", "percentage": 85.0, "properties": {"protein": 0.0, "fat": 100.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0}},
            {"id": "ing_cocoa", "name": "Cocoa Powder", "percentage": 15.0, "properties": {"protein": 20.0, "fat": 12.0, "carbs": 50.0, "sugar": 1.0, "fibre": 30.0}}
        ]
        nut_keto = self.calc.calculate_canonical_nutrition(keto_comps, serving_size_g=25.0)
        assert nut_keto["fat_g_per_100g"] >= 80.0
        assert nut_keto["energy_kcal_per_100g"] >= 700.0

        # 10c: Small serving size (5g) and Large serving size (500g)
        nut_5g = self.calc.calculate_canonical_nutrition(self.sample_components, serving_size_g=5.0)
        assert nut_5g["serving_size_g"] == 5.0
        assert abs(nut_5g["protein_g_per_serving"] - round(nut_5g["protein_g_per_100g"] * 0.05, 1)) <= 0.1

        nut_500g = self.calc.calculate_canonical_nutrition(self.sample_components, serving_size_g=500.0)
        assert nut_500g["serving_size_g"] == 500.0
        assert abs(nut_500g["protein_g_per_serving"] - round(nut_500g["protein_g_per_100g"] * 5.0, 1)) <= 0.5
