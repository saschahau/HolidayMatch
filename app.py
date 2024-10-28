import streamlit as st

from features.travelagent import Agent

def app():
    st.title('Home')
    st.write('Welcome to the home page')

    # Instantiate the travel agent
    if "travel_agent_instance" not in st.session_state:
        st.session_state.travel_agent_instance = Agent(st.secrets['openai_key'])
    travel_agent = st.session_state.travel_agent_instance

    st.write(isinstance(st.session_state.travel_agent_instance, Agent))

    # Get user input
    user_input = st.text_area("Enter your message", "")

    if st.button('Submit'):
        with st.spinner("Retrieving answer..."):
            response = travel_agent.get_response(user_input)
        st.write(response)

        st.subheader("History")
        for entry in travel_agent.responses:
            st.write(f"Q: {entry['question']}")
            st.write(entry['response'])

if __name__ == '__main__':
    app()
