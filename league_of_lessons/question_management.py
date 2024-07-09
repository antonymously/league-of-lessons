import pickle
import json
import numpy as np
from league_of_lessons.question_generation.multiple_choice import generate_multiple_choice_questions

class QuestionManager:

    def __init__(self):
        self.n_questions = 0
        self.name = "question_set"
        self.question_enabled = None

    def set_name(self, name):
        self.name = name
    
    def set_study_material(self, filepath, n_questions_request = 10):
        '''
        Generates questions using the study material in preparation for gameplay.
        '''
        self.study_material_filepath = filepath
        with open(filepath, "r") as f:
            self._set_study_material(f, n_questions_request = n_questions_request)

    def _set_study_material(self, file_like, n_questions_request = 10):
        study_material_txt = file_like.read()

        self.question_set = generate_multiple_choice_questions(
            study_material_txt,
            n_questions = n_questions_request,
        )

        # NOTE: the LLM may end up producing a different number of questions
        self.n_questions = len(self.question_set)

        # NOTE: all questions enabled by default
        self.question_enabled = [1 for i in range(self.n_questions)]

    def get_question(self, question_idx: int = None):
        '''
        Returns the index of the question and the question itself.
        '''
        # TODO: include enabled questions only

        if question_idx is None:
            question_idx = np.random.randint(0, self.n_questions)
        
        return question_idx, self.question_set[question_idx]

    def enable_question(self, question_idx):
        self.question_enabled[question_idx] = 1

    def disable_question(self, question_idx):
        self.question_enabled[question_idx] = 0

    def save_questions(self, filepath):
        # NOTE: use pickle so the student can't open the file and view the answers
        with open(filepath, "wb") as f:
            pickle.dump(self.question_set, f)
    
    def load_questions(self, filepath):
        with open(filepath, "rb") as f:
            self.question_set = pickle.load(f)

        self.n_questions = len(self.question_set)

    def save_state(
        self, 
        question_set_filepath,
        state_filepath,
    ):
        self.save_questions(question_set_filepath)

        state = {
            "name": self.name,
            "question_enabled": self.question_enabled,
        }

        with open(state_filepath, "w") as f:
            json.dump(state, f)

    def load_state(
        self, 
        question_set_filepath,
        state_filepath,
    ):
        self.load_questions(question_set_filepath)

        with open(state_filepath, "r") as f:
            state = json.load(f)

        self.name = state["name"]
        self.question_enabled = state["question_enabled"]
        if len(self.question_enabled) <= 0:
            # if no labels yet, just enable all questions
            self.question_enabled = [1 for i in range(self.n_questions)]