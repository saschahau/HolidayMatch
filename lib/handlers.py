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

from components.weather_component import weather_component
from features.matcher import Matcher
from features.travelagent.models import Destination, UserInfo
from lib.states import Stage
from lib.utils import get_question_groups, run_async_task, fetch_recommendations_with_images_async

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
    """ 
    A helper function to update the UI based on the current stage.

    This function is used to update the UI after the user interacts with the app and
    uses Streamlits rerun functionality. Despite the caveats and the side effects coming with st.rerun(), 
    due to the size of the app and the limited scope, we use it here.

    Better approaches might be:
    - Using callbacks
    - Using a streamlit containter
    """
    st.rerun() # Rerun the app to render the next stage. This is necessary to update the UI because of Streamlits rerun behavior when interacting with input widgets.

def next_step():
    """Move to the next step in the user preferences stage."""
    st.session_state["step"] += 1
    update_ui()

def previous_step():
    """Move to the previous step in the user preferences stage."""
    st.session_state["step"] -= 1
    update_ui()

def reset_preferences():
    """Reset the user preferences and start over."""
    st.session_state["step"] = 1
    st.session_state["answers"] = {}

@st.fragment
def handle_start():
    """ Render the UI for the start stage. """
    # Welcome Message
    st.title(":red[:material/travel_explore:]️ Welcome to HolidayMatch!")
    st.write("Your AI-powered travel planning assistant! Let's find your perfect holiday destination based on your preferences.")

    # Divider for visual separation
    st.divider()

    # User Info Input
    with st.container(border=True):
        st.subheader("Before we start, we'd like to know you better!")
        name = st.text_input("Please enter your name")
        age = st.slider("Please enter your age", 18, 99, 20)
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
    """ Render the UI for the user preferences stage.
        
        This stage is responsible for collecting the user preferences for the travel destination.
        It consists of multiple steps, each step contains a set of questions to collect the user preferences.
        After the user has answered all questions, the travel agent will make recommendations based on the preferences.
    """
    st.title('User Preferences')
    st.write('Please provide your travel preferences.')
    # Get user input

    # Initialize Session State for step management
    if "step" not in st.session_state:
        st.session_state["step"] = 1
    if "answers" not in st.session_state:
        st.session_state["answers"] = {}  # Stores the answers for each criterion

    # Questions and criteria
    question_groups = get_question_groups()

    # Display the current question based on the step
    current_step = st.session_state["step"]

    with st.container(border=True):
        if current_step <= len(question_groups):
            group = question_groups[current_step - 1]
            st.header(f"Step {current_step}: {group['title']}")

            # Show the weather component for the "When" group to support the user
            # with with weather information for the home location.
            if group["title"] == "When":
                st.markdown("""To help you make the best decision, we provide you with the predicted weather information for your home location.
                This way, you can consider the weather conditions when planning your trip.""")
                weather_component("Zurich")

            # Divider for visual separation
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
                    update_ui()

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
    """ Render the UI for the matcher stage.

        In this stage, the matcher will suggest destinations one by one, which are retrieved from the recommendation engine.
        The user can like or dislike the suggestions. The matcher will provide new suggestions based on the user's feedback or
        move to the next stage if the user has liked a suggestion.
        If the user has disliked all suggestions, the matcher will ask the user if they want to try again.
    """
    # Ensure that the matcher is available in the session state
    # If not, show an error message and stop the app.
    if "matcher" not in st.session_state:
        st.error("Matcher not found. Please restart the app.")
        st.stop()
    matcher = st.session_state.matcher



    # Get a destination suggestion from the matcher
    suggestion: Destination | None = matcher.suggest()
    if suggestion:
        st.title('We have the following suggestions for you')
        st.write('Matching your preferences with the best destinations...')

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
        st.title("Oh no! It seems like you didn't like any of the suggestions.")
        st.write("Would you like to try again?")

        # Provide the option to retrieve new suggestions.
        if st.button("Get new suggestions"):
            with st.spinner("Retrieving new suggestions..."):
                # Generate a new set of recommendations but exclude the ones that the user did not like
                destination_recommendations = travel_agent.get_travel_recommendations(
                    preferences = app_state.user_preferences,
                    user_information=app_state.user_info,
                    exclude_destinations = matcher.disliked_destinations)
                if destination_recommendations:
                    # Fetch images for the destinations asynchronously
                    run_async_task(fetch_recommendations_with_images_async, travel_agent, destination_recommendations)

                    # Replace the suggestions in the matcher with the new suggestions
                    matcher.replace_suggestions(destination_recommendations)
                    
                    # Update the matcher in the session state
                    st.session_state.matcher = matcher

            # Update the UI to show the next suggestion
            update_ui()

@st.fragment
def handle_present_details():
    """ Render the UI for the present details stage.
    
        This stage is responsible for presenting the details of the matched destination to the user.
        It displays the location details, such as the name, image, and a brief overview of the destination.
        Additionally, it provides information about the weather, transportation, and accommodation options.
    """
    # Load the matched destination
    destination = app_state.matched_destination
    if not destination:
        st.error("There is an error loading the destination. Please restart the app.")
        st.stop()

    # Make use of the helper function 'run_async_task' to retrieve the location details.
    location_details = run_async_task(travel_agent.get_location_details_async, destination.name)

    # Display the title and the image of the destination
    # The image is retrieved from a remote API.
    # Remarks:
    # - As an improvement, the image could be cached to reduce the number of requests.
    # - Additionally, it could be checked with AI if the image is appropriate or not.
    st.title(f"Nice, it's a match: {destination.name}!")
    st.image(destination.image_url)

    # Use tabs to improve the organization of the content
    tabs = ["Destination Overview", "Your Feedback"]
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
        st.header("Your Feedback")
        
        st.write("We'd love to hear your feedback about HolidayMatch.")

        sentiment_mapping = ["one", "two", "three", "four", "five"]
        selected = st.feedback("stars")
        if selected is not None:
            st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
            if sentiment_mapping[selected] == "one":
                st.write("We're sorry to hear that. Please let us know how we can improve.")                
            elif sentiment_mapping[selected] == "five":
                st.write("We're glad you enjoyed your experience with HolidayMatch!")
