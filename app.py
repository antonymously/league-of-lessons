'''
Streamlit app
'''
import os
import streamlit as st
import pickle
from league_of_lessons import SAVE_GAME_FILEPATH
from league_of_lessons.question_management import QuestionManager

st.set_page_config(
    page_title = "League of Lessons",
    page_icon = ":bookmark_tabs:",
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

# Initialize session state variables
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = 'teacher'

if 'game_state' not in st.session_state:
    st.session_state.game_state = None

if 'stream_story' not in st.session_state:
    # NOTE: on certain interactions, we don't want to stream
    st.session_state.stream_story = True

if 'question_manager' not in st.session_state:
    st.session_state.question_manager = QuestionManager()

st.session_state.questions_file = "./data/question_set.pkl"
st.session_state.questions_state_file = "./data/questions_state.json"
if os.path.exists(st.session_state.questions_file):
    st.session_state.question_manager.load_state(
        st.session_state.questions_file,
        st.session_state.questions_state_file,
    )
    st.session_state.question_set_available = True
else:
    st.session_state.question_set_available = False

def main():

    top_cols = st.columns([1 for i in range(4)])
    with top_cols[3]:
        viewer_role = st.selectbox(
            "Viewing as:",
            (
                "Teacher",
                "Student",
            )
        )

    title_container = st.container()
    with title_container:
        st.markdown(
            "<h1>League of Lessons</h1>", 
            unsafe_allow_html=True
        )

    mid_cols = st.columns([1 for i in range(3)])

    with mid_cols[1]:
        if st.button(
            "New Game", 
            use_container_width=True,
            disabled = (not st.session_state.question_set_available),
        ):
            st.session_state.game_state = None
            st.switch_page("pages/gameplay.py")

        if st.button("Continue Game", 
            disabled = ((not os.path.exists(SAVE_GAME_FILEPATH)) or (not st.session_state.question_set_available)), 
            use_container_width=True
        ):
            with open(SAVE_GAME_FILEPATH, "rb") as f:
                st.session_state.game_state = pickle.load(f)
            
            st.switch_page("pages/gameplay.py")

        if viewer_role == "Teacher":
            if st.button("Manage Questions", use_container_width=True):
                # load question manager state before switching page
                if st.session_state.question_set_available:
                    st.session_state.question_manager.load_state(
                        st.session_state.questions_file,
                        st.session_state.questions_state_file,
                    )
                st.switch_page("pages/manage_questions.py")

            if st.button("Manage API Keys", use_container_width=True):
                st.switch_page("pages/manage_api_keys.py")
        else:
            if st.session_state.question_set_available:
                st.write("Assigned Question Set: {}".format(st.session_state.question_manager.name))
            else:
                st.write("No assigned question set")

    # CSS
    st.markdown("""
        <style>
        h1 {text-align: center; color: grey;}
        div.stButton {text-align:center}
        </style>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()