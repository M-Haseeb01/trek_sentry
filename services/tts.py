from gradio_client import Client as GradioClient
from tempfile import NamedTemporaryFile

# Gradio TTS model

tts_client = GradioClient("MHaseeb-01/TTS")

def synthesize(text: str) -> bytes:
    """
    Converts text to speech using Gradio TTS.
    Returns raw audio bytes.
    """
    audio_path = tts_client.predict(
        text=text,
        speed=1.3,
        api_name="/synthesize_speech"
    )

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    return audio_bytes
