import json
from textwrap import dedent
from league_of_lessons import (
    MODEL_NAME,
    ANTHROPIC_CLIENT,
)

def generate_questions(study_material_txt, question_type="multiple_choice", n_questions=30):
    '''
    Uses Claude to generate different types of questions from the study material.
    Produces questions in a prescribed json format based on the question_type.
    '''
    if question_type == "multiple_choice":
        question_format = '''
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
        '''
    elif question_type == "true_false":
        question_format = '''
        [
            {{
                "question_text": "<question text>",
                "correct_answer": "<true or false>"
            }}
        ]
        '''
    elif question_type == "essay":
        question_format = '''
        [
            {{
                "question_text": "<question text>"
            }}
        ]
        '''
    elif question_type == "fill_in_the_blanks":
        question_format = '''
        [
            {{
                "question_text": "<question with blanks>",
                "correct_answers": ["<correct answer 1>", "<correct answer 2>", ...]
            }}
        ]
        '''
    else:
        raise ValueError("Invalid question_type. Choose from 'multiple_choice', 'true_false', 'essay', 'fill_in_the_blanks'.")

    prompt = dedent(f'''
        Use the provided study material to generate {n_questions} {question_type} questions.
        Provide the questions in the following json format.
        {question_format}

        Respond with only the json questions. Don't provide any further explanation or introductions.

        STUDY MATERIAL:
        {study_material_txt}
    ''').strip()

    response = ANTHROPIC_CLIENT.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return json.loads(response.content[0].text)