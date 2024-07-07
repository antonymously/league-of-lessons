import numpy as np
import math
from copy import copy
from typing import Optional
from league_of_lessons.game_generation.coop_dnd_generation import generate_story_continuation
from league_of_lessons.question_management import QuestionManager

def adjust_dice_roll(dice_roll: int, dice_type: str, answer_correct: bool):
    dice_max = int(dice_type[1:])

    penalty = math.ceil(dice_max*0.25)
    bonus = math.ceil(dice_max*0.25)

    if answer_correct:
        return min(dice_roll + bonus, dice_max)
    else:
        return max(dice_roll - penalty, 1)

class GameState:
    '''
    Saves the game history, display image and audio.
    '''
    
    def __init__(self,
        history: list = [],
        img_path: Optional[str] = None,
        audio_path: Optional[str] = None,
        _initial_dice_roll: Optional[int] = None,
        _current_question_idx: Optional[int] = None,
        _current_answer: Optional[dict] = None,
    ):
        self.history = history
        self.img_path = img_path
        self.audio_path = audio_path
        self._initial_dice_roll = _initial_dice_roll
        self._current_question_idx = _current_question_idx
        self._current_answer = _current_answer

class GameSession:

    def __init__(self, question_manager: QuestionManager = None, game_state: GameState = None):

        self.question_manager = question_manager
        
        if game_state is None:
            self.reset()
        else:
            self.load_state(game_state = game_state)

    def reset(self):
        self.history = []
        self.img_path = None
        self.audio_path = None

        self._initial_dice_roll = None
        self._current_question_idx = None
        self._current_answer = None

    def load_state(self, game_state: GameState):
        self.history = game_state.history
        self.img_path = game_state.img_path
        self.audio_path = game_state.audio_path

        self._initial_dice_roll = game_state._initial_dice_roll
        self._current_question_idx = game_state._current_question_idx
        self._current_answer = game_state._current_answer

    def get_game_state(self):
        '''
        NOTE: Saving game state should only be allowed
            when awaiting player action.
            Most recent event should be a required_action.

            Do not allow saving while answering study question.
        '''
        return GameState(
            history = self.history,
            img_path = self.img_path,
            audio_path = self.audio_path,
            _initial_dice_roll = self._initial_dice_roll,
            _current_question_idx = self._current_question_idx,
            _current_answer = self._current_answer,
        )

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
            self.history += next_events
        elif action["event_type"] == "player_action":
            self.history.append(action)
            next_events = generate_story_continuation(history = self.history)
            self.history += next_events
        elif action["event_type"] == "player_decision":
            self.history.append(action)
            next_events = generate_story_continuation(history = self.history)
            self.history += next_events
        elif action["event_type"] == "player_answer":
            # NOTE: don't include the question and answer in the history
            # just the final dice roll

            self._current_answer = copy(action)
            is_correct = (action["answer"] == self.question_manager.get_question(self._current_question_idx)[1]["correct_answer"])
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
            self.history += next_events

            # show result of question and dice adjustment for previous question
            next_events = [
                {
                    "event_type": "answer_assessment",
                    "assessment": "Correct" if is_correct else "Incorrect",
                    "correct_answer": self.question_manager.question_set[self._current_question_idx]["correct_answer"],
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
                self._current_question_idx, current_question = self.question_manager.get_question()

                # return events plus initial roll and question
                return next_events + [
                    {
                        "event_type": "initial_dice_roll",
                        "rolled_value": str(self._initial_dice_roll),
                    },
                    {
                        "event_type": "study_question",
                        "question_text": current_question["question_text"],
                        "choices": current_question["choices"],
                    },
                ]
