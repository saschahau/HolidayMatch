import streamlit as st

# App Title
st.title("Holiday Match")

# Initialize Session State for step management
if "step" not in st.session_state:
    st.session_state["step"] = 1
    st.session_state["answers"] = {}  # Stores the answers for each criterion

# Function to move to the next step
def next_step():
    st.session_state["step"] += 1

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
        "title": "Budget",
        "question": "How much would you like to spend on the entire trip?",
        "type": "radio",
        "options": ["Under $200", "$200-$500", "$500-$1000", "Other"]
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
        "options": ["Culture / Museums", "Hiking / Nature", "Beach / Relaxation", "Party"]
    },
    {
        "title": "Month",
        "question": "Which month would you like to travel?",
        "type": "multiselect",
        "options": [ "January", "February", "March", "April", "May", "June",
                     "July", "August", "September", "October", "November", "December"]
    },
    {
        "title": "Climate",
        "question": "Do you prefer warm or cooler weather?",
        "type": "radio",
        "options": ["Warm > 20°C", "Very warm > 30°C", "Cool < 10°C", "Doesn’t matter"]
    },
    {
        "title": "Means of Transport",
        "question": "How would you prefer to travel?",
        "type": "radio",
        "options": ["Car", "Train", "Airplane", "Ship"]
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
    }
]

# Display the current question based on the step
current_step = st.session_state["step"]

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

    if st.button("Restart"):
        reset_app()
    else:
        st.success("Thank you for completing Holiday Match!")
