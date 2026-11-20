import asyncio
import edge_tts

async def list_us_female_voices():
    voices = await edge_tts.list_voices()
    us_females = [v for v in voices if v["Locale"].startswith("en-US") and v["Gender"] == "Female"]
    for v in us_females[:8]:
        print(v["ShortName"], "-", v["FriendlyName"])

asyncio.run(list_us_female_voices())

