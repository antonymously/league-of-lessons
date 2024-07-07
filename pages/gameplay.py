import streamlit as st
from textwrap import dedent
from typing import Optional
from copy import copy
from league_of_lessons.game_session import GameSession
from league_of_lessons.utils import fake_stream_text

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

# add in initial components
game_container = st.container()

with game_container:
    image_container = st.empty()

with image_container:
    st.image("./assets/placeholder.png")

with game_container:
    answer_assessment_container = st.empty()
    story_container = st.empty()
    question_container = st.empty()
    input_container = st.empty()

bottom_cols = st.columns([1 for i in range(4)])

with bottom_cols[0]:
    if st.button("History", disabled = True, use_container_width=True):
        pass

with bottom_cols[2]:
    # NOTE: replace with on_click syntax when passing arguments
    if st.button("Save Game", use_container_width=True):
        pass

with bottom_cols[3]:
    if st.button("Main Menu", use_container_width=True):
        st.switch_page("app.py")

# CSS
st.markdown("""
    <style>
    div.stVerticalBlock {
        overflow-y: scroll;
        height: 80%;
    }
    div.stButton {align:center; text-align:center}
    </style>
    """, 
    unsafe_allow_html=True
)

def display_current_game_state():
    if st.session_state.game_state is None:
        # New game, need to generate story
        apply_game_action()

    next_events = st.session_state.next_events

    # TODO: if first action is "answer_assessment"
        # display correct answer
        # display adjusted dice roll
        # that's all, the rest can be viewed in history
    answer_assessment_container.empty()
    if next_events[0]["event_type"] == "answer_assessment":
        current_question = st.session_state.question_manager.get_question(
            game_session._current_question_idx
        )[1]
        current_answer = game_session._current_answer

        with answer_assessment_container:
            assessment_details_container = st.container()

        with assessment_details_container:

            if next_events[0]["assessment"] == "Correct":
                st.write("Your answer ({}) is correct!".format(current_answer["answer"]))
            else:
                st.write("Your answer ({}) is wrong!".format(current_answer["answer"]))
                st.write(
                    "The correct answer was ({}) {}".format(
                        current_question["correct_answer"], 
                        current_question["choices"][current_question["correct_answer"]],
                    )
                )
            st.write("Your dice roll has been adjusted to {}".format(next_events[0]["adjusted_dice_roll"]))

    # display story text
    # BUG: when story text is long, if overwwrites previous text?

    story_container.empty()
    for event in next_events:
        if event["event_type"] == "story_block":
            with story_container:
                story_text = st.write_stream(
                    fake_stream_text(
                        event["story"],
                        delay = 0.01
                    )
                )

    # display required action
    if next_events[-1]["event_type"] == "required_action":
        # NOTE: dice_roll action should never get here
        # it should always go to study_question
        question_container.empty()
        if next_events[-1]["required_action"] in ["player_decision", "player_action"]:
            with question_container:
                question_text = st.write_stream(
                    fake_stream_text(
                        next_events[-1]["prompt"],
                        delay = 0.01
                    )
                )

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
                    action_input = st.text_area("", value = 'Do Something')
                    st.form_submit_button(
                        'Execute Action',
                        on_click = apply_game_action,
                        kwargs = {
                            "action": {
                                "event_type": "player_action",
                                "action": action_input,
                            }
                        }
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
                        st.write_stream(fake_stream_text(event["prompt"], delay = 0.01))
                        break

            # display initial dice roll
            for event in reversed(next_events):
                if event["event_type"] == "initial_dice_roll":
                    st.write("You rolled an initial value of {}".format(event["rolled_value"]))
                    break

            st.write("STUDY QUESTION!")
            st.write("Answer the following question to adjust your dice roll:")
            question_text = st.write_stream(
                fake_stream_text(
                    next_events[-1]["question_text"],
                    delay = 0.01
                )
            )

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

def apply_game_action(action: Optional[dict] = None):
    print(action)

    # TODO: put loading indicator while generating

    # TODO: generate events
    if action is not None:
        next_events = game_session.next(action = action)
    else:
        if len(game_session.history) <= 0:
            # no history, new game
            next_events = game_session.next(action = action)
        else:
            next_events = st.session_state.next_events

    # TODO: remove loading indicator

    # TODO: update game_state
    st.session_state.game_state = game_session.get_game_state()
    st.session_state.next_events = next_events

def main():
    display_current_game_state()
    
main()