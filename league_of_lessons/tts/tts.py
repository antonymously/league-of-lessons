from pyht import Client
from pyht.client import TTSOptions
import tempfile
import wave
import os
import requests
import json
from league_of_lessons import OPENAI_CLIENT, TTS_SERVICE

if not os.environ.get('PYHT_VOICE_NARRATOR', False):

    # Set default Voice
    os.environ['PYHT_VOICE_NARRATOR'] = 's3://voice-cloning-zero-shot/b3def996-302e-486f-a234-172fa0279f0e/anthonysaad/manifest.json'

if not os.path.exists("./assets/narration"):
    os.makedirs("./assets/narration") 

PYHT_USER_ID = os.environ['PYHT_USER_ID']
PYHT_SECRET = os.environ['PYHT_SECRET']

def text_to_speech(text_to_convert):
    if TTS_SERVICE == "OPENAI":
        return text_to_speech_openai(text_to_convert)
    else:
        return text_to_speech_pyht(text_to_convert)

def text_to_speech_openai(text_to_convert):
    narration_file_path = "./assets/narration/narration.mp3"

    response = OPENAI_CLIENT.audio.speech.create(
        model = "tts-1",
        voice = "onyx",
        input = text_to_convert
    )

    response.stream_to_file(narration_file_path)
    return narration_file_path

def set_pyht_keys(pyht_user_id, pyht_secret):
    # use this to set pyht keys externally
    PYHT_USER_ID = pyht_user_id
    PYHT_SECRET = pyht_secret

def text_to_speech_pyht(text_to_convert):
    """Convert text to speech using pyht API"""

    client = Client(
        user_id = PYHT_USER_ID,
        api_key = PYHT_SECRET,
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

def get_list_of_voices(endpoint='v2'):
    if endpoint=='v2':
        
        url = "https://api.play.ht/api/v2/voices"

        headers = {
            "accept": "application/json",
            "AUTHORIZATION": os.environ['PYHT_SECRET'], 
            "X-USER-ID": os.environ['PYHT_USER_ID'], 
            
        }

        response = requests.get(url, headers=headers)
        list_of_voices = response.json()
    

    return list_of_voices