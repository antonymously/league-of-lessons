import streamlit as st

st.set_page_config(
    page_title = "League of Lessons",
    page_icon = ":key:",
    initial_sidebar_state = "collapsed",
)

def main():
    st.title("Manage API Keys")
    st.write("<API keys>")

    if st.button("Main Menu"):
        st.switch_page("app.py")

main()