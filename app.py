import os
import streamlit as st
from dotenv import load_dotenv

from features.travelagent import Agent
from lib.states import AppState, Stage

def app():
    """ Main Streamlit app function. """
    # Set the page title and favicon
    st.set_page_config(page_title="HolidayMatch", page_icon=":material/travel_explore:")

    # Instantiate the app state
    if "app_state" not in st.session_state:
        st.session_state.app_state = AppState()

    # Instantiate the travel agent
    if "travel_agent_instance" not in st.session_state:
        OPENAI_API_KEY = None
        TRIPADVISOR_API_KEY = None

        # Check if secrets.toml file exists, else load it from the environment
        try:
            # Load the API keys from the secrets.toml file.
            # The secrets.toml file is available in the Streamlit cloud deployment.
            #
            # References: 
            # - Streamlit. (2024). Secrets management for your Community Cloud app. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
            secrets_path = ".streamlit/secrets.toml"
            if os.path.exists(secrets_path):
                OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
                TRIPADVISOR_API_KEY = st.secrets["TRIPADVISOR_API_KEY"]
            else:
                raise FileNotFoundError
            
        except FileNotFoundError:
            # Load the API keys from the environment variables.
            # This is used here for the deployment on Azure.
            load_dotenv()
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            TRIPADVISOR_API_KEY = os.getenv("TRIPADVISOR_API_KEY")
        except Exception:
            st.error(f"An error occurred while loading the API keys!")
            st.stop()

        # Ensure that the API keys are not None. Otherwise, stop the app.
        # The API key are required for the app to work.
        if OPENAI_API_KEY is None or TRIPADVISOR_API_KEY is None:
            st.error(f"API keys are missing!")
            st.stop()

        # Create a travel agent instance and store it into the session state
        # to share the instance between reruns, for each user session.
        st.session_state.travel_agent_instance = Agent(
            openai_key=OPENAI_API_KEY,
            tripadvisor_key=TRIPADVISOR_API_KEY
        )

    # Import the handlers after the app state and travel agent are instantiated
    # Each stage has a corresponding handler function that is called to render the UI.
    # The handler functions are defined in the lib/handlers.py file.
    # This principle is used to separate the UI logic from the main app logic.
    # Since the app progresses through different stages, it is easier to manage the UI logic and the app logic separately.
    # With this pattern, we can easily add new stages or modify the existing ones without affecting the main app logic.
    # It also makes the code more modular and thus, easier to maintain. Additionally, we have no if-else hell in the main app logic
    # to render the UI, which makes it easier to read and understand.
    # 
    # It is inspired by the dictionary dispatch pattern to avoid a long chain of if-else statements.
    #
    # References: 
    # - Martin. (2023, February 1). Dictionary Dispatch Pattern in Python. https://martinheinz.dev/blog/90 
    from lib.handlers import (
        handle_start, 
        handle_user_preferences, 
        handle_matcher,
        handle_present_details
    )

    # Mapping of the different stages to their corresponding handler functions
    stage_handlers = {
        Stage.START: handle_start,
        Stage.USER_PREFERENCES: handle_user_preferences,
        Stage.MATCHER: handle_matcher,
        Stage.PRESENT_DETAILS: handle_present_details,
    }

    # Get the handler for the current stage
    handler = stage_handlers.get(st.session_state.app_state.stage)

    # Check if the handler for the current UI stage is available
    if handler:
        # Call the handler function to render the UI
        handler()
    else:
        st.error("No UI handler found!")
        st.stop()
            
if __name__ == '__main__':
    app()