import os
import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
os.makedirs("inspect_video", exist_ok=True)

# Extract frames every 5 seconds for the first 100 seconds to see exact screen transitions
cmd = [
    ffmpeg, "-y", "-i", r"demo_output\FINAL RECORDING.mp4",
    "-vf", "fps=1/5", "-vframes", "25",
    r"inspect_video\frame_%02d.jpg"
]
subprocess.run(cmd, check=True)

# Also check scene changes
cmd_scenes = [
    ffmpeg, "-i", r"demo_output\FINAL RECORDING.mp4",
    "-filter_complex", "select='gt(scene,0.1)',metadata=print:file=inspect_video/scenes.txt",
    "-f", "null", "-"
]
subprocess.run(cmd_scenes, stderr=subprocess.DEVNULL)
print("Frames extracted:", sorted(os.listdir("inspect_video")))

