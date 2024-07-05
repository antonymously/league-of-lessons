import streamlit as st

st.set_page_config(
    page_title = "League of Lessons",
    page_icon = ":grey_question:",
    initial_sidebar_state = "collapsed",
)

def main():
    st.title("Current Question Set")
    st.write("<Manage Questions>")

    if st.button("Main Menu"):
        st.switch_page("app.py")

main()