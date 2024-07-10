'''
Declare global variables here.
'''

import os
from dotenv import load_dotenv
import anthropic
from openai import OpenAI

load_dotenv()

MODEL_NAME = "claude-3-5-sonnet-20240620"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TTS_SERVICE = os.getenv("TTS_SERVICE", "OPENAI")
PYHT_USER_ID = os.getenv("PYHT_USER_ID")
PYHT_SECRET = os.getenv("PYHT_SECRET")

global ANTHROPIC_CLIENT
global OPENAI_CLIENT

if ANTHROPIC_API_KEY is not None:
    ANTHROPIC_CLIENT = anthropic.Anthropic(api_key = ANTHROPIC_API_KEY)
else:
    # wait for external set
    ANTHROPIC_CLIENT = None

if OPENAI_API_KEY is not None:
    OPENAI_CLIENT = OpenAI(api_key = OPENAI_API_KEY)
else:
    OPENAI_CLIENT = None

SAVE_GAME_FILEPATH = "./data/saved_game_state.pkl"

def set_anthropic_api_key(anthropic_api_key):
    # use this to set anthropic API key manually
    ANTHROPIC_CLIENT = anthropic.Anthropic(api_key = anthropic_api_key)

def set_openai_api_key(openai_api_key):
    # use this to set openai API key manually
    OPENAI_CLIENT = OpenAI(api_key = openai_api_key)