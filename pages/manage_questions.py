import os
import streamlit as st
from copy import copy
from pathlib import Path
import io
from league_of_lessons.ingest.pdf import load_pdf_document
from league_of_lessons import SAVE_GAME_FILEPATH

st.set_page_config(
    page_title = "League of Lessons",
    page_icon = ":grey_question:",
    initial_sidebar_state = "collapsed",
)

# hide sidebar immediately
st.markdown("""
    <style>
    [data-testid="collapsedControl"] {
        display: none
    }
    </style>
    """, 
    unsafe_allow_html=True
)

top_cols = st.columns([1 for i in range(4)])

def save_questions():
    # save all changes made
    st.session_state.question_manager.set_name(
        st.session_state.question_set_new_name
    )

    for q_idx, question in enumerate(st.session_state.question_manager.question_set):
        st.session_state.question_manager.question_enabled[q_idx] = st.session_state['q_enabled_' + str(q_idx)]

        # state stores the actual value, not the index
        correct_key = st.session_state['q_ans_' + str(q_idx)][0]

        st.session_state.question_manager.question_set[q_idx]["correct_answer"] = correct_key

    st.session_state.question_manager.save_state(
        st.session_state.questions_file,
        st.session_state.questions_state_file,
    )

    # when changes to question set are saved
    # just delete saved game state to avoid bugs
    if os.path.exists(SAVE_GAME_FILEPATH):
        os.remove(SAVE_GAME_FILEPATH)

with top_cols[3]:
    if st.button("Main Menu", use_container_width=True):
        st.switch_page("app.py")

def display_question_management():

    st.title("Manage Question Set")

    # Upload Study Material
    study_material_uploader = st.file_uploader(
        "Upload Study Material",
        type = ['txt', 'pdf'],
        key = 'study_material_file',
    )

    def regenerate_questions():
        # check file extension
        file_extension = Path(study_material_uploader.name).suffix

        if file_extension == ".txt":
            # it can be used as a file-like object
            st.session_state.question_manager._set_study_material(
                study_material_uploader,
                n_questions_request = st.session_state.n_questions_request,
            )

        elif file_extension == ".pdf":
            text_study_material = load_pdf_document(study_material_uploader)
            st.session_state.question_manager._set_study_material(
                io.StringIO(text_study_material),
                n_questions_request = st.session_state.n_questions_request,
            )

        st.session_state.question_set_available = True
        st.session_state.question_manager.save_state(
            st.session_state.questions_file,
            st.session_state.questions_state_file,
        )

    generation_cols = st.columns([1,2])
    with generation_cols[0]:
        # Regenerate Questions
        regenerate_button = st.button(
            'Regenerate Questions',
            disabled = (study_material_uploader is None),
            on_click = regenerate_questions,
        )
    with generation_cols[1]:
        n_questions_request = st.number_input(
            'Number of Questions to Generate',
            min_value = 1,
            max_value = 50,
            value = 10,
            step = 1,
            key = 'n_questions_request',
        )

    # Question List
        # with check-boxes for inclusion
        # indicate correct answer (radio)
        # OPTIONAL: allow text edit of questions
        # OPTIONAL: allow to add new questions
    questions_container = st.empty()

    if not st.session_state.question_set_available:
        return

    questions_container.empty()
    with questions_container:
        questions_sub_container = st.form(
            'Question Set',
            border = True,
        )

    with questions_sub_container:
        submit_button = st.form_submit_button(
            'Save Changes',
            on_click = save_questions,
        )

        # Question Set Name
        question_set_name_input = st.text_input(
            "Question Set Name",
            value = st.session_state.question_manager.name,
            key = 'question_set_new_name',
        )

        st.write("Questions:")

        for q_idx, question in enumerate(st.session_state.question_manager.question_set):
            q_key = 'q_enabled_' + str(q_idx)
            st.checkbox(
                question["question_text"],
                value = st.session_state.question_manager.question_enabled[q_idx],
                key = q_key,
            )

            options = [
                f"{key}. {choice}" for key, choice in sorted(question["choices"].items())
            ]
            keys = list(sorted(question["choices"].keys()))
            ans_index = keys.index(question["correct_answer"])

            qa_key = 'q_ans_' + str(q_idx)
            # NOTE: how to indent these choices?
            st.radio(
                "Choices:",
                options = options,
                index = ans_index,
                key = qa_key,
            )

display_question_management()