import imageio_ffmpeg
import subprocess

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg, "-y", "-ss", "15", "-i", r"demo_output\FINAL RECORDING.mp4",
    "-t", "8", "-vf", "fps=1", r"inspect_video\sec2_%02d.jpg"
]
subprocess.run(cmd, check=True)
print("Done extracting sec2_*.jpg")

