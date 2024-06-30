'''
Generates multiple choice questions from the provided study material.
'''
import json
from textwrap import dedent
from league_of_lessons import (
    MODEL_NAME,
    ANTHROPIC_CLIENT,
)

def generate_multiple_choice_questions(study_material_txt, n_questions = 30):
    '''
    Uses claude to generate multiple choice questions from the study material.
    Produces questions in a prescribed json format.
    '''
    prompt = dedent('''
        Use the provided study material to generate {n_questions} multiple choice questions.
        Provide the questions in the following json format.
        [
            {{
                "question_text": "<question text>",
                "choices": {{
                    "a": "<choice a>",
                    "b": "<choice b>",
                    "c": "<choice c>",
                    "d": "<choice d>",
                }},
                "correct_answer": "<letter key of correct answer>"
            }}
        ]

        Respond with only the json questions. Don't provide any further explanation or introductions.

        STUDY MATERIAL:
        {study_material_txt}
    ''').strip().format(
        study_material_txt = study_material_txt,
        n_questions = n_questions,
    )

    response = ANTHROPIC_CLIENT.messages.create(
        model = MODEL_NAME,
        max_tokens = 4096,
        messages = [
            {"role": "user", "content": prompt},
        ],
    )

    return json.loads(response.content[0].text)