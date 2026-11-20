import os
import glob
import subprocess
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def process_video():
    raw_files = glob.glob("demo_output/raw_video/*.webm")
    if not raw_files:
        print("No raw webm file found in demo_output/raw_video")
        return False
    
    raw_video = raw_files[0]
    complete_mp4 = "demo_output/Food_Formulator_Complete_Demo.mp4"
    voiceover_mp3 = "demo_output/Food_Formulator_Voiceover.mp3"
    final_narrated_mp4 = "demo_output/Food_Formulator_Final_Narrated_Demo.mp4"

    print(f"[FFmpeg] Found raw video: {raw_video}")
    print(f"[FFmpeg] Transcoding to Full HD 1080p 30fps MP4 (H.264): {complete_mp4}...")

    cmd_transcode = [
        FFMPEG_EXE, "-y",
        "-i", raw_video,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        complete_mp4
    ]
    subprocess.run(cmd_transcode, check=True)
    print(f"[FFmpeg] Complete video created successfully: {complete_mp4}")

    if os.path.exists(voiceover_mp3):
        print(f"[FFmpeg] Multiplexing voiceover audio ({voiceover_mp3}) into final narrated video: {final_narrated_mp4}...")
        cmd_merge = [
            FFMPEG_EXE, "-y",
            "-i", complete_mp4,
            "-i", voiceover_mp3,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            final_narrated_mp4
        ]
        subprocess.run(cmd_merge, check=True)
        print(f"[FFmpeg] Final narrated video created successfully: {final_narrated_mp4}")
    else:
        print(f"[FFmpeg] Voiceover file not found at {voiceover_mp3}")

    return True

if __name__ == "__main__":
    process_video()

