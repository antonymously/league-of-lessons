'''
Streamlit app
'''
import streamlit as st
from league_of_lessons.game_session import QuestionManager

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

if 'next_events' not in st.session_state:
    st.session_state.next_events = None

if 'question_manager' not in st.session_state:
    st.session_state.question_manager = QuestionManager()

def main():

    top_cols = st.columns([1 for i in range(4)])
    with top_cols[3]:
        option = st.selectbox(
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
        if st.button("New Game", use_container_width=True):
            st.switch_page("pages/gameplay.py")

        if st.button("Continue Game", 
            disabled = (st.session_state.game_state is None), 
            use_container_width=True
        ):
            st.switch_page("pages/gameplay.py")

        if st.button("Manage Questions", use_container_width=True):
            st.switch_page("pages/manage_questions.py")

        if st.button("Manage API Keys", use_container_width=True):
            st.switch_page("pages/manage_api_keys.py")

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