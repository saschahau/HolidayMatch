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

def handle_start():
    """Render the UI for the start stage."""
    print("Render start stage")
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
        app_state.set_stage(Stage.USER_PREFERENCES)
        st.write(app_state)
        st.session_state.app_state = app_state
        st.write(st.session_state.app_state)

def handle_user_preferences():
    """Render the UI for the user preferences stage."""
    print("Render user preferences stage")
    st.title('User Preferences')
    st.write('Please provide your travel preferences.')
    # Get user input
    # This is only a temporary solution until the preference builder is implemented
    user_input = st.text_area("Enter your message", "")

    if st.button('Get suggestions'):
        with st.spinner("Retrieving answer..."):
            response = travel_agent.get_travel_recommendations(user_input)
        st.write(response)

        st.subheader("History")
        for entry in travel_agent.responses:
            st.write(f"Q: {entry['question']}")
            st.write(entry['response'])

def handle_matcher():
    st.title('Matcher')
    st.write('Matching your preferences with the best destinations...')