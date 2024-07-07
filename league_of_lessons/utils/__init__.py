'''
Utilities
'''
import time
from textwrap import dedent

def fake_stream_text(text, delay = 0.05):
    for char in text:
        yield char
        time.sleep(delay)

def history_to_text(history):

    history_text = ""

    for i, event in enumerate(history):
        history_text += "<br>"
        if event["event_type"] == "story_summary":
            history_text += "SUMMARY OF STORY SO FAR:<br>"
            history_text += event["story"]

        elif event["event_type"] == "story_block":
            history_text += "STORY CONTINUATION:<br>"
            history_text += event["story"]

        elif event["event_type"] == "required_action":
            if event["required_action"] == "player_decision":
                history_text += "DECISION REQUIRED:<br>"
                history_text += event["prompt"]
            elif event["required_action"] == "player_action":
                history_text += "ACTION REQUIRED:<br>"
                history_text += event["prompt"]
            elif event["required_action"] == "player_dice_roll":
                history_text += "DICE ROLL REQUIRED:<br>"
                history_text += event["prompt"]

        elif event["event_type"] == "initial_dice_roll":
            history_text += "ROLLED INITIAL VALUE: {}".format(event["rolled_value"])

        elif event["event_type"] == "study_question":
            history_text += "REQUIRED STUDY QUESTION:<br>"
            history_text += event["question_text"]
            for key, choice in event["question_text"].items():
                history_text += "\n" + f"{key}. {choice}"

        elif event["event_type"] == "answer_assessment":
            history_text += "ANSWER ASSESSMENT: {}".format(event["assessment"])
            history_text += "\nCORRECT ANSWER: {}".format(event["correct_answer"])
            history_text += "\nDICE ROLL ADJUSTED TO: {}".format(event["adjusted_dice_roll"])

        elif event["event_type"] == "player_decision":
            history_text += "PLAYER DECISION:<br>"
            history_text += "{}. {}".format(event["choice"], history[i - 1]["choices"][event["choice"]])

        elif event["event_type"] == "player_action":
            history_text += "PLAYER ACTION:<br>"
            history_text += event["action"]

        elif event["event_type"] == "player_answer":
            history_text += "PLAYER ANSWER:<br>"
            history_text += event["answer"]


    return history_text