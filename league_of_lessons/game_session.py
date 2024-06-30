import numpy as np
import math
from typing import Optional
from league_of_lessons.game_generation.coop_dnd_generation import generate_story_continuation

def adjust_dice_roll(dice_roll: int, dice_type: str, answer_correct: bool):
    dice_max = int(next_events[-1]["dice_type"][1:])

    penalty = math.ceil(dice_max*0.25)
    bonus = math.ceil(dice_max*0.25)

    if answer_correct:
        return min(dice_roll + bonus, dice_max)
    else:
        return max(dice_roll - penalty, 1)

class GameSession:

    def __init__(self, question_set: list = []):

        self.question_set = question_set
        self.history = []
        
        self._initial_dice_roll = None
        self._current_question_idx = None

        self.n_questions = len(self.question_set)

    def reset(self):
        self.history = []

    def next(self, action: Optional[dict] = None):
        '''
        Continues the session given the input action of the player.

        Input action is a player_action, player_decision or player_answer.
        If the action_required is player_dice_roll, the dice is rolled automatically.
        But the player then has to answer a question to adjust the rolled value.

        Action is not required if history is empty (ie. story is just starting)
        '''

        if action is None:
            next_events = generate_story_continuation(history = self.history)
        elif action["event_type"] == "player_action":
            self.history.append(action)
            next_events = generate_story_continuation(history = self.history)
        elif action["event_type"] == "player_decision":
            self.history.append(action)
            next_events = generate_story_continuation(history = self.history)
        elif action["event_type"] == "player_answer":
            # NOTE: don't include the question and answer in the history
            # just the final dice roll

            is_correct = (action["answer"] == self.question_set[self._current_question_idx]["correct_answer"])
            adjusted_dice_roll = adjust_dice_roll(
                self._initial_dice_roll,
                self.history[-1]["dice_type"],
                answer_correct = is_correct,
            )

            self.history.append({
                "event_type": "player_dice_roll",
                "rolled_value": str(adjusted_dice_roll)
            })
            next_events = generate_story_continuation(history = self.history)

            # show result of question and dice adjustment for previous question
            next_events = [
                {
                    "event_type": "answer_assessment",
                    "assessment": "Correct" if is_correct else "Incorrect",
                    "correct_answer": self.question_set[self._current_question_idx]["correct_answer"],
                    "adjusted_dice_roll": str(adjusted_dice_roll),
                }
            ] + next_events

        if next_events[-1]["event_type"] == "story_block":
            # story has ended
            return next_events
        elif next_events[-1]["event_type"] == "required_action":
            if next_events[-1]["required_action"] in ["player_action","player_decision"]:
                return next_events
            elif next_events[-1]["required_action"] == "player_dice_roll":
                dice_max = int(next_events[-1]["dice_type"][1:])

                # make initial roll
                self._initial_dice_roll = np.random.randint(1, dice_max + 1)

                # select question
                # for now, select question randomly
                # later on consider question history, mastery, etc.
                self._current_question_idx = np.random.rantint(1, self.n_questions + 1)

                # return events plus initial roll and question
                return next_events + [
                    {
                        "event_type": "initial_dice_roll",
                        "rolled_value": str(self._initial_dice_roll),
                    },
                    {
                        "event_type": "study_question",
                        "question_text": self.question_set[self._current_question_idx]["question_text"],
                        "choices": self.question_set[self._current_question_idx]["choices"],
                    },
                ]
