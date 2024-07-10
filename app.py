'''
Streamlit app
'''
import os
import streamlit as st
import pickle
from league_of_lessons import SAVE_GAME_FILEPATH, set_anthropic_api_key, set_openai_api_key
from league_of_lessons.question_management import QuestionManager
from league_of_lessons.tts.tts import set_pyht_keys

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
st.session_state.api_keys_file = "./data/api_keys.pkl"

if os.path.exists(st.session_state.questions_file):
    st.session_state.question_manager.load_state(
        st.session_state.questions_file,
        st.session_state.questions_state_file,
    )
    st.session_state.question_set_available = True
else:
    st.session_state.question_set_available = False

if os.path.exists(st.session_state.api_keys_file):
    with open(st.session_state.api_keys_file, "rb") as f:
        api_keys = pickle.load(f)
    st.session_state._anthropic_api_key = api_keys["_anthropic_api_key"]
    st.session_state._openai_api_key = api_keys["_openai_api_key"]
    st.session_state._pyht_user_id = api_keys["_pyht_user_id"]
    st.session_state._pyht_secret = api_keys["_pyht_secret"]
else:
    st.session_state._anthropic_api_key = None
    st.session_state._openai_api_key = None
    st.session_state._pyht_user_id = None
    st.session_state._pyht_secret = None

if st.session_state._anthropic_api_key is not None:
    # if anthropic API key is available from session state
    # use that instead of the one from .env
    set_anthropic_api_key(st.session_state._anthropic_api_key)

if st.session_state._openai_api_key is not None:
    # if openai API key is available from session state
    # use that instead of the one from .env
    set_openai_api_key(st.session_state._openai_api_key)

if (st.session_state._pyht_user_id is not None) and (st.session_state._pyht_secret is not None):
    # if pyht API key is available from session state
    # use that instead of the one from .env
    set_pyht_keys(
        st.session_state._pyht_user_id,
        st.session_state._pyht_secret,
    )

# make data folder if it doesn't exist
if not os.path.exists("./data"):
    os.makedirs("./data") 

def check_api_keys_available():
    key_names = [
        ('_anthropic_api_key', 'ANTHROPIC_API_KEY'),
        ('_openai_api_key', 'OPENAI_API_KEY'),
        ('_pyht_user_id', 'PYHT_USER_ID'),
        ('_pyht_secret', 'PYHT_SECRET'),
    ]
    keys_available = True
    for key_name in key_names:
        if st.session_state[key_name[0]] is not None:
            continue
        if os.getenv(key_name[1], default = None) is not None:
            continue
        keys_available = False
        break
        
    return keys_available

st.session_state.api_keys_available = check_api_keys_available()

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
            disabled = ((not st.session_state.question_set_available) or (not st.session_state.api_keys_available)),
        ):
            st.session_state.game_state = None
            st.switch_page("pages/gameplay.py")

        if st.button("Continue Game", 
            disabled = ((not os.path.exists(SAVE_GAME_FILEPATH)) or (not st.session_state.question_set_available) or (not st.session_state.api_keys_available)), 
            use_container_width=True
        ):
            with open(SAVE_GAME_FILEPATH, "rb") as f:
                st.session_state.game_state = pickle.load(f)
            # don't stream when loading game
            st.session_state.stream_story = False
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