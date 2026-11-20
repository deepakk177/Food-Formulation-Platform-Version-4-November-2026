import asyncio
import os
import shutil
import subprocess
import numpy as np
from scipy.io import wavfile
import imageio_ffmpeg
import edge_tts

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VOICE = "en-IN-PrabhatNeural"

# Target ~160 words per minute
GLOBAL_RATE = "+50%"
INPUT_VIDEO = r"demo_output\FINAL RECORDING.mp4"
OUTPUT_DIR = "narration_output"
OUTPUT_VIDEO_NAME = "FINAL_RECORDING_WITH_AI_NARRATION.mp4"

SECTIONS_CONFIG = [
    {
        "id": "section_01",
        "title": "Introduction and Home Page Brief",
        "start_sec": 0.2,
        "end_slot_sec": 16.0,
        "rate": "+50%",
        "text": (
            "Welcome to our AI-powered Food Formulation Platform, designed to streamline food product development "
            "through artificial intelligence and structured food science knowledge. On the home page, users can submit "
            "product briefs in natural language to initiate intelligent formulation workflows."
        )
    },
    {
        "id": "section_02",
        "title": "Exploring an Already-Created Formulation",
        "start_sec": 16.5,
        "end_slot_sec": 85.0,
        "rate": "+50%",
        "text": (
            "Instead of going through every intermediate formulation step, we begin by directly opening an already-created "
            "formulation. This provides a simpler starting point for users who want to understand the final product before "
            "exploring the underlying technical process. The user can immediately access the formulation overview and examine "
            "the information associated with the developed product. This approach makes it easier to understand what the "
            "platform produces and how its different modules support food product development.\n\n"
            "In this overview, the system presents key performance indicators including eight out of eight satisfied constraints, "
            "a ninety-two percent AI confidence score, calculated yield, batch unit economics, and target water activity of zero "
            "point five eight. Users can inspect the full multi-layer formulation composition, process control parameters such "
            "as conching temperature and mixing speed, and direct cost breakdowns. The technical dossier view and interactive "
            "nutrition profile provide an immediate, multidimensional assessment of product viability before any physical "
            "bench trials begin."
        )
    },
    {
        "id": "section_03",
        "title": "Ingredient List and Analytical Modules",
        "start_sec": 85.5,
        "end_slot_sec": 145.0,
        "rate": "+50%",
        "text": (
            "Here, we explore the generated formulation in deeper detail through its ingredient composition and dedicated analytical "
            "modules. The ingredient list categorizes components into functional roles—such as prime press cocoa butter for the lipid "
            "matrix, soy protein isolate for protein enrichment, and ammonium phosphatides for rheological stability. Alongside the "
            "ingredients, the platform provides specialized analytical views: the nutrition profile verifies macronutrient targets against "
            "regulatory benchmarks; the cost analysis provides unit price and batch share modeling; and the allergens and compliance module "
            "evaluates declared allergens and cross-contact risks while auditing claims like high protein, low sugar, and GSFA additive standards.\n\n"
            "Furthermore, the technical dossier consolidates regulatory documentation, processing guidelines, and explainable AI insights. "
            "This comprehensive transparency enables food technologists and QA managers to audit ingredient interactions, justify "
            "formulation decisions, and accelerate commercial readiness."
        )
    },
    {
        "id": "section_04",
        "title": "Constraint Discovery and Configuration",
        "start_sec": 145.5,
        "end_slot_sec": 230.0,
        "rate": "+50%",
        "text": (
            "Now, we transition into the formulation engine to see how these recipes are generated from scratch through constraint "
            "configuration. The platform translates the natural language product brief into a structured constraint graph, categorizing "
            "requirements into strict hard constraints and multi-criteria soft objectives. Hard constraints act as non-negotiable feasibility "
            "vetoes—here enforcing a minimum of twenty-five percent cocoa butter, a strict ceiling of twenty-eight percent sugar, at least "
            "seven percent protein, and the absolute exclusion of dairy and animal derivatives to guarantee vegan compliance.\n\n"
            "In contrast, soft objectives govern optimization targets—including sensory texture, creamy melt kinetics, vanilla-cocoa flavor "
            "balance, and ingredient cost minimization. Users can dynamically fine-tune these parameters, promote or demote boundaries "
            "between hard vetoes and soft targets, or add custom regulatory limits. As the active constraint matrix verifies mass balance "
            "equality, the platform establishes the mathematical boundaries that govern candidate exploration."
        )
    },
    {
        "id": "section_05",
        "title": "Candidate Generation and Texture Strategy Set",
        "start_sec": 230.5,
        "end_slot_sec": 320.0,
        "rate": "+50%",
        "text": (
            "Once constraints are set, the platform executes candidate generation. Rather than relying on trial-and-error, the engine "
            "explores eligible ingredient spaces and applies sequential least squares programming—or SLSQP optimization—alongside Pareto-based "
            "frontier evaluation. Instead of collapsing competing criteria into an arbitrary single score, Pareto optimization identifies "
            "non-dominated solutions where improving one metric—such as protein content—does not unacceptably degrade cost or texture.\n\n"
            "The engine shortlists candidates into four specialized strategic archetypes: Functionality and Texture, Balanced Pareto, "
            "Nutrition-Maximized, and Cost-Optimized. Here, we inspect Candidate Set C, which achieved the top Pareto rank with an overall "
            "score of eighty-three point eight percent. This strategy maximizes emulsion stability, lipid crystal networks, and sensory "
            "mouthfeel. The modal details the mathematical solver parameters, enforcing exact one-hundred percent mass balance and water "
            "activity below zero point five eight, while explicitly outlining trade-offs—such as requiring disciplined temper crystallization "
            "to guarantee acoustic snap and long-term shelf stability."
        )
    },
    {
        "id": "section_06",
        "title": "Candidate Comparison and Trade-Off Analysis",
        "start_sec": 320.5,
        "end_slot_sec": 380.0,
        "rate": "+50%",
        "text": (
            "After examining individual sets, users enter the multi-candidate comparison view. Each candidate archetype represents a "
            "mathematically rigorous compromise along the Pareto frontier. The Nutrition-Maximized set pushes protein density to forty-five "
            "grams using premium isolates, while the Cost-Optimized formulation reduces raw material expenditure to ten dollars and two cents "
            "per kilogram. The Balanced set harmonizes sensory indulgence with clean-label compliance, and the Functionality set optimizes "
            "structural integrity.\n\n"
            "This comparative layout allows product developers and commercial stakeholders to evaluate formulations across nutritional "
            "yields, ingredient counts, and cost impacts simultaneously. By making trade-offs explicit, the platform eliminates guesswork, "
            "empowering teams to select the candidate that best aligns with their production capabilities and brand positioning."
        )
    },
    {
        "id": "section_07",
        "title": "Final Formulation Results and Specifications",
        "start_sec": 380.5,
        "end_slot_sec": 445.0,
        "rate": "+50%",
        "text": (
            "Upon selecting the preferred candidate, the platform generates the comprehensive final formulation report. This document details "
            "the exact recipe specification, percentage weight inclusions, and scaled batch calculations across pilot and production volumes. "
            "It links formulation components directly to unit operations—specifying particle refining below twenty-five microns, conching "
            "temperature profiles at forty-five degrees Celsius, and precision seed tempering conditions to establish the stable form five cocoa "
            "butter polymorphic crystal network.\n\n"
            "In addition, quality assurance parameters—such as a validated water activity of zero point five eight, pH of six point two, and "
            "antioxidant stability profiles—are pre-calculated to ensure twelve months of ambient shelf life. This actionable specification "
            "bridges the gap between digital formulation and factory-floor execution, providing bench scientists and manufacturing engineers "
            "with everything required to begin production trials immediately."
        )
    },
    {
        "id": "section_08",
        "title": "Ingredient Library and Scientific Specifications",
        "start_sec": 445.5,
        "end_slot_sec": 510.0,
        "rate": "+50%",
        "text": (
            "Next, we navigate to the Ingredient Library, a central repository of verified food raw materials, nutritional profiles, and "
            "regulatory metadata. Users can search and filter across functional classes—such as alternative sweeteners, plant proteins, lipids, "
            "and texturizers. Each ingredient card provides immediate visibility into market unit pricing, declared allergens, and regulatory clearances.\n\n"
            "Opening an ingredient like Rare Sugar Allulose reveals comprehensive scientific specifications—including its FDA GRAS notice number, "
            "caloric contribution of zero point two calories per gram, glycemic index, and functional sweetening equivalency. Crucially, the library "
            "integrates directly with the platform's Knowledge Graph, visualizing connected subgraphs that display associated physiological "
            "functions, recommended processing temperatures, and synergistic ingredient pairs. This empowers formulators to discover novel raw "
            "materials and explore substitutions with complete scientific and regulatory confidence."
        )
    },
    {
        "id": "section_09",
        "title": "Knowledge Graph Exploration and Reasoning Chains",
        "start_sec": 510.5,
        "end_slot_sec": 645.0,
        "rate": "+50%",
        "text": (
            "At the technological core of the platform is its Knowledge Graph, an ontology-driven semantic network that models food science "
            "relationships beyond traditional tabular databases. Rather than treating ingredients as isolated rows, the graph connects entities "
            "across multiple semantic layers—including raw ingredients, molecular nutrients, physicochemical properties, sensory attributes, "
            "food processing operations, and regulatory claims.\n\n"
            "Selecting an ingredient such as Pea Protein Isolate visualizes its immediate semantic neighborhood. The platform surfaces an "
            "explainable AI reasoning chain—tracing how an eighty percent protein density fulfills nutritional thresholds, maps to emulsifying "
            "and water-binding functional roles, and satisfies clean-label, non-GMO constraints. Formulators can adjust graph traversal depth "
            "from direct connections to second- and third-order interactions.\n\n"
            "Switching to the concentric circle and topological layouts reveals deeper cross-domain interactions. For instance, inspecting "
            "the Thermal Pasteurized process node highlights critical operational parameters, including an eighty-five degree Celsius heating "
            "profile and high-shear mixing at twelve hundred RPM. The graph dynamically maps how these thermal processing conditions interact "
            "with protein denaturation kinetics, lipid crystal polymorphism, and sensory shelf stability.\n\n"
            "By querying semantic paths across allergens, processing constraints, and functional behaviors, the Knowledge Graph transforms "
            "raw food data into actionable engineering intelligence, ensuring every AI formulation is rigorously grounded in biochemical reality."
        )
    },
    {
        "id": "section_10",
        "title": "Platform Conclusion and Summary",
        "start_sec": 645.5,
        "end_slot_sec": 687.0,
        "rate": "+50%",
        "text": (
            "In summary, the Food Formulation Platform unites natural language brief comprehension, instant dossier inspection, constraint-guided "
            "optimization, Pareto frontier discovery, and ontology-driven Knowledge Graph intelligence into a unified enterprise solution. "
            "By replacing manual trial-and-error with explainable AI and rigorous mathematical solvers, the platform significantly reduces "
            "formulation cycle times, guarantees compliance, and accelerates commercial food innovation from concept to factory shelf. "
            "Thank you for watching."
        )
    }
]

def format_srt_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        millis = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

async def generate_section(sec, out_mp3):
    rate_to_use = sec.get("rate", GLOBAL_RATE)
    c = edge_tts.Communicate(sec["text"], voice=VOICE, rate=rate_to_use)
    subtitles = []
    audio_data = bytearray()
    
    async for chunk in c.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            s_start = chunk["offset"] / 10_000_000.0
            s_dur = chunk["duration"] / 10_000_000.0
            subtitles.append({
                "start": sec["start_sec"] + s_start,
                "end": sec["start_sec"] + s_start + s_dur,
                "text": chunk["text"].strip()
            })
            
    with open(out_mp3, "wb") as f:
        f.write(audio_data)
        
    return subtitles

def convert_mp3_to_wav(mp3_path, wav_path):
    cmd = [
        FFMPEG, "-y", "-i", mp3_path,
        "-ar", "44100", "-ac", "2", "-f", "wav",
        wav_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def get_audio_duration(path):
    cmd = [FFMPEG, "-i", path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    return 0.0

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    temp_dir = os.path.join(OUTPUT_DIR, "temp_audio")
    os.makedirs(temp_dir, exist_ok=True)
    
    video_dur = get_audio_duration(INPUT_VIDEO)
    print(f"[Init] Input video: {INPUT_VIDEO} (Duration: {video_dur:.2f}s)")
    
    fs = 44100
    total_samples = int(np.ceil(video_dur * fs))
    master_narration = np.zeros((total_samples, 2), dtype=np.float32)
    all_subtitles = []
    
    # Save script to narration_script.txt
    script_txt_path = os.path.join(OUTPUT_DIR, "narration_script.txt")
    with open(script_txt_path, "w", encoding="utf-8") as f:
        f.write("FOOD FORMULATION PLATFORM - PROFESSIONAL DEMONSTRATION NARRATION SCRIPT (~160 WPM)\n")
        f.write("Voice: Indian English (Male) | Speaking Rate: ~160 WPM | Video: FINAL RECORDING.mp4\n")
        f.write("=" * 85 + "\n\n")
        for idx, sec in enumerate(SECTIONS_CONFIG, 1):
            start_m, start_s = int(sec["start_sec"] // 60), int(sec["start_sec"] % 60)
            end_m, end_s = int(sec["end_slot_sec"] // 60), int(sec["end_slot_sec"] % 60)
            f.write(f"Section {idx:02d}: {sec['title']} ({start_m:02d}:{start_s:02d}–{end_m:02d}:{end_s:02d})\n")
            f.write("-" * 85 + "\n")
            f.write(sec["text"].strip() + "\n\n")
    print(f"[Script] Saved {script_txt_path}")

    # Generate each section audio and compute exact WPM
    total_words = 0
    total_speech_sec = 0.0
    
    for sec in SECTIONS_CONFIG:
        out_mp3 = os.path.join(OUTPUT_DIR, f"{sec['id']}.mp3")
        subs = await generate_section(sec, out_mp3)
        all_subtitles.extend(subs)
        
        temp_wav = os.path.join(temp_dir, f"{sec['id']}.wav")
        convert_mp3_to_wav(out_mp3, temp_wav)
        
        _, data = wavfile.read(temp_wav)
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
            
        dur = len(data) / fs
        words = len(sec["text"].split())
        wpm = (words / dur) * 60
        total_words += words
        total_speech_sec += dur
        
        start_samp = int(sec["start_sec"] * fs)
        end_samp = start_samp + len(data)
        if end_samp > total_samples:
            data = data[:total_samples - start_samp]
            end_samp = total_samples
            
        master_narration[start_samp:end_samp] += data
        
        slot_span = sec["end_slot_sec"] - sec["start_sec"]
        pause_after = slot_span - dur
        print(f"[{sec['id']}] {sec['title'][:32]:32s} | Start: {sec['start_sec']:5.1f}s | Dur: {dur:5.2f}s | Words: {words:3d} | WPM: {wpm:5.1f} | Pause: {pause_after:4.1f}s")

    overall_wpm = (total_words / total_speech_sec) * 60
    print(f"\n[Summary] Total Words: {total_words} | Total Spoken Duration: {total_speech_sec:.2f}s | Overall Average WPM: {overall_wpm:.1f} WPM")
    
    # Peak normalization to -1.5 dBFS
    max_val = np.max(np.abs(master_narration))
    if max_val > 0.84:
        master_narration = (master_narration / max_val) * 0.84
    elif max_val > 0 and max_val < 0.70:
        master_narration = (master_narration / max_val) * 0.84
        
    master_wav = os.path.join(OUTPUT_DIR, "narration_master.wav")
    final_int16 = (master_narration * 32767).astype(np.int16)
    wavfile.write(master_wav, fs, final_int16)
    
    # Export narration_full.mp3 (high quality 256k)
    full_mp3 = os.path.join(OUTPUT_DIR, "narration_full.mp3")
    cmd_mp3 = [
        FFMPEG, "-y", "-i", master_wav,
        "-c:a", "libmp3lame", "-b:a", "256k",
        full_mp3
    ]
    subprocess.run(cmd_mp3, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[Export] Saved {full_mp3}")
    
    # Export narration_subtitles.srt
    srt_path = os.path.join(OUTPUT_DIR, "narration_subtitles.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, sub in enumerate(all_subtitles, 1):
            f.write(f"{idx}\n")
            f.write(f"{format_srt_time(sub['start'])} --> {format_srt_time(sub['end'])}\n")
            f.write(f"{sub['text']}\n\n")
    print(f"[Export] Saved {srt_path} with {len(all_subtitles)} subtitle cues")
    
    # Multiplex final video
    out_mp4 = os.path.join(OUTPUT_DIR, OUTPUT_VIDEO_NAME)
    print(f"[Mux] Multiplexing video with enriched 160 WPM narration into {out_mp4}...")
    cmd_mux = [
        FFMPEG, "-y",
        "-i", INPUT_VIDEO,
        "-i", master_wav,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        out_mp4
    ]
    subprocess.run(cmd_mux, check=True)
    print(f"[Mux] Final video created successfully: {out_mp4}")
    
    # Also copy to demo_output for convenience
    demo_out_mp4 = os.path.join("demo_output", OUTPUT_VIDEO_NAME)
    shutil.copy2(out_mp4, demo_out_mp4)
    print(f"[Copy] Synced to {demo_out_mp4}")
    
    # Clean up temp
    shutil.rmtree(temp_dir, ignore_errors=True)
    if os.path.exists(master_wav):
        os.remove(master_wav)
        
    print("\n=== ALL CONTINUOUS 160 WPM DELIVERABLES GENERATED IN narration_output/ ===")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        size_mb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / (1024 * 1024)
        print(f" - {f} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    asyncio.run(main())
