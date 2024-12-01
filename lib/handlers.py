"""This module contains handler functions for the different stages of the app.

Each handler function is responsible for rendering the UI for a specific stage of the app.
Each handler function should be named handle_<stage_name> and accept no arguments.
e.g. handle_start, handle_user_preferences, handle_retrieve_suggestions, etc.

Example:
    def handle_start():
        st.title('Welcome to HolidayMatch')
        st.write('Your AI-powered travel assistant!')
"""
import pandas as pd
import streamlit as st

from features.matcher import Matcher
from features.travelagent.models import Destination, UserInfo
from lib.states import Stage
from lib.utils import get_current_plus_two_years, run_async_task, fetch_recommendations_with_images_async

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

# Function to move to the next step
def next_step():
    st.session_state["step"] += 1
    update_ui()

# Function to move to the next step
def previous_step():
    st.session_state["step"] -= 1
    update_ui()

# Function to reset the app
def reset_preferences():
    st.session_state["step"] = 1
    st.session_state["answers"] = {}

@st.fragment
def handle_start():
    """Render the UI for the start stage."""
    # Welcome Message
    st.title(":red[:material/travel_explore:]️ Welcome to HolidayMatch!")
    st.write("Your AI-powered travel planning assistant! Let's find your perfect holiday destination based on your preferences.")

    # Divider for visual separation
    st.divider()

    # User Info Input
    with st.container(border=True):
        st.subheader("Before we start, we'd like to know you better!")
        name = st.text_input("Please enter your name")
        age = st.slider("Please enter your age", 0, 120, 20)
        gender = st.pills("Gender", ["Female", "Male", "Other", "I'd rather not to say"], selection_mode='single')

        # Intro Message after user information input
        if name != "" and gender is not None:
            st.subheader(f"Nice to meet you, {name}!")
            st.write("We'll ask you a few questions to find your ideal holiday destination. Ready? ")
            # Store the user information into the app state
            app_state.user_info = UserInfo(name=name, age=age, gender=gender)        

        # Add a "Next" button if you want to proceed to the next step
        # Disable the button as long as no user information is provided
        button_disabled = True if (not name or gender is None) else False
        if st.button("Let's go!", icon=":material/start:", disabled=button_disabled):
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
    if "answers" not in st.session_state:
        st.session_state["answers"] = {}  # Stores the answers for each criterion

    # Questions and criteria
    question_groups = [
        {
            "title": "When",
            "questions": [
                {
                    "title": "Travel Duration",
                    "question": "How long would you like to travel?",
                    "type": "radio",
                    "options": ["1-3 days", "4-7 days", "Longer than 1 week", "Other"]
                },
                {
                    "title": "Year",
                    "question": "Which year would you like to travel?",
                    "type": "pills::single",
                    "options": get_current_plus_two_years()
                },
                {
                    "title": "Month",
                    "question": "Which month would you like to travel?",
                    "type": "pills::multi",
                    "options": ["January", "February", "March", "April", "May", "June",
                                "July", "August", "September", "October", "November", "December"]
                },
            ]
        },
        {
            "title": "What",
            "questions": [
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
            ]
        },
        {
            "title": "Where",
            "questions": [
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
            ]
        },
        {
            "title": "How",
            "questions": [
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
                    "question": "How much would you like to spend for transportation and the accommodation?",
                    "description": "Select your budget range",
                    "type": "radio",
                    "options": ["Under CHF 500", "CHF 500 - CHF 1000", "CHF 1000 - CHF 2500", "More than CHF 2500"]
                }
            ]
        }
    ]

    # Display the current question based on the step
    current_step = st.session_state["step"]

    with st.container(border=True):
        if current_step <= len(question_groups):
            group = question_groups[current_step - 1]
            st.header(f"Step {current_step}: {group['title']}")
            st.write()
            st.divider()

            # Iterate through the questions in the group and collect the answers
            for question in group['questions']:
                st.subheader(question["question"])

                # Display the input type based on "type"
                if question["type"] == "radio":
                    answer = st.radio("Choose an option:", question["options"], index=0, key=f"{question['title']}_{current_step}")
                elif question["type"] == "multiselect":
                    answer = st.multiselect("Choose one or more options:", question["options"], key=f"{question['title']}_{current_step}")
                elif question["type"].startswith("pills"):
                    selection_mode = question["type"].split("::")[1]
                    answer = st.pills("Choose one or more options:", question["options"], selection_mode=selection_mode, key=f"{question['title']}_{current_step}")

                # Store the answer into the session state
                st.session_state["answers"][question["title"]] = answer

            st.divider()
            # "Next" button
            if st.button("Next"):
                # Save the answer
                next_step()

        # Summary or completion
        elif current_step == len(question_groups) + 1:
            st.header("Summary")
            st.write("Please review your answers before proceeding.")

            # Display user information
            st.subheader("User Information")
            st.write(f"**Name**: {app_state.user_info.name}")
            st.write(f"**Age**: {app_state.user_info.age}")
            st.write(f"**Gender**: {app_state.user_info.gender}")

            # Display the answers
            st.subheader("Preferences")
            st.write("Here are your answers:")
            for key, value in st.session_state["answers"].items():
                # Show in a 2-column layout
                col_1, col_2 = st.columns([0.3, 0.7])
                with col_1:
                    st.write(f"**{key}**")
                with col_2:
                    if isinstance(value, list):
                        st.write(", ".join(value))
                    elif isinstance(value, int):
                        st.write(str(value))
                    else:
                        st.write(value)

            # Show the buttons in a 2-column layout
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Restart", use_container_width=True):
                    # Reset the user preferences and start over
                    reset_preferences()

            with col2:
                if st.button('Get suggestions', type="primary", icon=":material/model_training:", use_container_width=True):
                    # Store the user preferences in the app state
                    app_state.user_preferences = st.session_state["answers"].items()

                    # Update the application state stage
                    app_state.stage = Stage.RETRIEVE_SUGGESTIONS

                    # Show a spinner while fetching the suggestions
                    with st.spinner("Finding travel recommendations for you..."):                        
                        # Get travel recommendations based on the user preferences
                        destination_recommendations = travel_agent.get_travel_recommendations(
                            preferences=st.session_state["answers"].items(),
                            user_information=app_state.user_info
                        )

                        # Ensure that results exist
                        if destination_recommendations:
                            # Fetch images for the destinations asynchronously
                            run_async_task(fetch_recommendations_with_images_async, travel_agent, destination_recommendations)

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

    # Get a destination suggestion from the matcher
    suggestion: Destination | None = matcher.suggest()
    if suggestion:
        # Create a container for the suggestions
        with st.container(border=True):
            # Display the image for the location
            if suggestion.image_url:
                st.image(suggestion.image_url)

            # Show destination information retrieved from the recommendation engine
            st.subheader(suggestion.name)
            st.write(suggestion.description)
            st.markdown("##### What you'd like to know:")
            st.markdown(f"**Travel tips**: {suggestion.travel_tips}")
            st.markdown(f"**Activities**: {", ".join(suggestion.activities)}")
            st.markdown(f"**Language**: {suggestion.language}")
            st.markdown(f"**Best time to visit**: {", ".join(suggestion.best_time_to_visit)}")
            st.markdown(f"**Transportation**: {", ".join(suggestion.transportation)}")

            # Show the buttons in a 2-column layout
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Dislike", icon=":material/swipe_left:" , use_container_width=True):
                    # Call the dislike method of the matcher, which will add the current location to the disliked ones.
                    # With the disliked options it is ensured, that the recommendation engine will not present them
                    # again if the user did not like any of the options and retrieves a new list of options.
                    matcher.dislike()

                    # Update the UI to show the next suggestion.
                    update_ui()
            with col2:
                if st.button("Like", type="primary", icon=":material/swipe_right:",  use_container_width=True):
                    # Set the destination in the app state and update the stage
                    app_state.matched_destination = suggestion
                    app_state.stage = Stage.PRESENT_DETAILS

                    # Store the updated app state into the session.
                    st.session_state.app_state = app_state

                    # Update the UI to show the details about the location.
                    update_ui()
    else:
        # The user did not like any of the suggestions that have been presented to him.
        st.write("No more suggestions. Would you like to try again?")

        # Provide the option to retrieve new suggestions.
        if st.button("Get new suggestions"):
            with st.spinner("Retrieving new suggestions..."):
                # Generate a new set of recommendations but exclude the ones that the user did not like
                destination_recommendations = travel_agent.get_travel_recommendations(
                    preferences = app_state.user_preferences,
                    user_information=app_state.user_info,
                    exclude_destinations = matcher.disliked_destinations)
                if destination_recommendations:
                    matcher.replace_suggestions(destination_recommendations)
                    st.session_state.matcher = matcher
            update_ui()

@st.fragment
def handle_present_details():
    # Load the matched destination
    destination = app_state.matched_destination
    if not destination:
        st.error("There is an error loading the destination. Please restart the app.")
        st.stop()

    # Make use of the helper function 'run_async_task' to retrieve the location details.
    location_details = run_async_task(travel_agent.get_location_details_async, destination.name)

    st.title(f"Nice, it's a match: {destination.name}!")
    st.write(location_details["latitude"], location_details["longitude"])

    # Display the image for the location
    st.image(destination.image_url)

    # Use tabs to improve the organization of the content
    tabs = ["Overview", "Your Trip"]
    tab1, tab2 = st.tabs(tabs)

    with tab1:
        with st.spinner("Generating destination overview..."):
            # Retrieve a destination summary from the recommendation engine.
            destination_overview = travel_agent.get_location_overview(destination.name,
                                                                      preferences=app_state.user_preferences,
                                                                      user_information=app_state.user_info
                                                                      )
            destination_overview = destination_overview.strip()
        st.markdown(destination_overview, unsafe_allow_html=True)

    with tab2:
        st.header("Your trip")
        st.write("All information relevant to your trip.")

        st.subheader("Weather")
        # Mock temperature data for Ibiza for the months of June, July, and August
        temperature_data = {
            "Day": list(range(1, 32)),  # Assuming 31 days for each month
            "July": [28 + (i % 2) for i in range(31)],  # Example data for July
        }

        # Convert the data into a DataFrame
        df = pd.DataFrame(temperature_data)

        # Streamlit Line Chart
        st.write(f"**Temperature Data prediction for {destination.name}**")
        st.line_chart(df.set_index("Day"))

        st.subheader("Transportation")
        st.write("tbd...")

        st.subheader("Accommodation")
        st.write("tbd...")
