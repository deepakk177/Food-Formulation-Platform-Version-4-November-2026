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

# Speaking rate calibrated to ~160 WPM for en-US-JennyNeural
GLOBAL_RATE = "+23%"
INPUT_VIDEO = r"demo_output\FINAL RECORDING.mp4"
OUTPUT_DIR = "narration_output"
OUTPUT_VIDEO_NAME = "FINAL_RECORDING_WITH_AI_NARRATION.mp4"

SECTIONS_CONFIG = [
    {
        "id": "section_01",
        "title": "Introduction and Home Page Brief",
        "start_sec": 0.5,
        "rate": "+23%",
        "text": (
            "Welcome to our AI-powered Food Formulation Platform, an intelligent environment designed to streamline "
            "food product development through artificial intelligence and structured food science knowledge. On the "
            "home page, product developers can submit natural language briefs to initiate automated formulation workflows."
        )
    },
    {
        "id": "section_02",
        "title": "Exploring an Already-Created Formulation",
        "start_sec": 16.5,
        "rate": "+23%",
        "text": (
            "Instead of going through every intermediate formulation step, we begin by directly opening an already-created "
            "formulation. This provides a simpler starting point for users who want to understand the final product before "
            "exploring the underlying technical process. The user can immediately access the formulation overview and examine "
            "the information associated with the developed product. This approach makes it easier to understand what the "
            "platform produces and how its different modules support food product development.\n\n"
            "Here on the dashboard, the system displays vital performance metrics, including eight out of eight satisfied "
            "constraints, a ninety-two percent AI confidence score, predictable production yields, and target water activity "
            "of zero point five eight. Scrolling down reveals the multi-layer composition across raw materials and emulsifiers, "
            "batch economics from pilot to full scale, and linked unit operations—such as conching temperature profiles and "
            "shear rates. This transparent architecture gives product developers immediate, audit-ready confidence in the formulation."
        )
    },
    {
        "id": "section_03",
        "title": "Ingredient Breakdown and Analytical Modules",
        "start_sec": 83.5,
        "rate": "+23%",
        "text": (
            "Moving into the analytical modules, the platform dissects the formulation across multiple critical quality dimensions. "
            "The ingredient breakdown classifies components by functional role—from prime press cocoa butter forming the lipid continuous "
            "phase, to ammonium phosphatides providing rheological control.\n\n"
            "In the nutrition panel, macronutrient targets are verified against dietary standards, showing balanced caloric distribution "
            "and high protein density. The allergens and compliance module evaluates declared allergens, monitors cross-contact risks, "
            "and cross-checks regulatory claims like low sugar and GSFA additive compliance. Furthermore, the technical dossier consolidates "
            "regulatory documentation, processing specifications, and explainable AI rationales into an exportable record. This bridges "
            "scientific R and D with operational compliance, ensuring every formulation is production-ready."
        )
    },
    {
        "id": "section_04",
        "title": "Constraint Discovery and Configuration",
        "start_sec": 144.0,
        "rate": "+23%",
        "text": (
            "Next, we enter the guided formulation engine to explore how new recipes are synthesized from scratch. The platform translates "
            "the natural language product brief into a structured constraint model, distinguishing between strict hard constraints and "
            "multi-criteria soft objectives.\n\n"
            "Hard constraints serve as non-negotiable feasibility vetoes. For our vegan white chocolate bar, the system enforces a strict "
            "twenty-five percent cocoa butter floor, a twenty-eight percent sugar ceiling, at least seven percent protein, and the absolute "
            "elimination of dairy and animal derivatives. Formulations violating any hard constraint are immediately disqualified.\n\n"
            "Simultaneously, soft objectives define the optimization frontier—balancing sensory texture, creamy melt kinetics, acoustic "
            "snap, and raw material cost minimization. Technologists can interactively toggle constraints between hard vetoes and soft "
            "goals, adjust threshold boundaries, or insert custom compliance rules. Once verified, the active constraints matrix locks "
            "in mass balance equality and feeds the parameter space directly into the mathematical optimization solver."
        )
    },
    {
        "id": "section_05",
        "title": "Candidate Generation and Texture Strategy Inspection",
        "start_sec": 230.0,
        "rate": "+23%",
        "text": (
            "With constraints established, the platform initiates candidate generation. Rather than relying on empirical trial-and-error, "
            "the engine explores eligible ingredient combinations and applies sequential least squares programming—or SLSQP optimization—alongside "
            "Pareto-based frontier evaluation.\n\n"
            "Pareto scoring evaluates competing formulation criteria simultaneously, isolating non-dominated alternatives where improving "
            "nutritional density does not compromise cost or physical texture. The system groups the highest-scoring recipes into four "
            "specialized archetypes: Functionality and Texture, Balanced Pareto, Nutrition-Maximized, and Cost-Optimized.\n\n"
            "Opening the inspector for Candidate Set C—which achieved the top Pareto rank with an overall score of eighty-three point "
            "eight percent—reveals its underlying formulation rationale. This recipe optimizes the continuous lipid phase and emulsifier "
            "synergy to maximize sensory mouthfeel and bloom resistance. The mathematical solver card explicitly confirms exact one-hundred "
            "percent mass balance and water activity below zero point five eight. Transparent trade-off analytics notify formulators that "
            "the higher lipid fraction requires disciplined temper crystallization control to guarantee shelf stability."
        )
    },
    {
        "id": "section_06",
        "title": "Multi-Candidate Comparison and Trade-Off Analysis",
        "start_sec": 319.0,
        "rate": "+23%",
        "text": (
            "Closing the modal, we transition into the comparative analysis view. Here, developers can benchmark candidate formulations "
            "side by side along the Pareto frontier.\n\n"
            "The Nutrition-Maximized candidate achieves an impressive forty-five grams of protein per serving using dense plant isolates, "
            "but incurs a higher ingredient cost of thirteen dollars and six cents per kilogram. In contrast, the Cost-Optimized candidate "
            "reduces unit cost to ten dollars and two cents while maintaining baseline functional standards. The Balanced set strikes an "
            "optimal commercial middle ground, while the Functionality set delivers premium structural integrity.\n\n"
            "By presenting multi-dimensional trade-offs transparently, the platform eliminates guesswork, enabling cross-functional teams "
            "from R and D, procurement, and brand management to select the winning formula collaboratively."
        )
    },
    {
        "id": "section_07",
        "title": "Final Formulation Report and Process Specifications",
        "start_sec": 378.0,
        "rate": "+23%",
        "text": (
            "Selecting Candidate Set C generates the comprehensive final formulation report. This dossier serves as the master technical "
            "specification for manufacturing handover.\n\n"
            "The report details exact ingredient inclusion percentages, scaled batch weights for pilot and commercial runs, and pre-calculated "
            "nutritional facts. Crucially, formulation components are linked directly to unit manufacturing operations. It prescribes "
            "mechanical particle refining below twenty-five microns, a forty-five degree Celsius conching cycle to disperse the fat phase, "
            "and precision seed tempering to induce form five polymorphic crystallization.\n\n"
            "Critical quality parameters—including a certified water activity of zero point five eight and a twelve-month ambient antioxidant "
            "stability pass—are validated upfront. This actionable output eliminates scale-up friction, transforming a computational candidate "
            "into a pilot-ready commercial reality."
        )
    },
    {
        "id": "section_08",
        "title": "Ingredient Library and Scientific Dossiers",
        "start_sec": 442.5,
        "rate": "+23%",
        "text": (
            "Beyond project-specific workflows, the platform provides dedicated scientific knowledge tools. Navigating to the Ingredient "
            "Library opens a centralized repository of verified food raw materials, functional properties, and regulatory profiles.\n\n"
            "Formulators can filter ingredients by functional category, allergen exclusions, or specific dietary claims. Opening an ingredient "
            "specification—such as Rare Sugar Allulose—displays comprehensive biochemical and regulatory metadata, including its official "
            "FDA GRAS notice number, near-zero caloric impact, and glycemic index profile.\n\n"
            "The library connects directly to the underlying Knowledge Graph, displaying localized subgraphs of functional interactions and "
            "clean-label substitution candidates. Whether reformulating to reduce sugar or searching for novel texturizers, formulators gain "
            "immediate access to scientifically validated ingredient intelligence."
        )
    },
    {
        "id": "section_09",
        "title": "Knowledge Graph Exploration and Reasoning Chains",
        "start_sec": 508.0,
        "rate": "+23%",
        "text": (
            "At the core of the platform is its Knowledge Graph—an ontology-driven semantic network that models food science relationships "
            "far beyond the limits of conventional databases.\n\n"
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
            "By traversing these structured semantic paths, the platform predicts ingredient compatibility, identifies potential allergen "
            "cross-reactivity, and ensures every formulation is grounded in verifiable biochemical science."
        )
    },
    {
        "id": "section_10",
        "title": "Enterprise Synthesis and Conclusion",
        "start_sec": 640.0,
        "rate": "+23%",
        "text": (
            "In conclusion, the Food Formulation Platform delivers an end-to-end intelligent environment for modern food product development. "
            "By integrating natural language brief interpretation, instant formulation auditing, constraint-driven mathematical optimization, "
            "and Knowledge Graph semantic reasoning, the platform empowers food scientists to innovate faster and with greater scientific "
            "certainty.\n\n"
            "From initial concept and feasibility checks to final pilot-ready technical dossiers, computational formulation transforms weeks "
            "of trial-and-error into minutes of data-driven design. Thank you for watching our demonstration."
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
        f.write("FOOD FORMULATION PLATFORM - CONTINUOUS DEMONSTRATION NARRATION SCRIPT\n")
        f.write("Voice: American Female (en-US-JennyNeural) | Target: Continuous (~160 WPM, <= 3s pauses)\n")
        f.write("=" * 85 + "\n\n")
        for idx, sec in enumerate(SECTIONS_CONFIG, 1):
            start_m, start_s = int(sec["start_sec"] // 60), int(sec["start_sec"] % 60)
            f.write(f"Section {idx:02d}: {sec['title']} (Starts at {start_m:02d}:{start_s:02d})\n")
            f.write("-" * 85 + "\n")
            f.write(sec["text"].strip() + "\n\n")
    print(f"[Script] Saved {script_txt_path}")

    # Generate each section audio and compute exact durations and pauses
    total_words = 0
    total_speech_sec = 0.0
    section_audios = []
    
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
        
        section_audios.append({
            "id": sec["id"],
            "title": sec["title"],
            "start_sec": sec["start_sec"],
            "dur": dur,
            "end_sec": sec["start_sec"] + dur,
            "words": words,
            "wpm": wpm,
            "data": data
        })

    # Check timings & write to master track
    for idx, sa in enumerate(section_audios):
        start_samp = int(sa["start_sec"] * fs)
        end_samp = start_samp + len(sa["data"])
        if end_samp > total_samples:
            sa["data"] = sa["data"][:total_samples - start_samp]
            end_samp = total_samples
            
        master_narration[start_samp:end_samp] += sa["data"]
        
        next_start = section_audios[idx + 1]["start_sec"] if idx + 1 < len(section_audios) else video_dur
        pause_after = next_start - sa["end_sec"]
        print(f"[{sa['id']}] {sa['title'][:32]:32s} | Start: {sa['start_sec']:5.1f}s | Dur: {sa['dur']:5.2f}s | End: {sa['end_sec']:5.1f}s | Next: {next_start:5.1f}s | Pause: {pause_after:4.1f}s | Words: {sa['words']:3d} | WPM: {sa['wpm']:5.1f}")

    overall_wpm = (total_words / total_speech_sec) * 60
    print(f"\n[Summary] Total Words: {total_words} | Total Spoken Duration: {total_speech_sec:.2f}s ({total_speech_sec/video_dur*100:.1f}% coverage) | Overall WPM: {overall_wpm:.1f} WPM")
    
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
    print(f"[Mux] Multiplexing video with continuous American female narration into {out_mp4}...")
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
        
    print("\n=== ALL CONTINUOUS DELIVERABLES GENERATED IN narration_output/ ===")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        size_mb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / (1024 * 1024)
        print(f" - {f} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    asyncio.run(main())

