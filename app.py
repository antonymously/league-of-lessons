'''
Streamlit app
'''
import streamlit as st

st.set_page_config(
    page_title = "League of Lessons",
    page_icon = ":bookmark_tabs:",
    initial_sidebar_state = "collapsed",
)

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
        if st.button("Start Game"):
            st.switch_page("pages/gameplay.py")

        if st.button("Manage Questions"):
            st.switch_page("pages/manage_questions.py")


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