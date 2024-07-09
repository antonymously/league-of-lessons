import streamlit as st
from textwrap import dedent
from typing import Optional
from copy import copy
import pickle
import time
from league_of_lessons import SAVE_GAME_FILEPATH
from league_of_lessons.game_session import GameSession
from league_of_lessons.tts.tts import text_to_speech
from league_of_lessons.utils import fake_stream_text, history_to_text

st.set_page_config(
    page_title = "League of Lessons",
    page_icon = ":video_game:",
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

# this will work even if game_state is None
game_session = GameSession(
    question_manager = st.session_state.question_manager,
    game_state = st.session_state.game_state,
)

def save_game():
    # don't stream text when save button is clicked
    with open(SAVE_GAME_FILEPATH, "wb") as f:
        pickle.dump(game_session.get_game_state(), f)

    # don't stream text when save button is clicked
    st.session_state.stream_story = False

top_cols = st.columns([1 for i in range(4)])

with top_cols[0]:
    # NOTE: replace with on_click syntax when passing arguments
    st.button(
        "Save Game",
        on_click = save_game,
        use_container_width = True,
    )

with top_cols[1]:
    study_score_container = st.empty()
    with study_score_container:
        st.write("Study Score: {}/{}".format(*game_session._study_score))

with top_cols[3]:
    if st.button("Main Menu", use_container_width=True):
        st.switch_page("app.py")

# add in initial components
game_container = st.container()

with game_container:
    history_expander = st.expander('History')
    image_container = st.empty()

with image_container:
    st.image("./assets/placeholder.png")

with game_container:
    audio_container = st.empty()
    answer_assessment_container = st.empty()
    story_container = st.empty()
    question_container = st.empty()
    input_container = st.empty()

def display_history():
    # write history
    with history_expander:
        if len(game_session.history) <= 0:
            st.write("No history yet!")
        else:
            st.markdown(
                history_to_text(game_session.history[:-len(game_session._next_events) + 1]), 
                unsafe_allow_html=True
            )

def apply_game_action(action: Optional[dict] = None):
    if st.session_state.action_input is not None:
        action_ = {
            "event_type": "player_action",
            "action": st.session_state.action_input,
        }
    else:
        action_ = action
    print(action_)

    # TODO: put loading indicator while generating

    # generate events
    # NOTE: next events are already stored in game_session
    next_events = game_session.next(action = action_)
    
    # TODO: remove loading indicator

    # update game_state
    st.session_state.game_state = game_session.get_game_state()

    # set stream story to true
    st.session_state.stream_story = True

def display_current_game_state():

    st.session_state.action_input = None

    # display history before the game action
        # so it does not include the new story block
    display_history()

    if st.session_state.game_state is None:
        # New game, need to generate story
        apply_game_action()
    
    next_events = game_session._next_events

    # if first action is "answer_assessment"
        # display correct answer
        # display adjusted dice roll
        # that's all, the rest can be viewed in history
    answer_assessment_container.empty()
    if next_events[1]["event_type"] == "answer_assessment":
        assessment_event = next_events[1]
        current_answer = game_session._current_answer
        current_question = st.session_state.question_manager.get_question(
            current_answer["question_idx"]
        )[1]
        
        with answer_assessment_container:
            assessment_details_container = st.container()

        with assessment_details_container:

            if assessment_event["assessment"] == "Correct":
                st.write("Your answer ({}) is correct!".format(current_answer["answer"]))
            else:
                st.write("Your answer ({}) is wrong!".format(current_answer["answer"]))
                st.write(
                    "The correct answer was ({}) {}".format(
                        current_question["correct_answer"], 
                        current_question["choices"][current_question["correct_answer"]],
                    )
                )
            st.write("Your dice roll has been adjusted to {}".format(assessment_event["adjusted_dice_roll"]))

    # display story text
    story_container.empty()
    for event in next_events:
        if event["event_type"] == "story_block":

            # generate the narration
            # TODO: can this be done async while streaming story?
            # TODO: save this to game state
            if st.session_state.stream_story:
                narration_audio = text_to_speech(event["story"])
                with audio_container:
                    st.audio(
                        narration_audio,
                        loop = False,
                        autoplay = True,
                    )
            else:
                # TEMP: no audio when load game
                pass

            with story_container:
                if st.session_state.stream_story:
                    story_text = st.write_stream(
                        fake_stream_text(
                            event["story"],
                            delay = 0.01
                        )
                    )
                else:
                    story_text = st.write(event["story"])

    # display required action
    if next_events[-1]["event_type"] == "required_action":
        # NOTE: dice_roll action should never get here
        # it should always go to study_question
        question_container.empty()
        if next_events[-1]["required_action"] in ["player_decision", "player_action"]:
            with question_container:
                if st.session_state.stream_story:
                    question_text = st.write_stream(
                        fake_stream_text(
                            next_events[-1]["prompt"],
                            delay = 0.01
                        )
                    )
                else:
                    question_text = st.write(next_events[-1]["prompt"])

        if next_events[-1]["required_action"] == "player_decision":
            # display choices
            input_container.empty()
            with input_container:
                choices_container = st.container()

            with choices_container:
                for key, choice in next_events[-1]["choices"].items():
                    st.button(
                        f"{key}. {choice}",
                        on_click = apply_game_action,
                        use_container_width = True,
                        kwargs = {
                            "action": {
                                "event_type": "player_decision",
                                "choice": key,
                            }
                        }
                    )

        elif next_events[-1]["required_action"] == "player_action":
            # display input box and execute button
            input_container.empty()
            with input_container:
                action_input_container = st.container()

            with action_input_container:
                with st.form('Player Action'):
                    action_input = st.text_area(
                        "Your Action", 
                        label_visibility = "collapsed",
                        placeholder = 'Do Something', 
                        key = 'action_input'
                    )
                    # NOTE: recommended approach here is to access session state variable
                        # in the callback function
                        # instead of adding it as args/kwargs here
                    submit_button = st.form_submit_button(
                        'Execute Action',
                        on_click = apply_game_action,
                    )

    elif next_events[-1]["event_type"] == "study_question":
        # NOTE: will need to modify this for other question types
        question_container.empty()
        with question_container:
            study_question_container = st.container()
        
        with study_question_container:
            # NOTE: there should be a dice roll preceding the question
            # display prompt for dice roll
            for event in reversed(next_events):
                if event["event_type"] == "required_action":
                    if event["required_action"] == "player_dice_roll":
                        if st.session_state.stream_story:
                            st.write_stream(fake_stream_text(event["prompt"], delay = 0.01))
                        else:
                            st.write(event["prompt"])
                        break

            # display initial dice roll
            for event in reversed(next_events):
                if event["event_type"] == "initial_dice_roll":
                    st.write("You rolled an initial value of {}".format(event["rolled_value"]))
                    break

            st.write("STUDY QUESTION!")
            st.write("Answer the following question to adjust your dice roll:")
            if st.session_state.stream_story:
                question_text = st.write_stream(
                    fake_stream_text(
                        next_events[-1]["question_text"],
                        delay = 0.01
                    )
                )
            else:
                question_text = st.write(next_events[-1]["question_text"])

        input_container.empty()
        with input_container:
            choices_container = st.container()

        with choices_container:
            for key, choice in next_events[-1]["choices"].items():
                st.button(
                    f"{key}. {choice}",
                    on_click = apply_game_action,
                    use_container_width = True,
                    kwargs = {
                        "action": {
                            "event_type": "player_answer",
                            "answer": key,
                        }
                    }
                )

        # TODO: display image

        # TODO: add audio narration

        # TODO: display history

        # TODO: 


# CSS
st.markdown("""
    <style>
    div.stVerticalBlock {
        overflow-y: scroll;
        height: 80%;
    }
    div.stButton {align:center; text-align:center}
    div[data-testid="stMarkdownContainer"] p {
        max-height: 500px;
        overflow-y: auto;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

def main():
    display_current_game_state()
    
main()