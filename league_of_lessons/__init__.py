'''
Declare global variables here.
'''

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

MODEL_NAME = "claude-3-5-sonnet-20240620"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

ANTHROPIC_CLIENT = anthropic.Anthropic(api_key = ANTHROPIC_API_KEY)
SAVE_GAME_FILEPATH = "./data/saved_game_state.pkl"

def set_anthropic_api_key(anthropic_api_key):
    # use this to set anthropic API key manually
    ANTHROPIC_CLIENT = anthropic.Anthropic(api_key = anthropic_api_key)