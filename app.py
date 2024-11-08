import streamlit as st

from features.travelagent import Agent

def app():
    st.set_page_config(page_title="HolidayMatch", page_icon="🌍")

    st.title('Welcome to HolidayMatch')
    st.write('Your AI-powered travel assistant!')

    # Instantiate the travel agent
    if "travel_agent_instance" not in st.session_state:
        st.session_state.travel_agent_instance = Agent(st.secrets['openai_key'])
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
