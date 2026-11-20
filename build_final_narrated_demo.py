import asyncio
import os
import shutil
import subprocess
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import imageio_ffmpeg
import edge_tts

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VOICE = "en-IN-PrabhatNeural"
INPUT_VIDEO = r"demo_output\FINAL RECORDING.mp4"
OUTPUT_DIR = "final_narrated_output"
OUTPUT_VIDEO_NAME = "FINAL_RECORDING_WITH_AI_NARRATION.mp4"

# Timeline Configuration
# Each section specifies id, title, start_time (seconds), speaking rate, and text
SECTIONS_CONFIG = [
    {
        "id": "section_01",
        "title": "Introduction",
        "start_sec": 1.0,
        "rate": "+8%",
        "text": (
            "Welcome to our Knowledge Graph-Driven, Constraints-Aware AI-Based Food Formulation Platform.\n\n"
            "This platform is designed to accelerate scientific food product development by combining artificial intelligence, "
            "knowledge graphs, ingredient intelligence, and constraint-based formulation.\n\n"
            "The objective is to help food scientists and product developers identify suitable ingredients, generate formulation candidates, "
            "evaluate product characteristics, and make evidence-supported formulation decisions."
        )
    },
    {
        "id": "section_02",
        "title": "Home Page and Product Brief",
        "start_sec": 34.5,
        "rate": "+6%",
        "text": (
            "Let's begin with the home page, which serves as the primary entry point for the formulation process.\n\n"
            "Users can describe their desired food product using a natural-language product brief. This brief contains the product category, "
            "ingredient preferences, nutritional targets, functional requirements, flavor profile, and shelf-life expectations.\n\n"
            "For this demonstration, we will work with a vegan white chocolate formulation.\n\n"
            "The system takes this product description and prepares it for structured analysis and formulation."
        )
    },
    {
        "id": "section_03",
        "title": "Dashboard",
        "start_sec": 71.0,
        "rate": "+4%",
        "text": (
            "After entering the platform, we reach the formulation dashboard.\n\n"
            "The dashboard provides an overview of the formulation workflow, including candidate ingredients, formulation progress, "
            "nutritional information, functional properties, and evaluation results.\n\n"
            "The platform organizes formulation information into multiple dimensions, allowing users to understand not only which ingredients "
            "are selected but also why they are suitable.\n\n"
            "The dashboard also provides analytical summaries and visual representations of formulation performance, helping users compare "
            "different candidate formulations."
        )
    },
    {
        "id": "section_04",
        "title": "Ingredient Selection",
        "start_sec": 113.0,
        "rate": "+0%",
        "text": (
            "Next, we move to the ingredient selection stage.\n\n"
            "The platform explores available ingredients from its underlying ingredient knowledge base and identifies candidates relevant "
            "to the product requirements.\n\n"
            "Each candidate is associated with structured information such as ingredient category, functional properties, nutritional "
            "composition, and suitability information.\n\n"
            "Rather than selecting ingredients using simple keyword matching alone, the platform uses relationships within the Knowledge Graph "
            "to support ingredient discovery.\n\n"
            "This makes it possible to explore ingredients based on their functional roles and relationships with other food components.\n\n"
            "The selected candidates are then passed to the subsequent formulation and evaluation stages."
        )
    },
    {
        "id": "section_05",
        "title": "Constraint Configuration",
        "start_sec": 168.0,
        "rate": "+0%",
        "text": (
            "An important component of this platform is constraint-aware formulation.\n\n"
            "The system translates product requirements into structured constraints that can be used during candidate evaluation.\n\n"
            "These constraints are divided into two major categories: hard constraints and soft constraints.\n\n"
            "Hard constraints represent mandatory conditions that a formulation must satisfy. For example, since our target product is vegan "
            "white chocolate, dairy-derived ingredients must be excluded.\n\n"
            "Soft constraints represent preferred characteristics, such as a creamy texture, a particular flavor profile, or a preferred "
            "nutritional composition.\n\n"
            "The platform also supports numerical constraints, including minimum protein content, maximum sugar content, and minimum cocoa butter "
            "concentration.\n\n"
            "Each constraint can be associated with a condition, priority, and importance weight.\n\n"
            "This structured representation allows the formulation engine to distinguish between mandatory requirements and optimization "
            "preferences.\n\n"
            "The objective is not simply to generate a recipe, but to generate candidates that are consistent with the specified product "
            "requirements."
        )
    },
    {
        "id": "section_06",
        "title": "Functionality and Texture Evaluation",
        "start_sec": 253.0,
        "rate": "+0%",
        "text": (
            "Now we move to the functional and texture evaluation stage.\n\n"
            "Ingredient selection alone is not sufficient for successful food formulation. Ingredients must also contribute to the required "
            "physical and functional characteristics of the final product.\n\n"
            "For this reason, the platform evaluates candidate sets against different functional and textural requirements.\n\n"
            "For our vegan white chocolate example, important characteristics include fat-system stability, smoothness, creamy mouthfeel, and "
            "melting behaviour.\n\n"
            "The system presents the relevant functional attributes and their associated evaluation results.\n\n"
            "This stage helps identify whether the selected combination of ingredients is suitable for the intended product characteristics.\n\n"
            "It also provides a basis for comparing different ingredient combinations rather than relying entirely on manual selection.\n\n"
            "These evaluations are intended as computational screening and decision-support results; experimental laboratory validation "
            "remains necessary to confirm actual product performance."
        )
    },
    {
        "id": "section_07",
        "title": "Candidate Sets and Formulation Comparison",
        "start_sec": 331.0,
        "rate": "+0%",
        "text": (
            "After the evaluation process, the platform organizes the available ingredient combinations into candidate sets.\n\n"
            "Each candidate set represents a possible formulation direction.\n\n"
            "Users can compare these candidates using their ingredient composition, functional suitability, nutritional characteristics, and "
            "constraint compliance.\n\n"
            "The system provides a structured view of the candidate results, making it easier to identify promising combinations.\n\n"
            "This approach supports systematic comparison and reduces the need to manually inspect every possible ingredient combination.\n\n"
            "The objective is to shortlist formulations that offer a reasonable balance between product requirements and ingredient functionality."
        )
    },
    {
        "id": "section_08",
        "title": "Formulation Results",
        "start_sec": 384.0,
        "rate": "+0%",
        "text": (
            "Here, we return to the formulation results and analytical dashboard.\n\n"
            "The dashboard brings together the information generated throughout the formulation workflow.\n\n"
            "Users can examine the selected ingredients, candidate formulation scores, nutritional information, and different evaluation "
            "parameters.\n\n"
            "The visual summaries help communicate the strengths and limitations of each candidate.\n\n"
            "Instead of presenting only a final recipe, the platform provides supporting information that helps explain the formulation "
            "decision.\n\n"
            "This is particularly important in research-oriented food product development, where transparency and traceability are essential."
        )
    },
    {
        "id": "section_09",
        "title": "Ingredient Library",
        "start_sec": 435.0,
        "rate": "+0%",
        "text": (
            "Next, we explore the Ingredient Library.\n\n"
            "The Ingredient Library acts as a centralized repository of food ingredients and their associated information.\n\n"
            "Each ingredient can contain details such as its name, category, functional role, nutritional composition, and other available "
            "properties.\n\n"
            "This structured information is important because the quality of formulation decisions depends heavily on the quality and "
            "organization of the underlying ingredient data.\n\n"
            "The library also provides an interface for exploring individual ingredients and their associated information.\n\n"
            "By maintaining ingredient information in a standardized structure, the platform creates a reusable foundation for multiple food "
            "product categories and formulation tasks."
        )
    },
    {
        "id": "section_10",
        "title": "Knowledge Graph Exploration",
        "start_sec": 510.0,
        "rate": "+0%",
        "text": (
            "Now, let's explore one of the most important components of our platform: the Food Knowledge Graph.\n\n"
            "The Knowledge Graph represents food-related information through interconnected nodes and relationships.\n\n"
            "Unlike a conventional database that primarily stores information in tables, a Knowledge Graph captures semantic relationships "
            "between different entities.\n\n"
            "For example, an ingredient can be connected to its food category, functional role, nutritional properties, flavor characteristics, "
            "and other related entities.\n\n"
            "These connections allow the platform to retrieve information through relationships rather than depending only on exact textual "
            "matches.\n\n"
            "The graph explorer provides a visual representation of these connections.\n\n"
            "Users can inspect individual nodes, explore their neighbouring entities, and understand how different food concepts are "
            "interconnected.\n\n"
            "The platform also supports different levels of graph exploration, from individual ingredient relationships to broader subgraphs.\n\n"
            "This graph-based representation is particularly useful for identifying related ingredients, understanding functional associations, "
            "and supporting context-aware ingredient retrieval.\n\n"
            "The Knowledge Graph therefore acts as the structured knowledge foundation of the formulation system.\n\n"
            "It connects ingredient intelligence with the constraint-aware retrieval and formulation workflow."
        )
    },
    {
        "id": "section_11",
        "title": "Conclusion",
        "start_sec": 625.0,
        "rate": "+2%",
        "text": (
            "To conclude, this platform integrates natural-language product requirements, structured ingredient intelligence, Knowledge "
            "Graph-based retrieval, constraint-aware candidate selection, and formulation evaluation into a unified workflow.\n\n"
            "The major contribution is the integration of food knowledge and formulation constraints to support more systematic and "
            "explainable food product development.\n\n"
            "The platform is designed to assist food scientists and product developers in exploring ingredient combinations, evaluating "
            "formulation candidates, and making informed decisions.\n\n"
            "Future work will focus on improving retrieval accuracy, expanding the ingredient knowledge base, strengthening formulation "
            "evaluation models, and validating generated candidates through laboratory experiments.\n\n"
            "Thank you for watching this demonstration."
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

async def generate_section_speech(sec, out_mp3):
    print(f"Generating {sec['id']} ({sec['title']}) at rate {sec['rate']}...")
    c = edge_tts.Communicate(sec["text"], voice=VOICE, rate=sec["rate"])
    
    subtitles = []
    audio_data = bytearray()
    
    async for chunk in c.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            # offset and duration in 100-nanoseconds (1e7 per second)
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

def build_subtle_ambient(total_sec=687, fs=44100):
    t = np.linspace(0, total_sec, int(fs * total_sec), endpoint=False)
    chord_len = 4.0
    chords = [
        [130.81, 164.81, 196.00, 246.94, 293.66], # Cmaj9
        [110.00, 130.81, 164.81, 196.00, 246.94], # Am9
        [87.31, 130.81, 174.61, 220.00, 261.63],  # Fmaj7
        [98.00, 146.83, 196.00, 246.94, 293.66]   # G6
    ]
    
    audio = np.zeros(len(t), dtype=np.float32)
    total_chords = int(np.ceil(total_sec / chord_len))
    
    for c_idx in range(total_chords):
        chord = chords[c_idx % len(chords)]
        start_sample = int(c_idx * chord_len * fs)
        end_sample = min(int((c_idx + 1.2) * chord_len * fs), len(t))
        num_samples = end_sample - start_sample
        if num_samples <= 0:
            break
        t_chord = np.linspace(0, num_samples / fs, num_samples, endpoint=False)
        env = np.ones(num_samples, dtype=np.float32)
        att = int(min(1.0 * fs, num_samples * 0.3))
        rel = int(min(1.5 * fs, num_samples * 0.4))
        env[:att] = 0.5 * (1 - np.cos(np.linspace(0, np.pi, att)))
        env[-rel:] = 0.5 * (1 + np.cos(np.linspace(0, np.pi, rel)))
        
        chord_signal = np.zeros(num_samples, dtype=np.float32)
        for freq in chord:
            chord_signal += np.sin(2 * np.pi * freq * t_chord) * 0.5
            chord_signal += np.sin(2 * np.pi * (freq * 2) * t_chord) * 0.25
        chord_signal *= env
        audio[start_sample:end_sample] += chord_signal * 0.10

    # Low-pass filter at 900 Hz to sit below speech frequencies
    nyq = 0.5 * fs
    b, a = butter(3, 900 / nyq, btype='low')
    audio = lfilter(b, a, audio)

    # Smooth fades
    fade_in = int(3.0 * fs)
    fade_out = int(4.0 * fs)
    audio[:fade_in] *= np.linspace(0, 1, fade_in)
    audio[-fade_out:] *= np.linspace(1, 0, fade_out)

    # Peak level at -25 dBFS
    max_amp = np.max(np.abs(audio))
    if max_amp > 0:
        audio = (audio / max_amp) * 0.050

    return audio

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    temp_dir = os.path.join(OUTPUT_DIR, "temp_audio")
    os.makedirs(temp_dir, exist_ok=True)
    
    video_dur = get_audio_duration(INPUT_VIDEO)
    print(f"Input video: {INPUT_VIDEO} (Duration: {video_dur:.2f}s)")
    
    fs = 44100
    total_samples = int(np.ceil(video_dur * fs))
    master_narration = np.zeros((total_samples, 2), dtype=np.float32)
    all_subtitles = []
    
    # 1. Generate individual clips and collect subtitle boundaries
    for sec in SECTIONS_CONFIG:
        out_mp3 = os.path.join(OUTPUT_DIR, f"{sec['id']}.mp3")
        subs = await generate_section_speech(sec, out_mp3)
        all_subtitles.extend(subs)
        
        # Convert to wav to load as float32
        temp_wav = os.path.join(temp_dir, f"{sec['id']}.wav")
        convert_mp3_to_wav(out_mp3, temp_wav)
        
        _, data = wavfile.read(temp_wav)
        # Normalize to float32 [-1, 1]
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
            
        dur = len(data) / fs
        start_samp = int(sec["start_sec"] * fs)
        end_samp = start_samp + len(data)
        
        if end_samp > total_samples:
            data = data[:total_samples - start_samp]
            end_samp = total_samples
            
        # Place into master timeline
        master_narration[start_samp:end_samp] += data
        print(f"Placed {sec['id']} at {sec['start_sec']:.1f}s -> {sec['start_sec'] + dur:.1f}s (Dur: {dur:.2f}s)")

    # 2. Add subtle corporate background music (-25 dB below speech)
    print("Synthesizing subtle ambient corporate background music...")
    ambient_audio = build_subtle_ambient(video_dur, fs)
    ambient_stereo = np.column_stack((ambient_audio, ambient_audio))
    
    final_mix = master_narration + ambient_stereo[:total_samples]
    
    # Peak normalization to -1.0 dBFS to prevent any clipping
    max_val = np.max(np.abs(final_mix))
    if max_val > 0.89:
        final_mix = (final_mix / max_val) * 0.89
        
    master_wav = os.path.join(OUTPUT_DIR, "narration_master.wav")
    final_int16 = (final_mix * 32767).astype(np.int16)
    wavfile.write(master_wav, fs, final_int16)
    print("Master audio written to narration_master.wav")
    
    # 3. Export narration_full.mp3 (high quality 256k)
    full_mp3 = os.path.join(OUTPUT_DIR, "narration_full.mp3")
    cmd_mp3 = [
        FFMPEG, "-y", "-i", master_wav,
        "-c:a", "libmp3lame", "-b:a", "256k",
        full_mp3
    ]
    subprocess.run(cmd_mp3, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Exported {full_mp3}")
    
    # 4. Generate narration_subtitles.srt
    srt_path = os.path.join(OUTPUT_DIR, "narration_subtitles.srt")
    print(f"Writing synchronized subtitles to {srt_path}...")
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, sub in enumerate(all_subtitles, 1):
            f.write(f"{idx}\n")
            f.write(f"{format_srt_time(sub['start'])} --> {format_srt_time(sub['end'])}\n")
            f.write(f"{sub['text']}\n\n")
    print(f"Exported {srt_path} with {len(all_subtitles)} subtitle cues")
    
    # 5. Export FINAL_RECORDING_WITH_AI_NARRATION.mp4
    # Multiplex with video using copy stream for maximum visual fidelity & 0 loss
    out_mp4 = os.path.join(OUTPUT_DIR, OUTPUT_VIDEO_NAME)
    print(f"Multiplexing video and audio into {out_mp4}...")
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
    print(f"Created {out_mp4} successfully!")
    
    # Also copy to demo_output for convenience
    demo_out_mp4 = os.path.join("demo_output", OUTPUT_VIDEO_NAME)
    shutil.copy2(out_mp4, demo_out_mp4)
    print(f"Copied final video to {demo_out_mp4}")
    
    # Clean up temp wav directory
    shutil.rmtree(temp_dir, ignore_errors=True)
    if os.path.exists(master_wav):
        os.remove(master_wav)
        
    print("\n=== PIPELINE EXECUTION COMPLETE ===")
    print("Deliverables in final_narrated_output/:")
    for f in os.listdir(OUTPUT_DIR):
        size_mb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / (1024 * 1024)
        print(f" - {f} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    asyncio.run(main())

