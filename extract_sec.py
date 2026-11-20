import imageio_ffmpeg
import subprocess

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg, "-y", "-ss", "10", "-i", r"demo_output\FINAL RECORDING.mp4",
    "-t", "6", "-vf", "fps=1", r"inspect_video\sec_%02d.jpg"
]
subprocess.run(cmd, check=True)
print("Done extracting sec_*.jpg")

