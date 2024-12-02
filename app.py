import streamlit as st
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx

from features.travelagent import Agent
from lib.states import AppState, Stage

def get_remote_ip():
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip

def app():
    """Main function for the Streamlit app."""

    # Set the page title and favicon
    st.set_page_config(page_title="HolidayMatch", page_icon=":material/travel_explore:")

    # Get the user's IP address
    st.markdown(f"Remote ip is {get_remote_ip()}")

    # Instantiate the app state
    if "app_state" not in st.session_state:
        st.session_state.app_state = AppState()

    # Instantiate the travel agent
    if "travel_agent_instance" not in st.session_state:
        openai_api_key = None
        if "openai_key" not in st.secrets:
            if "chatbot_api_key" not in st.session_state:                
                st.write("Please provide your OpenAI API key")
                openai_api_key = st.text_input("OpenAI API key", key="chatbot_api_key", type="password")
            openai_api_key = st.session_state.chatbot_api_key
            if not openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()
        else:
            openai_api_key = st.secrets["openai_key"]
        if "tripadvisor_api_key" not in st.secrets:
            st.error("Please provide your TripAdvisor API key")
            st.stop()

        # Create a travel agent instance
        st.session_state.travel_agent_instance = Agent(
            openai_key=openai_api_key,
            tripadvisor_key=st.secrets["tripadvisor_api_key"]
        )
    
    # Import the handlers after the app state and travel agent are instantiated
    from lib.handlers import (
        handle_start, 
        handle_user_preferences, 
        handle_matcher,
        handle_present_details
    )

    # Handler mapping
    stage_handlers = {
        Stage.START: handle_start,
        Stage.USER_PREFERENCES: handle_user_preferences,
        Stage.MATCHER: handle_matcher,
        Stage.PRESENT_DETAILS: handle_present_details,
    }

    handler = stage_handlers.get(st.session_state.app_state.stage)
    if handler:
        # Process the according UI handler
        handler()
            
if __name__ == '__main__':
    app()
