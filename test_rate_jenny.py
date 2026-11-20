import asyncio
import edge_tts
import imageio_ffmpeg
import subprocess

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

test_text = (
    "Welcome to our AI-powered Food Formulation Platform, designed to streamline food product development "
    "through artificial intelligence and structured food science knowledge. On the home page, users can submit "
    "product briefs in natural language to initiate intelligent formulation workflows."
)

async def test_rate(rate_str):
    out = f"test_{rate_str.replace('+', '').replace('%', '')}.mp3"
    c = edge_tts.Communicate(test_text, voice="en-US-JennyNeural", rate=rate_str)
    await c.save(out)
    cmd = [ffmpeg, "-i", out]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            dur = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
            words = len(test_text.split())
            wpm = (words / dur) * 60
            print(f"Rate: {rate_str} -> Duration: {dur:.2f}s | Words: {words} | WPM: {wpm:.1f}")

async def main():
    for r in ["+0%", "+5%", "+10%", "+15%"]:
        await test_rate(r)

asyncio.run(main())

