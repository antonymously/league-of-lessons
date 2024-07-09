import streamlit as st
import pickle

st.set_page_config(
    page_title = "League of Lessons",
    page_icon = ":key:",
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

with top_cols[3]:
    if st.button("Main Menu", use_container_width=True):
        st.switch_page("app.py")

def save_api_keys():
    # TODO: confirm that API keys are working

    api_keys = {
        "_anthropic_api_key": st.session_state._anthropic_api_key,
        "_openai_api_key": st.session_state._openai_api_key,
        "_pyht_user_id": st.session_state._pyht_user_id,
        "_pyht_secret": st.session_state._pyht_secret,
    }
    with open(st.session_state.api_keys_file, "wb") as f:
        pickle.dump(api_keys, f)

def display_api_key_management():
    st.title("Manage API Keys")
    
    api_keys_form = st.form(
        'API Keys',
        border = True,
    )

    with api_keys_form:
        submit_button = st.form_submit_button(
            'Save Changes',
            on_click = save_api_keys,
        )

        st.text_input(
            "Anthropic API Key",
            key = '_anthropic_api_key',
        )

        st.text_input(
            "OpenAI API Key",
            key = '_openai_api_key',
        )

        st.text_input(
            "PlayHT User ID",
            key = '_pyht_user_id',
        )

        st.text_input(
            "PlayHT Secret",
            key = '_pyht_secret',
        )

display_api_key_management()