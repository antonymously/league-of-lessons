from pyht import Client
from pyht.client import TTSOptions
import tempfile
import wave
import os


def text_to_speech(text_to_convert):
    """Convert text to speech using pyht API"""

    client = Client(
    user_id=os.environ['PYHT_USER_ID'], 
    api_key=os.environ['PYHT_SECRET']
    )

    options = TTSOptions(voice=os.environ['PYHT_VOICE_NARRATOR'])

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as fp:
        with wave.open(fp, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)

            for chunk in client.tts(text_to_convert, options):
                wf.writeframes(chunk)

        audio_file_path = fp.name

    return audio_file_path

