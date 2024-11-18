"""This module contains handler functions for the different stages of the app.

Each handler function is responsible for rendering the UI for a specific stage of the app.
Each handler function should be named handle_<stage_name> and accept no arguments.
e.g. handle_start, handle_user_preferences, handle_retrieve_suggestions, etc.

Example:
    def handle_start():
        st.title('Welcome to HolidayMatch')
        st.write('Your AI-powered travel assistant!')
"""
import streamlit as st

from features.matcher import Matcher
from features.travelagent.destination import Destination
from lib.states import Stage

# Get the app state from the session state
if "app_state" not in st.session_state:
    st.error("App state not found. Please restart the app.")
    st.stop()
app_state = st.session_state.app_state

# Get the travel agent instance from the session state
if "travel_agent_instance" not in st.session_state:
    st.error("Travel agent instance not found. Please restart the app.")
travel_agent = st.session_state.travel_agent_instance



def update_ui():
    """Render the UI for the current stage."""
    st.rerun() # Rerun the app to render the next stage. This is necessary to update the UI because of Streamlits rerun behavior when interacting with input widgets.

def handle_start():
    """Render the UI for the start stage."""
    # Welcome Message
    st.title("✈️ Welcome to HolidayMatch!")
    st.write("Your AI-powered travel planning assistant! Let's find your perfect holiday destination based on your preferences.")

    # Divider for visual separation
    st.divider()

    # User Info Input
    st.subheader("Before we start, what's your name?")
    name = st.text_input("Enter your name")

    # Intro Message After Name Input
    st.subheader(f"Nice to meet you, {name}!")
    st.write("We'll ask you a few questions to find your ideal holiday destination. Ready? Let's go!")

    # Add a "Next" button if you want to proceed to the next step
    if st.button("Next"):
        app_state.stage = Stage.USER_PREFERENCES
        st.session_state.app_state = app_state
        update_ui()

def handle_user_preferences():
    """Render the UI for the user preferences stage."""
    st.title('User Preferences')
    st.write('Please provide your travel preferences.')
    # Get user input
    # This is only a temporary solution until the preference builder is implemented
    user_input = st.text_area("Enter your message", "")
    if st.button('Get suggestions'):
        app_state.user_preferences = user_input
        with st.spinner("Retrieving answer..."):
            destination_recommendations = travel_agent.get_travel_recommendations(user_input)
            if destination_recommendations:
                # Create a new matcher
                matcher = Matcher(destination_recommendations)
                st.session_state.matcher = matcher

                # Update the application state stage
                app_state.stage = Stage.MATCHER
                st.session_state.app_state = app_state
        update_ui()

def handle_matcher():
    """Render the UI for the matching stage."""
    if "matcher" not in st.session_state:
        st.error("Matcher not found. Please restart the app.")
        st.stop()
    matcher = st.session_state.matcher

    st.title('Matcher')
    st.write('Matching your preferences with the best destinations...')

    st.info(f"Current index: {matcher.get_index()}. Total suggestions: {matcher.get_recommendations_count()}")

    suggestion: Destination | None = matcher.suggest()
    if suggestion:
        st.subheader(suggestion.name)
        st.write(suggestion.description)
        st.write(suggestion.travel_tips)

        if st.button("Like"):
            app_state.matched_destination = suggestion
            app_state.stage = Stage.PRESENT_DETAILS
            st.session_state.app_state = app_state
            update_ui()

        if st.button("Dislike"):
            matcher.dislike()
            update_ui()

    else:
        st.write("No more suggestions. Would you like to try again?")
        if st.button("Get new suggestions"):
            with st.spinner("Retrieving new suggestions..."):
                destination_recommendations = travel_agent.get_travel_recommendations(app_state.user_preferences)
                if destination_recommendations:
                    matcher.replace_suggestions(destination_recommendations)
                    st.session_state.matcher = matcher
            update_ui()

def handle_present_details():
    destination = app_state.matched_destination
    if not destination:
        st.error("There is an error loading the destination. Please restart the app.")
        st.stop()

    st.title(f"Nice, you selected {destination.name}!")
