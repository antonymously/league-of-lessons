import streamlit as st

st.set_page_config(
    page_title = "League of Lessons",
    page_icon = ":video_game:",
    initial_sidebar_state = "collapsed",
)

def main():
    st.title("League of Lessons")
    st.write("<Gameplay>")

    if st.button("Main Menu"):
        st.switch_page("app.py")

main()