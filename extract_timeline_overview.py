import imageio_ffmpeg
import subprocess

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg, "-y", "-i", r"demo_output\FINAL RECORDING.mp4",
    "-vf", "fps=1/30", r"inspect_video\time_%03d.jpg"
]
subprocess.run(cmd, check=True)
print("Done extracting timeline frames every 30s")

