import numpy as np
import math
from copy import copy
from typing import Optional
import json
from league_of_lessons.game_generation.coop_dnd_generation import generate_story_continuation
from league_of_lessons.question_management import QuestionManager
from league_of_lessons.utils import story_history_only

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
        _next_events: Optional[list] = None,
        _study_score: Optional[list] = [0,0],
    ):
        self.history = history
        self.img_path = img_path
        self.audio_path = audio_path
        self._initial_dice_roll = _initial_dice_roll
        self._current_question_idx = _current_question_idx
        self._current_answer = _current_answer
        self._next_events = _next_events
        self._study_score = _study_score

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
        self._next_events = None
        self._study_score = [0,0]

    def load_state(self, game_state: GameState):
        self.history = game_state.history
        self.img_path = game_state.img_path
        self.audio_path = game_state.audio_path

        self._initial_dice_roll = game_state._initial_dice_roll
        self._current_question_idx = game_state._current_question_idx
        self._current_answer = game_state._current_answer
        self._next_events = game_state._next_events
        self._study_score = game_state._study_score

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
            _next_events = self._next_events,
            _study_score = self._study_score,
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
            next_events = generate_story_continuation(history = story_history_only(self.history))

        elif action["event_type"] == "player_action":
            next_events = [action]
            next_events += generate_story_continuation(history = story_history_only(self.history + [action]))

        elif action["event_type"] == "player_decision":
            next_events = [action]
            next_events += generate_story_continuation(history = story_history_only(self.history + [action]))
            
        elif action["event_type"] == "player_answer":
            # NOTE: don't include the question and answer in the history
            # just the final dice roll

            next_events = [action]
            self._current_answer = copy(action)
            self._current_answer["question_idx"] = self._current_question_idx

            is_correct = (action["answer"] == self.question_manager.get_question(self._current_question_idx)[1]["correct_answer"])
            self._study_score[1] += 1
            if is_correct:
                self._study_score[0] += 1

            adjusted_dice_roll = adjust_dice_roll(
                self._initial_dice_roll,
                self.history[-3]["dice_type"],
                answer_correct = is_correct,
            )

            next_events += [
                {
                    "event_type": "answer_assessment",
                    "assessment": "Correct" if is_correct else "Incorrect",
                    "correct_answer": self.question_manager.question_set[self._current_question_idx]["correct_answer"],
                    "adjusted_dice_roll": str(adjusted_dice_roll),
                }
            ]

            dice_roll_event = {
                "event_type": "player_dice_roll",
                "rolled_value": str(adjusted_dice_roll)
            }

            next_events += [dice_roll_event]

            # exclude study question events
            next_events += generate_story_continuation(history = story_history_only(self.history + [dice_roll_event]))

        if next_events[-1]["event_type"] == "story_block":
            # story has ended
            self._next_events = next_events
            self.history += next_events
            return next_events
        elif next_events[-1]["event_type"] == "required_action":
            if next_events[-1]["required_action"] in ["player_action","player_decision"]:
                self._next_events = next_events
                self.history += next_events
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
                next_events = next_events + [
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

                self._next_events = next_events
                self.history += next_events
                return next_events
