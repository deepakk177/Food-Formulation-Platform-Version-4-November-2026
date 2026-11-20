import asyncio
import os
import shutil
import subprocess
import numpy as np
from scipy.io import wavfile
import imageio_ffmpeg
import edge_tts

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VOICE = "en-US-JennyNeural"
GLOBAL_RATE = "+23%"
INPUT_VIDEO = r"demo_output\FINAL RECORDING.mp4"
OUTPUT_DIR = "narration_output"
OUTPUT_VIDEO_NAME = "FINAL_RECORDING_WITH_AI_NARRATION.mp4"

SECTIONS_CONFIG = [
    {
        "id": "section_01",
        "title": "Introduction and Home Page Brief",
        "target_start": 0.5,
        "text": (
            "Welcome to our AI-powered Food Formulation Platform, an intelligent environment designed to streamline "
            "food product development through artificial intelligence and structured food science knowledge. On the "
            "home page, product developers can submit natural language briefs to initiate automated formulation workflows."
        )
    },
    {
        "id": "section_02",
        "title": "Exploring an Already-Created Formulation",
        "target_start": 16.5,
        "text": (
            "Instead of going through every intermediate formulation step, we begin by directly opening an already-created "
            "formulation. This provides a simpler starting point for users who want to understand the final product before "
            "exploring the underlying technical process. The user can immediately access the formulation overview and examine "
            "the information associated with the developed product. This approach makes it easier to understand what the "
            "platform produces and how its different modules support food product development.\n\n"
            "Here on the primary dashboard, the platform visualizes core performance indicators, including eight out of eight "
            "satisfied constraints, a ninety-two percent artificial intelligence confidence score, predictable production yields, "
            "and a validated target water activity of zero point five eight. Scrolling down reveals the complete multi-layer "
            "formulation composition, spanning base raw materials, functional emulsifiers, and preservative systems. Product "
            "developers can review batch economics across pilot and commercial scales, direct ingredient cost allocations, and "
            "interconnected unit operations—such as refining limits and conching profiles. Reviewing these process control parameters "
            "confirms tight moisture regulation below eight percent and validated water activity limits to ensure ambient shelf stability."
        )
    },
    {
        "id": "section_03",
        "title": "Ingredient Breakdown and Analytical Modules",
        "target_start": 84.0,
        "text": (
            "Moving into the analytical modules, the platform dissects the formulation across multiple critical quality dimensions. "
            "The ingredient breakdown classifies components by functional role—from prime press cocoa butter forming the lipid continuous "
            "phase, to ammonium phosphatides providing rheological control. Users can inspect exact inclusion percentages, unit costs, "
            "and category taxonomy.\n\n"
            "In the nutrition panel, macronutrient targets are verified against dietary standards, showing balanced caloric distribution "
            "and high protein density. The allergens and compliance module evaluates declared allergens, monitors cross-contact risks, "
            "and cross-checks regulatory claims like low sugar and GSFA additive compliance. Furthermore, the technical dossier consolidates "
            "regulatory documentation, processing specifications, and explainable AI rationales into an exportable record. With the formulation "
            "thoroughly audited across cost, stability, and safety benchmarks, users can transition seamlessly into the guided engine to configure "
            "custom product criteria and parameters. This consolidated technical record provides complete quality assurance before scaling up."
        )
    },
    {
        "id": "section_04",
        "title": "Constraint Discovery and Configuration",
        "target_start": 145.0,
        "text": (
            "Now, we transition into the formulation engine to examine how recipes are synthesized from scratch through constraint "
            "configuration. The platform translates the natural language product brief into an active constraint matrix, categorizing "
            "requirements into strict hard constraints and multi-criteria soft objectives.\n\n"
            "Hard constraints act as non-negotiable feasibility vetoes. For our vegan white chocolate bar, the system enforces a strict "
            "twenty-five percent cocoa butter floor, a twenty-eight percent sugar ceiling, at least seven percent protein, and the absolute "
            "elimination of dairy and animal derivatives to guarantee vegan compliance. Formulations violating any hard constraint are "
            "immediately disqualified.\n\n"
            "In contrast, soft objectives govern optimization targets along the Pareto frontier—balancing sensory texture, creamy melt "
            "kinetics, acoustic snap, and raw material cost minimization. Technologists can interactively toggle constraints between hard "
            "vetoes and soft goals, adjust threshold boundaries, or insert custom compliance rules.\n\n"
            "As the user reviews the active constraints matrix, the system validates mass balance equality and prepares the parameter "
            "space for mathematical optimization. This explicit constraint hierarchy ensures that every candidate generated strictly "
            "satisfies safety and regulatory bounds while targeting peak sensory performance. The structured matrix eliminates ambiguity, "
            "allowing algorithmic solvers to explore only commercially and biochemically feasible ingredient spaces for industrial production. "
            "These dynamic constraint boundaries ensure rigorous formulation precision and factory reproducibility."
        )
    },
    {
        "id": "section_05",
        "title": "Candidate Generation and Texture Strategy Inspection",
        "target_start": 230.0,
        "text": (
            "With constraints established, the platform initiates candidate generation. Rather than relying on empirical trial-and-error, "
            "the engine explores eligible ingredient spaces and applies sequential least squares programming—or SLSQP optimization—alongside "
            "Pareto-based frontier evaluation.\n\n"
            "Pareto scoring evaluates competing formulation criteria simultaneously, isolating non-dominated alternatives where improving "
            "nutritional density does not compromise cost or physical texture. The system groups the highest-scoring recipes into four "
            "specialized archetypes: Functionality and Texture, Balanced Pareto, Nutrition-Maximized, and Cost-Optimized.\n\n"
            "Opening the inspector for Candidate Set C—which achieved the top Pareto rank with an overall score of eighty-three point eight "
            "percent—reveals its underlying formulation rationale. This recipe optimizes the continuous lipid phase and emulsifier synergy "
            "to maximize sensory mouthfeel and bloom resistance.\n\n"
            "The mathematical solver card explicitly confirms exact one-hundred percent mass balance and water activity below zero point "
            "five eight. Transparent trade-off analytics notify formulators that the higher lipid fraction requires disciplined temper "
            "crystallization control to guarantee acoustic snap and shelf stability. The underlying solver maximizes emulsifier synergy "
            "and lipid crystal fractions under strict mass balance, ensuring optimal mouthfeel and zero phase separation. Formulators gain "
            "complete insight into algorithmic objective weights, thermodynamic feasibility, and ingredient synergy before advancing to selection, "
            "guaranteeing factory reproducibility. This transparent solver convergence provides complete scientific explainability across all matrix fractions."
        )
    },
    {
        "id": "section_06",
        "title": "Multi-Candidate Comparison and Trade-Off Analysis",
        "target_start": 320.0,
        "text": (
            "Closing the modal, we transition into the comparative analysis view. Here, developers can benchmark candidate formulations "
            "side by side along the Pareto frontier.\n\n"
            "The Nutrition-Maximized candidate achieves an impressive forty-five grams of protein per serving using dense plant isolates, "
            "but incurs a higher ingredient cost of thirteen dollars and six cents per kilogram. In contrast, the Cost-Optimized candidate "
            "reduces unit cost to ten dollars and two cents while maintaining baseline functional standards. The Balanced set strikes an "
            "optimal commercial middle ground, while the Functionality set delivers premium structural integrity.\n\n"
            "By presenting multi-dimensional trade-offs transparently, the platform eliminates guesswork, enabling cross-functional teams "
            "from R and D, procurement, and brand management to select the winning formula collaboratively. This multi-objective trade-off "
            "analysis empowers teams to choose the exact balance of nutritional potency, sensory indulgence, and ingredient cost that fits "
            "their go-to-market strategy, confirming feasibility across all manufacturing, sensory, and economic criteria. Cross-functional teams can align on commercial launch strategies with total confidence."
        )
    },
    {
        "id": "section_07",
        "title": "Final Formulation Report and Process Specifications",
        "target_start": 380.0,
        "text": (
            "Selecting Candidate Set C generates the comprehensive final formulation report. This dossier serves as the master technical "
            "specification for manufacturing handover.\n\n"
            "The report details exact ingredient inclusion percentages, scaled batch weights for pilot and commercial runs, and pre-calculated "
            "nutritional facts. Crucially, formulation components are linked directly to unit manufacturing operations. It prescribes "
            "mechanical particle refining below twenty-five microns, a forty-five degree Celsius conching cycle to disperse the fat phase, "
            "and precision seed tempering to induce form five polymorphic crystallization.\n\n"
            "Critical quality parameters—including a certified water activity of zero point five eight and a twelve-month ambient antioxidant "
            "stability pass—are validated upfront. Automated batch economics project cost per kilogram and yield across production volumes, "
            "establishing clear commercial viability before factory scheduling and pilot trial execution. This end-to-end documentation "
            "accelerates the transition from laboratory prototype to commercial line production without costly formulation rework, batch "
            "failures, or manufacturing delays. The complete technical dossier provides manufacturing teams with an immediate execution roadmap."
        )
    },
    {
        "id": "section_08",
        "title": "Ingredient Library and Scientific Dossiers",
        "target_start": 445.0,
        "text": (
            "Beyond project-specific workflows, the platform provides dedicated scientific knowledge tools. Navigating to the Ingredient "
            "Library opens a centralized repository of verified food raw materials, functional properties, and regulatory profiles.\n\n"
            "Formulators can filter ingredients by functional category, allergen exclusions, or specific dietary claims. Opening an ingredient "
            "specification—such as Rare Sugar Allulose—displays comprehensive biochemical and regulatory metadata, including its official "
            "FDA GRAS notice number, near-zero caloric impact, and glycemic index profile.\n\n"
            "The library connects directly to the underlying Knowledge Graph, displaying localized subgraphs of functional interactions and "
            "clean-label substitution candidates. Visualizing this localized knowledge graph subgraph uncovers direct linkages between allulose, "
            "sweetness equivalence, and clean-label dietary compliance, empowering formulators to explore substitutions with complete confidence. "
            "This structured repository bridges ingredient procurement with biochemical science, ensuring consistent quality, regulatory compliance, "
            "and predictable functionality across global ingredient supply chains."
        )
    },
    {
        "id": "section_09",
        "title": "Knowledge Graph Exploration and Reasoning Chains",
        "target_start": 510.0,
        "text": (
            "At the technological core of the platform is its Knowledge Graph—an ontology-driven semantic network that models food science "
            "relationships far beyond the limits of conventional databases.\n\n"
            "Rather than treating ingredients as isolated table records, the graph connects entities across multiple semantic layers—spanning "
            "raw agricultural inputs, functional molecules, physicochemical properties, sensory descriptors, processing unit operations, "
            "and regulatory standards.\n\n"
            "Selecting an ingredient like Pea Protein Isolate visualizes its immediate semantic neighborhood. The system displays an "
            "explainable AI reasoning chain, demonstrating how an eighty percent protein concentration satisfies high-protein targets, "
            "provides functional emulsification and water binding, and fulfills non-GMO, clean-label safety constraints.\n\n"
            "Formulators can dynamically adjust traversal depth to inspect higher-order relationships or switch between force-directed and "
            "concentric circle layouts. Traversal reveals critical manufacturing interactions—such as how thermal pasteurization at eighty-five "
            "degrees Celsius and twelve hundred RPM shear affects protein denaturation kinetics, emulsion stability, and volatile flavor "
            "retention.\n\n"
            "Switching to the concentric circles layout isolates the Thermal Pasteurized process node. Here, operational controls are "
            "quantified at eighty-five degrees Celsius with high-shear mixing at twelve hundred RPM. The graph dynamically maps how these "
            "thermal processing conditions interact with protein denaturation kinetics, lipid crystal polymorphism, and sensory shelf "
            "stability. By querying these structured semantic paths across allergens, processing constraints, and functional behaviors, the "
            "Knowledge Graph transforms raw food science into actionable engineering intelligence, ensuring every AI formulation is rigorously "
            "grounded in verifiable biochemical reality. Formulators can interactively filter by claims, nutrient thresholds, or process parameters, "
            "gaining full explainability into complex ingredient synergies.\n\n"
            "This continuous semantic reasoning ensures that formulations are not only mathematically optimal on paper, but also physically stable "
            "and manufacturable under real-world processing conditions. By unifying food informatics with mechanistic modeling, the Knowledge "
            "Graph empowers developers to de-risk recipes before entering pilot plant trials, connecting molecular properties directly to final "
            "product quality. This predictive intelligence guarantees manufacturing success."
        )
    },
    {
        "id": "section_10",
        "title": "Enterprise Synthesis and Conclusion",
        "target_start": 644.0,
        "text": (
            "In conclusion, the Food Formulation Platform delivers an end-to-end intelligent environment for modern food product development. "
            "By integrating natural language brief interpretation, instant formulation auditing, constraint-driven mathematical optimization, "
            "and Knowledge Graph semantic reasoning, the platform empowers food scientists to innovate faster and with greater scientific "
            "certainty.\n\n"
            "From initial concept and feasibility checks to final pilot-ready technical dossiers, computational formulation transforms weeks "
            "of trial-and-error into minutes of data-driven design. It provides multidisciplinary teams with the speed, precision, and "
            "regulatory assurance needed to bring superior food products to market efficiently. Thank you for watching our demonstration."
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

async def generate_audio_file(sec, out_mp3):
    c = edge_tts.Communicate(sec["text"], voice=VOICE, rate=GLOBAL_RATE)
    sub_cues = []
    audio_data = bytearray()
    
    async for chunk in c.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            s_start = chunk["offset"] / 10_000_000.0
            s_dur = chunk["duration"] / 10_000_000.0
            sub_cues.append({
                "rel_start": s_start,
                "rel_end": s_start + s_dur,
                "text": chunk["text"].strip()
            })
            
    with open(out_mp3, "wb") as f:
        f.write(audio_data)
        
    return sub_cues

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

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    video_dur = get_audio_duration(INPUT_VIDEO)
    print(f"[Init] Input video: {INPUT_VIDEO} (Duration: {video_dur:.2f}s)")
    
    # 1. Generate individual MP3 files and WAV files
    durations = []
    all_raw_cues = []
    for i, sec in enumerate(SECTIONS_CONFIG):
        mp3_path = os.path.join(OUTPUT_DIR, f"{sec['id']}.mp3")
        wav_path = os.path.join(OUTPUT_DIR, f"{sec['id']}.wav")
        cues = await generate_audio_file(sec, mp3_path)
        convert_mp3_to_wav(mp3_path, wav_path)
        dur = get_audio_duration(wav_path)
        durations.append(dur)
        all_raw_cues.append(cues)
        words = len(sec["text"].split())
        wpm = (words / (dur / 60.0)) if dur > 0 else 0
        print(f"Generated {sec['id']}: dur={dur:.2f}s, words={words}, WPM={wpm:.1f}")

    # 2. Compute dynamic start times with STRICT pause limit <= 2.8s and no end cut-off
    start_times = []
    end_times = []
    pauses = []

    for i in range(len(SECTIONS_CONFIG)):
        if i == 0:
            s_time = SECTIONS_CONFIG[0]["target_start"]
        elif i == 1:
            s_time = 16.5
        else:
            prev_end = end_times[i-1]
            target = SECTIONS_CONFIG[i]["target_start"]
            gap = target - prev_end
            if gap > 2.5:
                s_time = prev_end + 1.8
            elif gap < 1.0:
                s_time = prev_end + 1.5
            else:
                s_time = target
        
        dur = durations[i]
        e_time = s_time + dur
        start_times.append(s_time)
        end_times.append(e_time)
        
        if i > 0:
            pause = s_time - end_times[i-1]
            pauses.append(pause)

    # Print verification breakdown
    print("\n" + "="*80)
    print("CONTINUOUS TIMELINE AUDIT (STRICT PAUSE <= 2.8s GUARANTEE)")
    print("="*80)
    all_cues_srt = []
    cue_idx = 1
    
    for i, sec in enumerate(SECTIONS_CONFIG):
        sec_start = start_times[i]
        sec_dur = durations[i]
        sec_end = end_times[i]
        next_start = start_times[i+1] if i + 1 < len(SECTIONS_CONFIG) else video_dur
        pause_to_next = next_start - sec_end
        words = len(sec["text"].split())
        wpm = (words / (sec_dur / 60.0))
        
        print(f"[{sec['id']}] {sec['title'][:30]:<30} | Start: {sec_start:5.1f}s | Dur: {sec_dur:5.2f}s | End: {sec_end:5.1f}s | Next: {next_start:5.1f}s | Pause: {pause_to_next:4.1f}s | Words: {words:3d} | WPM: {wpm:5.1f}")
        
        for c in all_raw_cues[i]:
            cue_start = sec_start + c["rel_start"]
            cue_end = sec_start + c["rel_end"]
            if cue_end > sec_end:
                cue_end = sec_end
            all_cues_srt.append({
                "index": cue_idx,
                "start": cue_start,
                "end": cue_end,
                "text": c["text"]
            })
            cue_idx += 1

    total_spoken = sum(durations)
    total_words = sum(len(s["text"].split()) for s in SECTIONS_CONFIG)
    avg_wpm = total_words / (total_spoken / 60.0)
    print("\n" + "-"*80)
    print(f"[Summary] Total Words: {total_words} | Spoken Duration: {total_spoken:.2f}s ({total_spoken/video_dur*100:.1f}% coverage) | Average WPM: {avg_wpm:.1f} WPM")
    print(f"[Check] Pause range between all sections: Min {min(pauses):.2f}s, Max {max(pauses):.2f}s (All strictly <= 3.0s: {all(p <= 3.0 for p in pauses)})")
    print("="*80 + "\n")

    # 3. Assemble full master audio in numpy array
    sample_rate = 44100
    total_samples = int(np.ceil(video_dur * sample_rate))
    master_audio = np.zeros((total_samples, 2), dtype=np.float32)

    for i, sec in enumerate(SECTIONS_CONFIG):
        wav_path = os.path.join(OUTPUT_DIR, f"{sec['id']}.wav")
        sr, data = wavfile.read(wav_path)
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
        elif data.dtype == np.int32:
            data = data.astype(np.float32) / 2147483648.0
        if len(data.shape) == 1:
            data = np.column_stack([data, data])
            
        start_sample = int(start_times[i] * sample_rate)
        end_sample = min(start_sample + len(data), total_samples)
        samples_to_copy = end_sample - start_sample
        master_audio[start_sample:end_sample] += data[:samples_to_copy]

    # Normalize audio to -1.5 dBFS
    peak = np.max(np.abs(master_audio))
    target_peak = 10.0 ** (-1.5 / 20.0)  # ~0.8414
    if peak > 0:
        master_audio = (master_audio / peak) * target_peak
        
    master_int16 = np.clip(master_audio * 32767.0, -32768, 32767).astype(np.int16)
    master_wav_path = os.path.join(OUTPUT_DIR, "narration_full.wav")
    wavfile.write(master_wav_path, sample_rate, master_int16)
    
    # Convert master WAV to MP3
    master_mp3_path = os.path.join(OUTPUT_DIR, "narration_full.mp3")
    cmd_mp3 = [
        FFMPEG, "-y", "-i", master_wav_path,
        "-b:a", "256k", master_mp3_path
    ]
    subprocess.run(cmd_mp3, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[Export] Saved {master_mp3_path}")

    # 4. Save script text file
    script_txt_path = os.path.join(OUTPUT_DIR, "narration_script.txt")
    with open(script_txt_path, "w", encoding="utf-8") as f:
        f.write("# Master Narration Script - Food Formulation Platform\n")
        f.write(f"# Voice: {VOICE} | Speed: {GLOBAL_RATE} (~155 WPM) | Max Pause <= 2.8s\n\n")
        for i, sec in enumerate(SECTIONS_CONFIG):
            f.write(f"## [{sec['id']}] {sec['title']} ({format_srt_time(start_times[i])} --> {format_srt_time(end_times[i])})\n\n")
            f.write(sec["text"] + "\n\n")
    print(f"[Script] Saved {script_txt_path}")

    # 5. Save SRT subtitles file
    srt_path = os.path.join(OUTPUT_DIR, "narration_subtitles.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        for cue in all_cues_srt:
            f.write(f"{cue['index']}\n")
            f.write(f"{format_srt_time(cue['start'])} --> {format_srt_time(cue['end'])}\n")
            f.write(f"{cue['text']}\n\n")
    print(f"[Export] Saved {srt_path} with {len(all_cues_srt)} subtitle cues")

    # 6. Multiplex into final MP4 video
    out_video_path = os.path.join(OUTPUT_DIR, OUTPUT_VIDEO_NAME)
    print(f"[Mux] Multiplexing video with continuous American female narration into {out_video_path}...")
    cmd_mux = [
        FFMPEG, "-y",
        "-i", INPUT_VIDEO,
        "-i", master_mp3_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        out_video_path
    ]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[Mux] Final video created successfully: {out_video_path}")

    # Mirror to demo_output
    demo_dest = os.path.join("demo_output", OUTPUT_VIDEO_NAME)
    shutil.copy2(out_video_path, demo_dest)
    print(f"[Copy] Synced to {demo_dest}")

if __name__ == "__main__":
    asyncio.run(main())
