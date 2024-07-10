import json
from textwrap import dedent
from league_of_lessons import (
    MODEL_NAME,
    ANTHROPIC_CLIENT,
)

def summarize_current_state(history):
    '''
    Use claude to summarize the current state in preparation for image generation.
    '''

    system_prompt = dedent(
    '''
    You will be provided the ongoing history of a Dungeons and Dragons-like game in json format.
    In 50 words or less, describe the current scenario as of the end of the history.
    Provide details which can be used by an image generating AI to generate an image of the scenario.
    '''
    ).strip()

    prompt = dedent('''
        Provide a description for the following history:
        {history}
    ''').strip().format(
        history = json.dumps(history, indent = 4)
    )

    response = ANTHROPIC_CLIENT.messages.create(
        model = MODEL_NAME,
        max_tokens = 4096,
        system = system_prompt,
        messages = [
            {"role": "user", "content": prompt},
        ],
    )

    return response.content[0].text

def trim_history(trim_thresh = 30, trim_to = 15):
    '''
    Use claude to trim history. If history is longer than or equal to the trim_thresh
    it will trim it down to the trim_to and add a story summary at the start.
    '''
    pass