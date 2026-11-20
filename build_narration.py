import os
import asyncio
import edge_tts
import imageio_ffmpeg
import subprocess

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

SCENES = [
    {
        "id": 1,
        "title": "Platform Introduction & Landing Page",
        "route": "/",
        "script": (
            "Welcome to the Food Formulation AI Platform — an enterprise-grade computational intelligence system "
            "engineered for food scientists, research chefs, and product development engineers. "
            "In modern industrial food manufacturing, developing new formulations has historically been a lengthy, "
            "trial-and-error endeavor, often demanding dozens of bench-top kitchen trials, pilot-plant test runs, "
            "and extensive sensory panels that can span six to eighteen months. "
            "The Food Formulator platform transforms this paradigm by combining an extensive knowledge graph of "
            "nearly twenty-four thousand characterized ingredients with automated constraint discovery, "
            "numerical mass balance optimization, and multi-jurisdictional regulatory compliance. "
            "In this comprehensive demonstration, we will explore the complete end-to-end capabilities of the platform, "
            "from unstructured brief submission to final manufacturing specification."
        )
    },
    {
        "id": 2,
        "title": "Central Command Dashboard & Workspace Overview",
        "route": "/dashboard",
        "script": (
            "We begin on the central application dashboard. The persistent left-hand navigation sidebar provides "
            "seamless access to all platform modules: the Five-Stage Guided Formulation Wizard, the Expert Studio "
            "for manual formulation adjustments, the comprehensive Ingredient Catalog, the interactive Knowledge Graph "
            "Explorer, and the Multi-Jurisdictional Regulatory Matrix. "
            "On the main dashboard canvas, formulation teams can monitor active research and development projects, "
            "overall compliance pass rates, total ingredient nodes indexed in the system, and cost optimization benchmarks. "
            "We can also review existing projects in the laboratory database, such as Gluten-Free Sandwich Bread, "
            "Energy Bars, and Cranberry Protein Confectionery. Each project maintains its own formulation iterations, "
            "target parameters, and regulatory audit trail."
        )
    },
    {
        "id": 3,
        "title": "Stage 1: Natural Language Product Brief Submission",
        "route": "/dashboard/formulate/guided (Stage 1)",
        "script": (
            "We now enter the Guided Formulator to begin our flagship five-stage workflow. "
            "Stage 1 accepts unstructured natural-language product specifications directly from marketing or culinary briefs. "
            "For this demonstration, we submit a rigorous commercial requirement: "
            "Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, "
            "at most 28% sugar, creamy melt, rich vanilla and cocoa flavor, 12-month shelf life, and free from dairy ingredients. "
            "Notice how this brief encapsulates multiple interdependent constraints: compositional floors for cocoa butter, "
            "nutritional thresholds for protein and sugar, strict vegan and dairy-free dietary standards, "
            "rheological texture preferences, and ambient shelf-life stability. "
            "We select Confectionery and Chocolate as our target category, designate North America FDA as our target market, "
            "and click Analyze Brief to trigger the natural language processing engine."
        )
    },
    {
        "id": 4,
        "title": "Stage 2: Automated Constraint Discovery & Entity Extraction",
        "route": "/dashboard/formulate/guided (Stage 2)",
        "script": (
            "In Stage 2, the extraction engine has parsed the brief and successfully discovered eleven distinct structured constraints. "
            "The system maps the requirements into actionable parameters: mandatory vegan dietary status, complete dairy allergen exclusion, "
            "a minimum protein target of 7%, a maximum sugar ceiling of 28%, and a critical minimum of 25% cocoa butter "
            "to ensure authentic chocolate crystallization and snap. "
            "Sensory attributes including creamy melt mouthfeel and rich vanilla and cocoa flavor profiles are identified as functional targets, "
            "alongside a 12-month ambient shelf-life requirement. "
            "Crucially, the platform automatically prunes conflicting ingredients and impossible allergen constraints before solving, "
            "preventing infeasible formulation sets. With all discovered constraints verified, we advance to goal prioritization."
        )
    },
    {
        "id": 5,
        "title": "Stage 3: Hard Constraints & Soft Objectives Prioritization",
        "route": "/dashboard/formulate/guided (Stage 3)",
        "script": (
            "Stage 3 demonstrates the platform's flexible constraint management interface. "
            "Here, constraints are divided into two distinct operational classes: Hard Constraints and Soft Objectives. "
            "Hard constraints represent non-negotiable feasibility boundaries — including food safety regulations, legal maximums, "
            "and zero-tolerance allergen exclusions. If a formulation candidate violates even one hard constraint, it is mathematically disqualified. "
            "In contrast, soft objectives guide the multi-objective Pareto solver, allowing the formulator to adjust priority weights "
            "between ingredient cost minimization, nutritional density, and sensory texture scores. "
            "Formulators can seamlessly toggle constraints between hard and soft tiers or fine-tune slider weights "
            "before triggering the numerical optimization solver."
        )
    },
    {
        "id": 6,
        "title": "Stage 4: Pareto Candidate Generation & Deep-Dive Inspection",
        "route": "/dashboard/formulate/guided (Stage 4)",
        "script": (
            "In Stage 4, the platform delivers distinct candidate formulation sets synthesized by our numerical engine. "
            "Under the hood, the backend queries our 23,893-ingredient knowledge base and executes a Sequential Least Squares Programming "
            "algorithm to optimize the recipe subjected to exact mass balance and nutritional target equations. "
            "The system generates three distinct strategic formulation variants: a Cost-Optimized Strategy, a Balanced Performance Strategy, "
            "and a Functionality and Texture-Optimized Strategy. "
            "Opening the Candidate Inspector modal provides complete transparency into the formulated recipe: "
            "Prime Press Cocoa Butter at exactly 25.0% satisfying our brief, high-purity plant protein isolates, "
            "organic chia seeds providing rheological viscosity, fat-free cocoa mass, ammonium phosphatides as an emulsifier, "
            "and natural vanilla flavor systems. "
            "We also inspect the multi-axis performance radar chart evaluating cost, nutrition, stability, and clean-label index "
            "before selecting this candidate set for final reporting."
        )
    },
    {
        "id": 7,
        "title": "Stage 5: Final Formulation Dossier (All 7 Analytical Tabs)",
        "route": "/dashboard/formulate/guided (Stage 5)",
        "script": (
            "Stage 5 presents the complete seven-tab Technical Formulation Dossier — an industrial-grade manufacturing specification. "
            "In Tab 1, Overview, we confirm complete 100.00% mass balance closure, a high feasibility score of 94%, "
            "a water activity of 0.58 guaranteeing shelf-stability without artificial preservatives, and an interactive macronutrient donut chart. "
            "In Tab 2, Ingredients, we examine the complete production recipe with exact percentages, gram allocations, and botanical functional roles. "
            "Tab 3, Process, outlines the pilot-plant manufacturing protocol, detailing high-shear dry blending, fat melting, refining, "
            "conching at 55 degrees Celsius, and controlled tempering curves. "
            "In Tab 4, Cost Analysis, costs are presented directly per individual raw material — avoiding vague category approximations. "
            "Tab 5, Nutrition Profile, displays dynamically calculated values: 495 kilocalories, 47.5 grams of protein, carbohydrates, "
            "and key minerals with zero placeholder values. "
            "Tab 6, Allergens and Compliance, verifies full compliance with FDA 21 CFR and EFSA standards, confirming zero dairy cross-contact risk. "
            "Finally, Tab 7, AI Rationale, details the scientific justification behind each ingredient substitution. "
            "Notice also the pinned stage bar at the top, enabling instant bidirectional navigation across all stages without data loss."
        )
    },
    {
        "id": 8,
        "title": "Knowledge Graph Explorer & Semantic Traversal",
        "route": "/dashboard/knowledge-graph",
        "script": (
            "We now transition to the Knowledge Graph Explorer — the semantic intelligence core powering the platform. "
            "This module maps 23,893 food ingredients connected through complex multi-relational triples, "
            "including functional class memberships, compatibility edges, nutrient relationships, and allergen taxonomies. "
            "Using the interactive force-directed canvas, food scientists can filter node types, inspect ingredient clusters, "
            "and examine bidirectional relationships. "
            "Searching for key functional components such as Pea Protein Isolate or Cocoa Butter reveals rich node metadata, "
            "including chemical identifiers, regulatory GRAS status, and connected replacement nodes. "
            "By adjusting graph traversal depth, researchers can explore ingredient substitution pathways that maintain "
            "emulsion stability and flavor harmony."
        )
    },
    {
        "id": 9,
        "title": "Comprehensive Ingredient Library & Specification Drawer",
        "route": "/dashboard/ingredients",
        "script": (
            "Next, we inspect the Ingredient Library, which provides an exhaustive, searchable repository of all 23,893 cataloged ingredients. "
            "Formulators can search by common name, CAS number, or filter by functional classifications such as "
            "Proteins, Sweeteners, Emulsifiers, Hydrocolloids, and Fats and Oils. "
            "Clicking any ingredient card expands the slide-over specification drawer. "
            "Here, we can inspect verified physicochemical parameters — such as water activity, pH, and solubility — "
            "alongside macro and micronutrient distributions, allergen warnings, and benchmark market pricing. "
            "This grounded database ensures that every formulation synthesized by our AI is immediately reproducible on the factory floor "
            "using real, commercially available ingredients."
        )
    },
    {
        "id": 10,
        "title": "User Profile, Laboratory Settings & Formulation History",
        "route": "/dashboard/profile",
        "script": (
            "In the User Profile and Project History module, researchers and enterprise administrators can manage their scientific workspace. "
            "We observe the logged-in demonstration profile with Expert User privileges, organizational affiliation with the "
            "TCS Food Formulation Laboratory, and comprehensive formulation history logs. "
            "Formulators can review previously archived projects, compare iteration histories, and safely export technical audit dossiers. "
            "The platform enforces strict role-based access control and credential hashing, ensuring proprietary formulation recipes "
            "and intellectual property remain securely compartmentalized."
        )
    },
    {
        "id": 11,
        "title": "Closing Summary & Dashboard Return",
        "route": "/dashboard",
        "script": (
            "Returning to the central command dashboard, we conclude this demonstration of the Food Formulation AI Platform. "
            "By seamlessly integrating natural language brief interpretation, automated constraint extraction, a 23,893-ingredient knowledge graph, "
            "SciPy numerical optimization, and multi-jurisdictional regulatory compliance, the platform transforms food product development "
            "from an empirical trial-and-error cycle into a predictable, mathematically grounded digital science. "
            "Thank you for your time and interest in the Food Formulator platform."
        )
    }
]

async def generate_scene_audio(scene):
    out_path = f"demo_output/scene_{scene['id']:02d}.mp3"
    comm = edge_tts.Communicate(scene["script"], "en-US-ChristopherNeural", rate="-2%")
    await comm.save(out_path)
    # Get duration using ffprobe or ffmpeg
    cmd = [
        FFMPEG_EXE, "-i", out_path,
        "-f", "null", "-"
    ]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    # Find duration: "Duration: 00:01:23.45"
    duration = 0.0
    for line in proc.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            duration = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
            break
    scene["audio_path"] = out_path
    scene["duration"] = duration
    print(f"Scene {scene['id']} ({scene['title']}): {duration:.2f}s")
    return scene

async def main():
    os.makedirs("demo_output", exist_ok=True)
    results = []
    for sc in SCENES:
        res = await generate_scene_audio(sc)
        results.append(res)
    
    # Concatenate all audio files into demo_output/Food_Formulator_Voiceover.mp3
    concat_list_file = "demo_output/audio_concat.txt"
    with open(concat_list_file, "w") as f:
        for sc in results:
            abs_p = os.path.abspath(sc["audio_path"]).replace("\\", "/")
            f.write(f"file '{abs_p}'\n")
            
    out_voiceover = "demo_output/Food_Formulator_Voiceover.mp3"
    cmd_cat = [
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_file, "-c", "copy", out_voiceover
    ]
    subprocess.run(cmd_cat, check=True)
    print("Voiceover concatenated successfully:", out_voiceover)
    
    # Calculate timestamps
    total_time = 0.0
    csv_rows = ["Scene_ID,Scene_Title,Route,Start_Time,End_Time,Duration_Seconds"]
    for sc in results:
        start_fmt = f"{int(total_time // 60):02d}:{int(total_time % 60):02d}"
        end_time = total_time + sc["duration"]
        end_fmt = f"{int(end_time // 60):02d}:{int(end_time % 60):02d}"
        csv_rows.append(f"{sc['id']},\"{sc['title']}\",\"{sc['route']}\",{start_fmt},{end_fmt},{sc['duration']:.2f}")
        sc["start_time"] = total_time
        sc["end_time"] = end_time
        total_time = end_time
        
    csv_path = "demo_output/Food_Formulator_Scene_Timestamps.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("\n".join(csv_rows) + "\n")
    print(f"Timestamps CSV written: {csv_path}, Total Duration: {total_time:.2f}s ({total_time/60:.2f} minutes)")

if __name__ == "__main__":
    asyncio.run(main())

