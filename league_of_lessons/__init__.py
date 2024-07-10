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
TTS_SERVICE = os.getenv("TTS_SERVICE")

ANTHROPIC_CLIENT = anthropic.Anthropic(api_key = ANTHROPIC_API_KEY)
OPENAI_CLIENT = OpenAI(api_key = OPENAI_API_KEY)
SAVE_GAME_FILEPATH = "./data/saved_game_state.pkl"

def set_anthropic_api_key(anthropic_api_key):
    # use this to set anthropic API key manually
    ANTHROPIC_CLIENT = anthropic.Anthropic(api_key = anthropic_api_key)

def set_openai_api_key(openai_api_key):
    # use this to set openai API key manually
    OPENAI_CLIENT = OpenAI(api_key = OPENAI_API_KEY)