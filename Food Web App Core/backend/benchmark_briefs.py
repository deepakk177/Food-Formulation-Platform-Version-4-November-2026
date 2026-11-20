"""
100 Product Brief Definitions for TCS Food Formulator Benchmark
5 Product Categories x 20 Briefs Each = Exactly 100 Briefs (PB001 - PB100)
"""

BENCHMARK_BRIEFS = [
    # =========================================================================
    # CATEGORY 1: PROTEIN BARS / FUNCTIONAL SNACKS (PB001 - PB020)
    # =========================================================================
    {
        "id": "PB001",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Create a vegan high-protein chocolate bar containing at least 20% protein and at most 25% fat. The product should feature a chewy texture, rich cocoa flavour, low water activity (aw <= 0.60), 12-month ambient shelf stability, and a competitive raw material cost below 10.0 USD/kg. Avoid dairy, whey, and animal-derived ingredients.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB002",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Formulate a gluten-free berry energy bar containing at least 15% protein and at least 8% fibre. Requires high moisture retention, soft and chewy texture, vibrant strawberry flavour, clean label ingredients, and raw material cost under 12.0 USD/kg. Prohibit gluten-containing grains and synthetic colorants.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB003",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Design a keto-friendly almond crunch snack bar containing at most 3% sugar and at least 18% protein, with acceptable fat content under 30%. Must provide crunchy texture, nutty almond flavour, 9-month ambient stability, and raw material cost ceiling of 14.0 USD/kg. Prohibit added refined cane sugar.",
        "target_consumer": "Ketogenic Lifestyle Consumers"
    },
    {
        "id": "PB004",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Develop an allergen-free functional seed snack bar containing at least 16% protein and at least 6% fibre. Must maintain cohesive binding without crumbling, pleasant vanilla flavour, low water activity, and 6-month shelf life. Strictly exclude the top 9 allergens including peanuts, tree nuts, soy, dairy, and gluten.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB005",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Formulate a vegan diabetic-friendly mocha protein bar containing at least 22% protein and at most 2% sugar. The formulation requires firm texture, coffee and chocolate flavour, controlled glycemic response, and raw material cost below 11.5 USD/kg. Exclude animal products and high-glycemic syrups.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB006",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Create a clean label plant-based peanut butter protein bar containing at least 20% protein, at least 7% fibre, and controlled fat under 22%. Requires chewy mouthfeel, natural peanut aroma, low bitterness, ambient stability, and cost under 9.0 USD/kg. Prohibit artificial preservatives and dairy derivatives.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB007",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Design a senior-friendly high-protein soft chew snack bar containing at least 18% protein with soft easy-swallow texture. Requires high water binding, gentle vanilla flavour, balanced caloric density, and 9-month ambient shelf life. Avoid tough chewy binders and high-shear textural agents.",
        "target_consumer": "Seniors & Elderly Nutrition"
    },
    {
        "id": "PB008",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Develop an ultra-low-cost school-safe functional protein bar containing at least 15% protein and raw material cost strictly below 6.5 USD/kg. Must be nut-free and dairy-free, featuring crunchy texture, cocoa flavour, and 12-month ambient stability. Prohibit peanuts, tree nuts, and expensive exotic extracts.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB009",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Formulate a vegan endurance electrolyte protein bar containing at least 17% protein, 10% fibre, and balanced sodium content. Requires chewy texture, citrus lemon flavour, low water activity, and 9-month ambient shelf life. Avoid dairy, gelatin, and artificial sweeteners.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB010",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Create a premium chocolate brownie protein bar containing at least 25% protein and at most 18% fat. Requires dense fudge texture, deep cocoa flavour, zero chalkiness, and raw material cost target up to 15.0 USD/kg. Avoid dairy ingredients while maintaining a luxurious confectionery mouthfeel.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB011",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Design a gluten-free vegan apple cinnamon protein bar containing at least 16% protein and at least 8% fibre. Requires soft-baked texture, warming spice aroma, 6-month shelf life, and raw material cost under 10.5 USD/kg. Prohibit gluten-containing cereals, milk, and eggs.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB012",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Develop a high-protein savory snack bar containing at least 20% protein, at most 5% sugar, and controlled fat under 15%. Features crunchy texture, savory herb and garlic notes, low water activity (aw <= 0.55), and 12-month stability. Exclude dairy and artificial flavor enhancers.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB013",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Formulate a dairy-free coconut caramel protein snack bar containing at least 18% protein and at most 20% fat. Requires smooth chewy texture, toasted coconut flavour, ambient stability, and raw material cost below 11.0 USD/kg. Avoid dairy butter, milk powder, and whey.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB014",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Create a gut-health prebiotic protein bar containing at least 15% protein and at least 10% fibre from clean label inulin or resistant dextrin. Requires soft chewy texture, berry vanilla flavour, ambient stability, and raw material cost under 12.5 USD/kg. Prohibit artificial bulking agents.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB015",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Design a high-protein crispy cluster snack containing at least 22% protein and at most 12% fat. Requires crunchy aeration, light chocolate coating, low water activity, and 9-month shelf life. Formulate with raw material cost under 9.5 USD/kg and exclude animal-derived proteins.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB016",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Develop a vegan zero-added-sugar almond protein bar containing at least 20% protein and at most 1% sugar. Must feature firm chewy bite, almond and vanilla flavour, ambient shelf stability, and cost under 13.0 USD/kg. Exclude cane sugar, honey, and dairy products.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB017",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Formulate a hypoallergenic protein energy bite containing at least 14% protein, at least 5% fibre, and no detectable major allergens. Requires cohesive spherical geometry, soft texture, cocoa flavour, and 6-month shelf life. Strictly avoid peanuts, tree nuts, gluten, soy, eggs, and dairy.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB018",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Create a clean label matcha green tea protein bar containing at least 18% protein and controlled fat under 16%. Must provide smooth dense texture, authentic earthy matcha flavour, low bitterness, and ambient shelf stability. Exclude synthetic colors and animal-derived proteins.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB019",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Design a high-fibre oat & chia protein snack bar containing at least 16% protein and at least 9% fibre. Requires chewy texture, natural vanilla flavour, 9-month ambient stability, and cost under 8.5 USD/kg. Prohibit dairy, hydrogenated fats, and high-fructose corn syrup.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB020",
        "category": "Protein Bars / Functional Snacks",
        "brief": "Develop an ultra-high-protein plant bar containing at least 30% protein and at most 14% fat. Requires acceptable chewiness without hardening over 9 months ambient storage, dark chocolate flavour, and raw material cost below 14.5 USD/kg. Avoid dairy proteins and gelatin.",
        "target_consumer": "Athletes & Sports Performance"
    },

    # =========================================================================
    # CATEGORY 2: PLANT-BASED BEVERAGES (PB021 - PB040)
    # =========================================================================
    {
        "id": "PB021",
        "category": "Plant-Based Beverages",
        "brief": "Create a vegan high-protein chocolate RTD beverage containing at least 6% protein and at most 2% fat. Must achieve stable emulsification without phase separation, smooth creamy mouthfeel, rich cocoa flavour, and 9-month ambient shelf stability. Strictly exclude dairy milk, whey, and carrageenan.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB022",
        "category": "Plant-Based Beverages",
        "brief": "Formulate a sugar-free oat vanilla latte beverage containing at least 3% protein and at most 0.5% sugar. Requires stable oil-in-water emulsion, creamy body, aromatic vanilla coffee notes, and 12-month ambient shelf life. Prohibit dairy and added sucrose.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB023",
        "category": "Plant-Based Beverages",
        "brief": "Design a clean label almond protein recovery drink containing at least 5% protein and at least 3% fibre. Requires low sedimentation, smooth texture, toasted almond flavour, and raw material cost under 7.5 USD/kg. Strictly avoid dairy, soy, and synthetic emulsifiers.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB024",
        "category": "Plant-Based Beverages",
        "brief": "Develop a nut-free allergen-safe plant milk beverage for children containing at least 4% protein, calcium fortification, and at most 4% sugar. Must feature smooth creamy texture, natural vanilla flavour, 6-month shelf life, and cost under 5.0 USD/kg. Exclude peanuts, tree nuts, soy, and dairy.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB025",
        "category": "Plant-Based Beverages",
        "brief": "Formulate an elderly-oriented nutrient-dense meal replacement beverage containing at least 7% protein, at least 4% healthy fats, and low viscosity for easy swallowing. Requires mild vanilla flavour, complete emulsification, and 9-month ambient stability. Exclude lactose and dairy whey.",
        "target_consumer": "Seniors & Elderly Nutrition"
    },
    {
        "id": "PB026",
        "category": "Plant-Based Beverages",
        "brief": "Create a ketogenic coconut MCT plant beverage containing at least 8% fat, at most 1% carbohydrates, and 4% protein. Must maintain stable lipid emulsion without creaming, creamy coconut mouthfeel, and ambient shelf stability. Exclude dairy cream and high-glycemic carbohydrates.",
        "target_consumer": "Ketogenic Lifestyle Consumers"
    },
    {
        "id": "PB027",
        "category": "Plant-Based Beverages",
        "brief": "Design a refreshing plant-based citrus electrolyte beverage containing at least 3% protein, low sugar under 4%, and balanced electrolytes. Must achieve optical clarity or light translucency, crisp lemon flavour, and 6-month shelf life. Exclude dairy, artificial food dyes, and heavy gums.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB028",
        "category": "Plant-Based Beverages",
        "brief": "Develop an ultra-low-cost commercial plant-based tea latte beverage containing at least 2.5% protein and raw material cost below 4.0 USD/kg. Must deliver smooth mouthfeel, authentic black tea and dairy-free creamy notes, and 12-month ambient stability. Exclude animal milk.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB029",
        "category": "Plant-Based Beverages",
        "brief": "Formulate a gut-health prebiotic golden turmeric plant drink containing at least 3% protein and 4% soluble fibre. Requires stable suspension of spice particulates, warming ginger-turmeric aroma, low bitterness, and 6-month shelf life. Avoid dairy and synthetic stabilizing gums.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB030",
        "category": "Plant-Based Beverages",
        "brief": "Create a high-protein plant-based berry smoothie drink containing at least 8% protein, at least 5% fibre, and controlled fat under 3%. Must exhibit rich viscous texture, vibrant strawberry-blueberry flavour, and refrigerated 45-day stability. Avoid dairy and artificial coloring agents.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB031",
        "category": "Plant-Based Beverages",
        "brief": "Design a gluten-free plant-based cold brew protein coffee beverage containing at least 6% protein and at most 3% sugar. Requires stable protein dispersion without thermal precipitation during pasteurization, coffee aroma, and 9-month shelf life. Exclude gluten, dairy, and high-fat creamers.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB032",
        "category": "Plant-Based Beverages",
        "brief": "Develop a vegan chocolate hazelnut recovery drink containing at least 5% protein and controlled fat under 4%. Requires silky mouthfeel, roasted hazelnut and cocoa flavour, and raw material cost below 8.0 USD/kg. Strictly avoid dairy milk and animal-derived stabilizers.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB033",
        "category": "Plant-Based Beverages",
        "brief": "Formulate an allergen-free pea protein RTD beverage containing at least 7% protein, zero chalkiness, and low bitterness. Requires effective flavor masking, smooth texture, vanilla flavour, and 12-month ambient stability. Exclude top 9 allergens including soy, dairy, and nuts.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB034",
        "category": "Plant-Based Beverages",
        "brief": "Create a clean label dairy-free matcha latte containing at least 3.5% protein and at most 4% sugar. Must feature homogeneous dispersion without green tea sedimentation, creamy body, and 6-month ambient shelf life. Avoid dairy milk, mono-diglycerides, and artificial additives.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB035",
        "category": "Plant-Based Beverages",
        "brief": "Design a low-calorie plant-based hydration drink containing at least 2% protein, under 20 kcal per 100ml, and zero added sugar. Must provide crisp thirst-quenching mouthfeel, natural berry flavour, and 9-month ambient shelf stability. Exclude dairy and artificial sweeteners.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB036",
        "category": "Plant-Based Beverages",
        "brief": "Develop a functional sleep-support plant-based chamomile latte containing at least 3% protein, low fat under 2%, and soothing herbal vanilla notes. Requires smooth viscosity, thermal stability during retort, and 12-month shelf life. Prohibit dairy and animal-derived ingredients.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB037",
        "category": "Plant-Based Beverages",
        "brief": "Formulate a diabetic-safe unsweetened plant milk containing at least 4% protein, at most 0.2% sugar, and raw material cost under 5.5 USD/kg. Must deliver neutral dairy-like appearance, creamy mouthfeel, and 9-month ambient shelf life. Exclude cane sugar, syrups, and dairy milk.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB038",
        "category": "Plant-Based Beverages",
        "brief": "Create a fortified plant-based breakfast drink containing at least 5% protein, 4% fibre, and essential micronutrients. Requires medium viscosity, pleasant oat vanilla flavour, 6-month ambient shelf stability, and cost under 6.8 USD/kg. Strictly exclude dairy and soy.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB039",
        "category": "Plant-Based Beverages",
        "brief": "Design a high-protein post-workout chai tea plant beverage containing at least 8% protein and at most 3% fat. Must achieve heat-stable protein suspension without grittiness, spiced cinnamon-cardamom notes, and 9-month ambient shelf stability. Exclude animal dairy and whey.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB040",
        "category": "Plant-Based Beverages",
        "brief": "Develop an organic clean-label plant protein shake containing at least 6% protein, at least 3% fibre, and raw material cost below 9.0 USD/kg. Must feature velvety texture, rich cocoa flavour, 12-month shelf life, and zero synthetic hydrocolloids. Exclude dairy and artificial additives.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },

    # =========================================================================
    # CATEGORY 3: PLANT-BASED YOGURT / DAIRY ALTERNATIVES (PB041 - PB060)
    # =========================================================================
    {
        "id": "PB041",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Create a vegan high-protein Greek-style yogurt alternative containing at least 8% protein and at most 4% fat. Must exhibit thick spoonable texture, smooth mouthfeel, pleasant lactic acidity (pH 4.2 - 4.5), low syneresis, and 45-day refrigerated stability. Strictly avoid dairy, gelatin, and carrageenan.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB042",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Formulate a clean label coconut-based vanilla yogurt alternative containing at least 3% protein, at most 5% sugar, and rich creamy body. Requires firm gel structure without phase separation, vanilla aroma, and 60-day refrigerated shelf life. Prohibit dairy milk, gelatin, and artificial stabilizers.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB043",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Design a sugar-free probiotic oat yogurt alternative containing at least 4% protein and at most 0.5% sugar. Must feature smooth creamy texture, balanced tart flavour, low water separation, and cost below 6.5 USD/kg. Exclude added sucrose and dairy-derived cultures.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB044",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Develop an allergen-free plant-based strawberry yogurt alternative for kids containing at least 3.5% protein, at least 3% fibre, and fruit puree blend. Must achieve smooth lump-free texture, natural strawberry aroma, and 45-day shelf life. Strictly exclude nuts, soy, gluten, and dairy.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB045",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Formulate an elderly-friendly nutrient-dense cultured dairy alternative containing at least 6% protein, smooth easy-swallow consistency, and calcium fortification. Requires low astringency, mild creamy flavour, and 60-day refrigerated stability. Exclude dairy lactose and tough particulate ingredients.",
        "target_consumer": "Seniors & Elderly Nutrition"
    },
    {
        "id": "PB046",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Create a keto high-fat coconut yogurt alternative containing at least 12% fat, at most 2% carbohydrates, and 3% protein. Must feature luxurious custard-like texture, natural coconut flavour, and 45-day chilled stability. Strictly avoid dairy cream and high-sugar stabilizers.",
        "target_consumer": "Ketogenic Lifestyle Consumers"
    },
    {
        "id": "PB047",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Design a clean label almond-based blueberry yogurt alternative containing at least 4% protein and at least 4% fibre. Requires glossy appearance, smooth spoonability, blueberry fruit swirl compatibility, and raw material cost under 7.5 USD/kg. Exclude dairy and synthetic gums.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB048",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Develop an ultra-low-cost commercial plant-based yogurt alternative containing at least 3% protein and raw material cost strictly below 4.5 USD/kg. Requires stable gel matrix, pleasant mild tartness, and 45-day shelf life. Exclude animal dairy and premium specialty extracts.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB049",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Formulate a drinkable prebiotic plant-based yogurt alternative containing at least 4% protein and 5% prebiotic soluble fibre. Requires low-viscosity pourable texture, refreshing peach flavour, low wheying-off, and 60-day refrigerated shelf stability. Avoid dairy and artificial texturizers.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB050",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Create a high-protein chocolate plant-based dessert yogurt alternative containing at least 7% protein, at most 6% sugar, and controlled fat under 5%. Requires rich pudding-like body, decadent cocoa flavour, and 45-day stability. Avoid dairy ingredients and synthetic emulsifiers.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB051",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Design a gluten-free soy-free cultured cashew cream cheese alternative containing at least 5% protein and smooth spreadable texture. Requires clean lactic tang, microbiological shelf stability of 60 days, and cost under 11.0 USD/kg. Prohibit gluten, soy, and dairy ingredients.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB052",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Develop a vegan clean-label plain unsweetened yogurt alternative containing at least 5% protein and at most 1% naturally occurring sugar. Requires clean neutral-tart profile, firm set curd, and 45-day shelf life. Strictly avoid dairy, gelatin, and artificial sweeteners.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB053",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Formulate a hypoallergenic hemp and flax yogurt alternative containing at least 6% protein, rich in omega-3 fatty acids, and zero major allergens. Requires smooth creamy mouthfeel, subtle nutty taste, and 45-day refrigerated stability. Exclude nuts, soy, gluten, and dairy.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB054",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Create a functional energy plant-based yogurt alternative containing at least 5% protein, B-vitamins, and refreshing citrus lemon notes. Requires smooth spoonable texture, low syneresis, and 60-day chilled stability. Avoid dairy, high-sugar syrups, and synthetic dyes.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB055",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Design a low-fat plant-based mango yogurt alternative containing at least 4% protein and at most 2% fat. Must achieve creamy body despite low fat content, tropical mango flavour, and raw material cost under 6.0 USD/kg. Exclude dairy cream and animal gelatin.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB056",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Develop an ambient shelf-stable plant-based yogurt alternative pouch containing at least 3.5% protein and 12-month ambient stability through post-fermentation pasteurization. Requires stable hydrocolloid matrix, smooth texture, and fruit flavour. Avoid dairy milk.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB057",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Formulate a savory plant-based garlic and herb yogurt dip alternative containing at least 5% protein, at most 8% fat, and thick dipping viscosity. Requires savory herb flavour, balanced acidity, and 60-day shelf life. Exclude dairy sour cream and animal ingredients.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB058",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Create a clean label raspberry oat yogurt alternative containing at least 4.5% protein, at least 3% fibre, and fruit preparations. Requires smooth spoonable texture, authentic raspberry flavour, and raw material cost below 7.0 USD/kg. Avoid dairy, synthetic colors, and artificial flavors.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB059",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Design a high-protein post-workout vanilla cultured plant cup containing at least 10% protein and at most 3% fat. Requires thick Greek-style texture, clean vanilla finish, low bitterness, and 45-day shelf life. Strictly exclude dairy milk, whey, and gelatin.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB060",
        "category": "Plant-Based Yogurt / Dairy Alternatives",
        "brief": "Develop an organic coconut chia pudding yogurt alternative containing at least 4% protein, 6% fibre, and suspended chia seeds. Requires pleasant viscous mouthfeel, mild coconut flavour, and 45-day refrigerated shelf stability. Prohibit dairy and synthetic chemical stabilizers.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },

    # =========================================================================
    # CATEGORY 4: BAKERY PRODUCTS (PB061 - PB080)
    # =========================================================================
    {
        "id": "PB061",
        "category": "Bakery Products",
        "brief": "Create a vegan high-protein chocolate chip cookie containing at least 15% protein and at most 18% fat. Requires soft-baked chewy texture, rich vanilla and chocolate flavour, 6-month ambient shelf life, and raw material cost under 9.0 USD/kg. Avoid eggs, butter, milk, and whey.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB062",
        "category": "Bakery Products",
        "brief": "Formulate a gluten-free high-fibre sandwich loaf containing at least 8% protein, at least 6% fibre, and soft crumb structure. Requires uniform aeration, 14-day ambient mold-free shelf life, and raw material cost under 5.0 USD/kg. Strictly exclude wheat, rye, barley, and dairy.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB063",
        "category": "Bakery Products",
        "brief": "Design a diabetic-safe low-carb almond bakery muffin containing at least 12% protein, at most 2% sugar, and rich moist crumb. Requires gentle sweetness, almond flavour, and 21-day ambient shelf stability. Prohibit added cane sugar, wheat flour, and high-fructose corn syrup.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB064",
        "category": "Bakery Products",
        "brief": "Develop an allergen-free school-safe blueberry muffin containing at least 7% protein, at least 4% fibre, and soft texture. Requires stable chemical leavening, natural blueberry flavour, and 14-day ambient shelf life. Strictly exclude nuts, eggs, dairy, soy, and gluten.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB065",
        "category": "Bakery Products",
        "brief": "Formulate an elderly-oriented soft nutrient-dense breakfast biscuit containing at least 10% protein, low crumb fragmentation for choking prevention, and calcium fortification. Requires pleasant vanilla flavour and 6-month ambient stability. Exclude hard crunchy inclusions.",
        "target_consumer": "Seniors & Elderly Nutrition"
    },
    {
        "id": "PB066",
        "category": "Bakery Products",
        "brief": "Create a keto-friendly seed & flax artisan bread containing at least 14% protein, at most 3% net carbohydrates, and robust crust. Requires good dough rise, nutty aroma, and 14-day ambient shelf life. Prohibit refined wheat flour and high-sugar additives.",
        "target_consumer": "Ketogenic Lifestyle Consumers"
    },
    {
        "id": "PB067",
        "category": "Bakery Products",
        "brief": "Design a clean label whole-grain oat digestive biscuit containing at least 9% protein, at least 7% fibre, and crumbly snap texture. Requires wholesome toasted oat flavour, 9-month ambient stability, and raw material cost under 6.0 USD/kg. Avoid artificial leaveners and dairy butter.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB068",
        "category": "Bakery Products",
        "brief": "Develop an ultra-low-cost commercial burger bun containing at least 8% protein, soft resilient crumb, and raw material cost strictly below 3.5 USD/kg. Requires uniform gas retention, golden crust, and 14-day ambient mold stability. Exclude expensive dairy powders.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB069",
        "category": "Bakery Products",
        "brief": "Formulate a vegan high-protein brownie containing at least 16% protein and at most 15% fat. Requires dense fudgy mouthfeel, deep cocoa aroma, low water activity (aw <= 0.65), and 6-month ambient shelf life. Strictly avoid eggs, dairy milk, and animal fats.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB070",
        "category": "Bakery Products",
        "brief": "Create a clean label cinnamon spice breakfast muffin containing at least 8% protein, at least 5% fibre, and natural cinnamon aroma. Must achieve dome-shaped rise, tender crumb, 14-day ambient stability, and raw material cost below 6.5 USD/kg. Prohibit synthetic emulsifiers.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB071",
        "category": "Bakery Products",
        "brief": "Design a gluten-free vegan pizza crust containing at least 8% protein, pliable dough rolling characteristics, and crispy baked rim. Requires authentic yeast-fermented aroma, 9-month frozen or 30-day modified atmosphere stability, and cost under 6.0 USD/kg. Exclude gluten and dairy.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB072",
        "category": "Bakery Products",
        "brief": "Develop a high-protein savory cracker containing at least 18% protein, at most 10% fat, and crisp crunchy bite. Requires savory rosemary and sea salt notes, low water activity (aw <= 0.45), and 12-month ambient stability. Exclude dairy cheese and artificial flavor enhancers.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB073",
        "category": "Bakery Products",
        "brief": "Formulate a sugar-free vegan lemon shortbread biscuit containing at least 8% protein and at most 0.5% sugar. Requires crumbly melt-in-mouth texture, zesty citrus flavour, and 6-month ambient shelf life. Avoid cane sugar, animal butter, and eggs.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB074",
        "category": "Bakery Products",
        "brief": "Create a hypoallergenic banana bread snack loaf containing at least 7% protein, at least 4% fibre, and moist texture. Requires natural banana aroma, 14-day ambient shelf life, and raw material cost under 7.0 USD/kg. Strictly exclude eggs, dairy, nuts, soy, and wheat.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB075",
        "category": "Bakery Products",
        "brief": "Design a high-protein soft pretzel containing at least 14% protein, chewy crumb, and traditional alkaline-browned exterior. Requires savory salt topping, 7-day ambient stability, and raw material cost below 4.5 USD/kg. Prohibit dairy and animal-derived dough conditioners.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB076",
        "category": "Bakery Products",
        "brief": "Develop a clean label gluten-free chocolate cupcake containing at least 9% protein, at most 12% fat, and light aerated crumb. Requires cocoa flavour, 21-day ambient shelf life, and raw material cost under 8.5 USD/kg. Exclude gluten, dairy, and artificial emulsifiers.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB077",
        "category": "Bakery Products",
        "brief": "Formulate an energy-dense functional trail biscuit containing at least 15% protein, 8% fibre, and healthy seed lipids. Requires crunchy durable structure that resists transit breakage, cranberry vanilla flavour, and 12-month shelf life. Exclude dairy and hydrogenated fats.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB078",
        "category": "Bakery Products",
        "brief": "Create a vegan brioche-style soft dinner roll containing at least 8% protein, golden sheen, and rich feathery crumb. Must achieve authentic buttery aroma using plant-based fats, 10-day ambient shelf life, and cost under 4.0 USD/kg. Strictly exclude dairy butter, milk, and eggs.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB079",
        "category": "Bakery Products",
        "brief": "Design a low-sodium high-potassium sandwich loaf for heart health containing at least 9% protein, at most 150mg sodium per 100g, and soft white crumb. Requires balanced yeast flavour and 14-day mold-free shelf life. Prohibit excessive salt and dairy powders.",
        "target_consumer": "Seniors & Elderly Nutrition"
    },
    {
        "id": "PB080",
        "category": "Bakery Products",
        "brief": "Develop an organic gingerbread functional biscuit containing at least 10% protein, at least 5% fibre, and warming ginger-molasses notes. Requires snappy bite, 9-month ambient shelf life, and raw material cost under 7.5 USD/kg. Exclude dairy, eggs, and synthetic preservatives.",
        "target_consumer": "Health-Conscious Active Adults"
    },

    # =========================================================================
    # CATEGORY 5: SAUCES / SPREADS / EMULSIFIED PRODUCTS (PB081 - PB100)
    # =========================================================================
    {
        "id": "PB081",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Create an egg-free vegan mayonnaise emulsion containing at least 45% fat, at most 2% sugar, and thick spoonable consistency. Must achieve stable oil-in-water emulsion without phase separation, creamy mouthfeel, balanced lemon-vinegar acidity, and 9-month ambient stability. Strictly exclude eggs, dairy, and artificial colorants.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB082",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Formulate a clean label chocolate hazelnut spread containing at least 8% protein, at most 20% sugar, and smooth spreadability at room temperature. Requires roasted hazelnut and cocoa flavour, low oil separation, 12-month ambient shelf life, and cost under 11.0 USD/kg. Avoid dairy milk, whey, and palm oil.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB083",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Design a diabetic-safe sugar-free tomato ketchup containing at least 3% protein, at most 1% naturally occurring sugar, and rich clinging viscosity. Requires savory ripe tomato flavour, balanced vinegar tang, and 12-month ambient shelf stability. Strictly prohibit cane sugar, corn syrup, and artificial dyes.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB084",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Develop an allergen-free school-safe sandwich spread containing at least 6% protein, smooth spreadable texture, and savory roasted seed flavour. Must be shelf-stable for 9 months under ambient storage and cost below 7.0 USD/kg. Strictly exclude peanuts, tree nuts, soy, gluten, and dairy.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB085",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Formulate an elderly-friendly nutrient-dense savory gravy sauce containing at least 5% protein, smooth lump-free texture for dysphagia management, and controlled sodium. Requires rich savory roasted herb flavour, low viscosity resistance, and 12-month shelf life. Exclude dairy butter and gluten.",
        "target_consumer": "Seniors & Elderly Nutrition"
    },
    {
        "id": "PB086",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Create a keto high-fat creamy garlic dip containing at least 60% fat, at most 2% net carbs, and 3% protein. Must achieve robust emulsion stability, pungent garlic herb notes, and 6-month refrigerated shelf life. Prohibit dairy cream, starch fillers, and added sugars.",
        "target_consumer": "Ketogenic Lifestyle Consumers"
    },
    {
        "id": "PB087",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Design a clean label vegan creamy ranch dressing containing at least 30% fat, at most 3% sugar, and pourable emulsion viscosity. Requires herbal dill-garlic flavour, low syneresis, 6-month ambient shelf life, and raw material cost under 6.5 USD/kg. Exclude eggs, dairy buttermilk, and modified starches.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB088",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Develop an ultra-low-cost commercial emulsified white sauce containing at least 2.5% protein, smooth viscosity, and raw material cost strictly below 3.0 USD/kg. Requires stable emulsion under freeze-thaw conditions and 9-month shelf life. Exclude expensive dairy cream.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB089",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Formulate a high-protein savory peanut satay sauce containing at least 12% protein, controlled fat under 20%, and rich coating viscosity. Requires authentic roasted peanut and chili aroma, ambient stability, and raw material cost below 7.5 USD/kg. Exclude dairy and artificial flavorings.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB090",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Create a clean label dairy-free cheese style spread containing at least 6% protein, smooth knife-spreadable texture, and fermented savory umami notes. Requires 60-day refrigerated stability, natural yellow color, and cost under 9.5 USD/kg. Strictly exclude dairy milk, casein, and synthetic preservatives.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB091",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Design a low-calorie plant-based vinaigrette dressing containing at most 10% fat, at most 3% sugar, and stable suspended herbs. Requires bright lemon-herb acidity, attractive translucent emulsion, and 12-month ambient shelf life. Prohibit high-calorie oils and synthetic gums.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB092",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Develop a spicy chipotle vegan mayo emulsion containing at least 40% fat, 2% protein, and smooth dipping texture. Requires smoky chipotle pepper flavour, robust thermal emulsion stability, and 9-month ambient shelf life. Exclude eggs, dairy, and artificial colors.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB093",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Formulate an allergen-free sweet caramel spread containing at least 3% protein, at most 25% sugar, and rich buttery mouthfeel. Requires smooth glossy appearance, 9-month ambient stability, and cost under 8.0 USD/kg. Strictly exclude dairy butter, milk powder, peanuts, and tree nuts.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB094",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Create a high-protein hummus spread containing at least 10% protein, at most 12% fat, and velvety dipping body. Requires roasted garlic and sesame tahini flavour, 45-day chilled stability, and cost below 5.5 USD/kg. Avoid dairy and synthetic preservatives.",
        "target_consumer": "Athletes & Sports Performance"
    },
    {
        "id": "PB095",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Design a clean label plant-based hollandaise sauce alternative containing at least 35% healthy fat, smooth emulsified pourability, and subtle lemon acidity. Must remain stable upon warm holding (50°C), with 6-month shelf life. Exclude egg yolks and dairy butter.",
        "target_consumer": "Vegan & Plant-Based Consumers"
    },
    {
        "id": "PB096",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Develop a diabetic-friendly smoky barbecue sauce containing at least 3% protein, at most 1.5% sugar, and clinging viscosity. Requires deep smoke and tomato flavour, 12-month ambient shelf life, and raw material cost under 4.5 USD/kg. Exclude molasses, brown sugar, and high-fructose corn syrup.",
        "target_consumer": "Diabetic & Low-GI Consumers"
    },
    {
        "id": "PB097",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Formulate a hypoallergenic seed butter spread containing at least 15% protein, at least 6% fibre, and controlled fat under 35%. Requires silky spreadability, rich toasted sunflower seed aroma, and 12-month ambient stability. Exclude peanuts, tree nuts, and dairy.",
        "target_consumer": "Children & School Age"
    },
    {
        "id": "PB098",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Create a functional turmeric and black pepper golden tahini spread containing at least 8% protein, high mineral content, and smooth spreadability. Requires earthy nutty flavour, bright natural yellow hue, and 9-month ambient shelf life. Avoid dairy and artificial coloring agents.",
        "target_consumer": "Health-Conscious Active Adults"
    },
    {
        "id": "PB099",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Design a low-sodium vegan pesto spread containing at least 7% protein, at most 200mg sodium per 100g, and rich olive-herb texture. Requires fragrant basil and garlic notes, 60-day refrigerated stability, and cost under 10.0 USD/kg. Strictly exclude dairy parmesan cheese and animal rennet.",
        "target_consumer": "Seniors & Elderly Nutrition"
    },
    {
        "id": "PB100",
        "category": "Sauces / Spreads / Emulsified Products",
        "brief": "Develop an organic clean label dark chocolate almond butter spread containing at least 12% protein, at most 15% sugar, and rich glossy spreadability. Requires intense roasted almond and cocoa flavour, 12-month ambient shelf life, and raw material cost below 13.5 USD/kg. Avoid dairy and hydrogenated oils.",
        "target_consumer": "Health-Conscious Active Adults"
    }
]
