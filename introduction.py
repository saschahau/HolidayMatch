import streamlit as st

# Set the page title and favicon
st.set_page_config(
    page_title="Holidaymatch",
    page_icon="✈️"
)

# Welcome Message
st.title("✈️ Welcome to Holidaymatch!")
st.write("Welcome to Holidaymatch, your personalized travel planning assistant! Let’s find your perfect holiday destination based on your preferences.")

# Divider for visual separation
st.divider()

# User Info Input
st.subheader("Before we start, what’s your name?")
name = st.text_input("Enter your name")

# Intro Message After Name Input
st.subheader(f"Nice to meet you, {name}!")
st.write("We'll ask you a few questions to find your ideal holiday destination. Ready? Let's go!")

# Add a "Next" button if you want to proceed to the next step
if st.button("Next"):
    st.write("Let's start finding your perfect holiday destination!")  # Placeholder for the next step