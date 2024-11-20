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

@st.fragment
def handle_start():
    """Render the UI for the start stage."""
    # Welcome Message
    st.title("✈️ Welcome to HolidayMatch!")
    st.write("Your AI-powered travel planning assistant! Let's find your perfect holiday destination based on your preferences.")

    # Divider for visual separation
    st.divider()

    start_container = st.container()
    # User Info Input
    st.subheader("Before we start, what's your name?")
    name = st.text_input("Please enter your name")

    if name != "":
        with st.container(border=True):
            # Intro Message After Name Input
            st.subheader(f"Nice to meet you, {name}!")
            st.write("We'll ask you a few questions to find your ideal holiday destination. Ready? ")

            # Add a "Next" button if you want to proceed to the next step
            if st.button("Let's go!", icon=":material/start:"):
                app_state.stage = Stage.USER_PREFERENCES
                st.session_state.app_state = app_state
                update_ui()

@st.fragment
def handle_user_preferences():
    """Render the UI for the user preferences stage."""
    st.title('User Preferences')
    st.write('Please provide your travel preferences.')
    # Get user input

    # Initialize Session State for step management
    if "step" not in st.session_state:
        st.session_state["step"] = 1
        st.session_state["answers"] = {}  # Stores the answers for each criterion

    # Function to move to the next step
    def next_step():
        st.session_state["step"] += 1
        update_ui()

    # Function to reset the app
    def reset_app():
        st.session_state["step"] = 1
        st.session_state["answers"] = {}

    # Questions and criteria
    questions = [
        {
            "title": "Travel Duration",
            "question": "How long would you like to travel?",
            "type": "radio",
            "options": ["1-3 days", "4-7 days", "Longer than 1 week", "Other"]
        },
        {
            "title": "Type of Trip",
            "question": "What type of trip do you prefer?",
            "type": "multiselect",
            "options": ["City trip", "Beach vacation", "Hiking vacation",
                        "General sports vacation", "Relaxation / SPA vacation",
                        "Ski vacation / Après-ski"]
        },
        {
            "title": "Interests",
            "question": "What would you like to do most during your trip?",
            "type": "multiselect",
            "options": ["Culture / Museums", "Hiking / Nature", "Beach / Relaxation", "Party", "Adventure"]
        },
        {
            "title": "Month",
            "question": "Which month would you like to travel?",
            "type": "multiselect",
            "options": ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"]
        },
        {
            "title": "Climate",
            "question": "Do you prefer warm or cooler weather?",
            "type": "radio",
            "options": ["Cool < 10°C", "Warm > 20°C", "Very warm > 30°C", "Doesn’t matter"]
        },
        {
            "title": "Destination",
            "question": "Where would you like to travel?",
            "type": "radio",
            "options": ["Stay in Europe", "North America", "South America", "Asia",
                        "Africa", "Australia / Oceania", "Doesn’t matter"]
        },
        {
            "title": "Travel Companions",
            "question": "Who will you be traveling with?",
            "type": "radio",
            "options": ["Solo", "Couple", "Family (with children)", "Friends", "Group"]
        },
        {
            "title": "Accommodation Preferences",
            "question": "What type of accommodation do you prefer?",
            "type": "radio",
            "options": ["Hotel", "Vacation Rental (Airbnb, etc.)", "Hostel",
                        "Resort", "Camping", "Doesn’t matter"]
        },
        {
            "title": "Budget",
            "question": "How much would you like to spend on the entire trip?",
            "type": "radio",
            "options": ["Under CHF 500", "CHF 500 - CHF 1000", "CHF 1000 - CHF 2500", "More than CHF 2500"]
        }
    ]

    # Display the current question based on the step
    current_step = st.session_state["step"]

    with st.container(border=True):
        if current_step <= len(questions):
            question = questions[current_step - 1]
            st.header(f"Step {current_step}: {question['title']}")
            st.write(question["question"])

            # Display the input type based on "type"
            if question["type"] == "radio":
                answer = st.radio("Choose an option:", question["options"], index=0)
            elif question["type"] == "multiselect":
                answer = st.multiselect("Choose one or more options:", question["options"])

            # "Next" button
            if st.button("Next"):
                # Save the answer
                st.session_state["answers"][question["title"]] = answer
                next_step()

        # Summary or completion
        elif current_step == len(questions) + 1:
            st.header("Summary")
            st.write("Here are your answers:")
            for key, value in st.session_state["answers"].items():
                st.write(f"*{key}:* {value}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Restart", use_container_width=True):
                    reset_app()

            with col2:
                # This is only a temporary solution until the preference builder is implemented
                # user_input = st.text_area("Enter your message", "")
                if st.button('Get suggestions', type="primary", icon=":material/model_training:", use_container_width=True):
                    app_state.user_preferences = st.session_state["answers"].items()
                    with st.spinner("Retrieving answer..."):
                        destination_recommendations = travel_agent.get_travel_recommendations(st.session_state["answers"].items())
                        if destination_recommendations:
                            # Create a new matcher
                            matcher = Matcher(destination_recommendations)
                            st.session_state.matcher = matcher

                            # Update the application state stage
                            app_state.stage = Stage.MATCHER
                            st.session_state.app_state = app_state
                    update_ui()

@st.fragment
def handle_matcher():
    """Render the UI for the matching stage."""
    if "matcher" not in st.session_state:
        st.error("Matcher not found. Please restart the app.")
        st.stop()
    matcher = st.session_state.matcher

    st.title('We have the following suggestions for you')
    st.write('Matching your preferences with the best destinations...')

    suggestion: Destination | None = matcher.suggest()
    if suggestion:
        # st.write(suggestion)
        # Create a container for the suggestions
        with st.container(border=True):
            st.subheader(suggestion.name)
            st.write(suggestion.description)
            st.markdown("##### What you'd like to know:")
            st.markdown(f"**Travel tips**: {suggestion.travel_tips}")
            st.markdown(f"**Activities**: {", ".join(suggestion.activities)}")
            st.markdown(f"**Language**: {suggestion.language}")
            st.markdown(f"**Best time to visit**: {", ".join(suggestion.best_time_to_visit)}")
            st.markdown(f"**Transportation**: {", ".join(suggestion.transportation)}")
            if suggestion.image_url:
                st.image(suggestion.image_url)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Dislike", icon=":material/swipe_left:" , use_container_width=True):
                    matcher.dislike()
                    update_ui()

            with col2:
                if st.button("Like", type="primary", icon=":material/swipe_right:",  use_container_width=True):
                    app_state.matched_destination = suggestion
                    app_state.stage = Stage.PRESENT_DETAILS
                    st.session_state.app_state = app_state
                    update_ui()

    else:
        st.write("No more suggestions. Would you like to try again?")
        if st.button("Get new suggestions"):
            with st.spinner("Retrieving new suggestions..."):
                # Generate a new set of recommendations but exclude the ones that the user did not like
                destination_recommendations = travel_agent.get_travel_recommendations(
                    app_state.user_preferences,
                    exclude_destinations = matcher.disliked_destinations)
                if destination_recommendations:
                    matcher.replace_suggestions(destination_recommendations)
                    st.session_state.matcher = matcher
            update_ui()

@st.fragment
def handle_present_details():
    destination = app_state.matched_destination
    if not destination:
        st.error("There is an error loading the destination. Please restart the app.")
        st.stop()

    st.title(f"Nice, you selected {destination.name}!")
    st.image("https://www.spain.info/.content/imagenes/cabeceras-grandes/baleares/ibiza-cala-s1534753385.jpg")

    tabs = ["Overview", "Hotels", "Flights"]

    tab1, tab2, tab3 = st.tabs(tabs)

    with tab1:
        st.header("Overview")
        st.markdown("Some text...")

    with tab2:
        st.header("Hotels")
        st.markdown("Some text...")

    with tab3:
        st.header("Flights")
        st.markdown("Some text...")
