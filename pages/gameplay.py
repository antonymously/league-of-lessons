import streamlit as st
from textwrap import dedent
from league_of_lessons.game_session import GameSession

st.set_page_config(
    page_title = "League of Lessons",
    page_icon = ":video_game:",
    initial_sidebar_state = "collapsed",
)

# this will work even if game_state is None
game_session = GameSession(
    question_manager = st.session_state.question_manager,
    game_state = st.session_state.game_state,
)

def main():
    image_container = st.container()

    with image_container:
        st.image("./assets/placeholder.png")

    story_container = st.container()

    with story_container:
        st.markdown(dedent('''Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
            nisi ut aliquip ex ea commodo consequat.'''
        ))

    bottom_cols = st.columns([1 for i in range(4)])
    with bottom_cols[3]:
        if st.button("Main Menu"):
            st.switch_page("app.py")

    # CSS
    st.markdown("""
        <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        div.stButton {align:center; text-align:center}
        """, 
        unsafe_allow_html=True
    )

main()