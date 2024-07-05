import numpy as np
import math
from typing import Optional
from league_of_lessons.game_generation.coop_dnd_generation import generate_story_continuation
from league_of_lessons.question_generation.multiple_choice import generate_multiple_choice_questions

def adjust_dice_roll(dice_roll: int, dice_type: str, answer_correct: bool):
    dice_max = int(dice_type[1:])

    penalty = math.ceil(dice_max*0.25)
    bonus = math.ceil(dice_max*0.25)

    if answer_correct:
        return min(dice_roll + bonus, dice_max)
    else:
        return max(dice_roll - penalty, 1)

class QuestionManager:

    def __init__(self, n_questions_request: int = 30):
        self.n_questions_request = n_questions_request
    
    def set_study_material(self, filepath):
        '''
        Generates questions using the study material in preparation for gameplay.
        '''
        self.study_material_filepath = filepath
        with open(filepath, "r") as f:
            study_material_txt = f.read()

        self.question_set = generate_multiple_choice_questions(
            study_material_txt,
            n_questions = self.n_questions_request,
        )

        # NOTE: the LLM may end up producing a different number of questions
        self.n_questions = len(self.question_set)

    def get_question(self, question_idx: int = None):
        '''
        Returns the index of the question and the question itself.
        '''
        if question_idx is None:
            question_idx = np.random.randint(1, self.n_questions + 1)
        
        return question_idx, self.question_set[question_idx]

class GameState:
    '''
    Saves the game history, display image and audio.
    '''
    
    def __init__(self,
        history: list = [],
        img_path: Optional[str] = None,
        audio_path: Optional[str] = None,
    ):
        self.history = history
        self.img_path = img_path
        self.audio_path = audio_path

class GameSession:

    def __init__(self, question_manager: QuestionManager = None, game_state: GameState = None):

        self.question_manager = question_manager
        
        self._initial_dice_roll = None
        self._current_question_idx = None

        if game_state is None:
            self.reset()
        else:
            self.load_state(game_state = game_state)

    def reset(self):
        self.history = []
        self.img_path = None
        self.audio_path = None

    def load_state(self, game_state: GameState):
        self.history = game_state.history
        self.img_path = game_state.img_path
        self.audio_path = game_state.audio_path

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
