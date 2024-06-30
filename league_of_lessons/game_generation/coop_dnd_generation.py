'''
Uses an LLM to continuously generate a cooperative, interactive adventure.

The adventure goes like this:
- LLM generates story block until player action, decision or dice roll is required.
- If action is required, 
-   player inputs action using natural language, then continue.
- If decision is required, 
-   player selects among choices provided by LLM, then continue.
- If dice roll is required,
-   player rolls dice specified by LLM.
-   player then answers a study question to penalize or augment the roll.
-   then continue

'''
import json
from textwrap import dedent
from league_of_lessons import (
    MODEL_NAME,
    ANTHROPIC_CLIENT,
)

def generate_story_continuation(history: list = []):
    '''
    Generates the continuation of the story using claude.
    Continues the story until a player action/decision/dice roll is required.

    History is in the form of a list containing previous story portions,
    player actions, decisions, dice rolls
    '''

    system_prompt = dedent('''
        You are a dungeon master for a Dnd-like text game.
        You will be provided the history of the game so far.
        History is in the form of a list containing previous story portions,
        player actions, decisions, dice rolls.

        If the history is empty, the game has just started.

        Your role is to provide the continuation of the story until another player
        action, decision or dice roll is required.
        You may also immediately require an action, decision or dice roll when appropriate.
        
        Player actions are provided by the player in natural language.
        Player decisions are selected among choices you provide.
        Player dice rolls are carried out as you require.
        You should require dice rolls immediately require a dice roll when the player
        takes an action which involves elements of skill and/or chance.
        These can be attacks, sneack attempts, spell casts, persuation attempts, etc.

        Provide your response as a continuation of the history in the following json format.
        [
            {
                "event_type": "story_block",
                "story": "<story text>"
            },
            {
                "event_type": "required_action",
                "required_action": "<player_action, player_decision or player_dice_roll>",
                "prompt": "<briefly explain the required action, decision or purpose for dice roll>",
                "choices": {
                    "a": "<choice-a text>",
                    "b": "<choice-b text>"
                }
                "dice_type": "<d4, d6, d8, d10, d12 or d20>"
            }
        ]

        Provide choices only when the required_action is player_decision.
        Provide the dice_type only when the required_action is dice roll.
        To end the story, do not provide any more required action.

        Respond with only the json continuation. Don't provide any further explanation or introductions.
    ''').strip()

    prompt = dedent('''
        Provide continuation for the following history:
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

    return json.loads(response.content[0].text)