import edge_tts

async def generate_audio(text, outputFilename):
    # Use a Hindi voice
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural")
    await communicate.save(outputFilename)





