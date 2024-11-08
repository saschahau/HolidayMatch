import streamlit as st

from features.travelagent import Agent

def app():
    st.set_page_config(page_title="HolidayMatch", page_icon="🌍")

    st.title('Welcome to HolidayMatch')
    st.write('Your AI-powered travel assistant!')

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
        st.session_state.travel_agent_instance = Agent(openai_api_key)
    travel_agent = st.session_state.travel_agent_instance

    # Get user input
    # This is only a temporary solution until the preference builder is implemented
    user_input = st.text_area("Enter your message", "")

    if st.button('Get suggestions'):
        with st.spinner("Retrieving answer..."):
            response = travel_agent.get_travel_suggestions(user_input)
        st.write(response)

        st.subheader("History")
        for entry in travel_agent.responses:
            st.write(f"Q: {entry['question']}")
            st.write(entry['response'])
            
if __name__ == '__main__':
    app()
