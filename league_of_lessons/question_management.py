import pickle
import numpy as np
from league_of_lessons.question_generation.multiple_choice import generate_multiple_choice_questions

class QuestionManager:

    def __init__(self, n_questions_request: int = 30):
        self.n_questions_request = n_questions_request
        self.n_questions = 0
    
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
            question_idx = np.random.randint(0, self.n_questions)
        
        return question_idx, self.question_set[question_idx]

    def save_questions(self, filepath):
        # NOTE: use pickle so the student can't open the file and view the answers
        with open(filepath, "wb") as f:
            pickle.dump(self.question_set, f)
    
    def load_questions(self, filepath):
        with open(filepath, "rb") as f:
            self.question_set = pickle.load(f)

        self.n_questions = len(self.question_set)