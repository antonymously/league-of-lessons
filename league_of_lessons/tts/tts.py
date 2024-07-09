from pyht import Client
from pyht.client import TTSOptions
import tempfile
import wave
import os
import requests
import json

if not os.environ.get('PYHT_VOICE_NARRATOR', False):

    # Set default Voice
    os.environ['PYHT_VOICE_NARRATOR'] = 's3://voice-cloning-zero-shot/b3def996-302e-486f-a234-172fa0279f0e/anthonysaad/manifest.json'



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