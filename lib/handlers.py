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
from features.travelagent.models import Destination
from lib.states import Stage
from lib.utils import run_async_task, fetch_recommendations_with_images

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
def reset_app():
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
        st.subheader("Before we start, what's your name?")
        name = st.text_input("Please enter your name")
        # Intro Message After Name Input
        if name != "":
            st.subheader(f"Nice to meet you, {name}!")
            st.write("We'll ask you a few questions to find your ideal holiday destination. Ready? ")


        # Add a "Next" button if you want to proceed to the next step
        # Disable the button as long as no name is provided
        button_disabled = True if not name else False
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
                    "title": "Month",
                    "question": "Which month would you like to travel?",
                    "type": "pills",
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
                elif question["type"] == "pills":
                    answer = st.pills("Choose one or more options:", question["options"], selection_mode="multi")

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
            st.write("Here are your answers:")
            for key, value in st.session_state["answers"].items():
                col_1, col_2 = st.columns([0.3, 0.7])
                with col_1:
                    st.write(f"**{key}**")
                with col_2:
                    if isinstance(value, list):
                        st.write(", ".join(value))
                    else:
                        st.write(value)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Restart", use_container_width=True):
                    reset_app()

            with col2:
                # This is only a temporary solution until the preference builder is implemented
                # user_input = st.text_area("Enter your message", "")
                if st.button('Get suggestions', type="primary", icon=":material/model_training:", use_container_width=True):
                    app_state.user_preferences = st.session_state["answers"].items()
                    with st.spinner("Finding travel recommendations for you..."):
                        destination_recommendations = travel_agent.get_travel_recommendations(st.session_state["answers"].items())
                        if destination_recommendations:
                            # Fetch images for the destinations asynchronously
                            run_async_task(fetch_recommendations_with_images, travel_agent, destination_recommendations)

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

            st.subheader(suggestion.name)
            st.write(suggestion.description)
            st.markdown("##### What you'd like to know:")
            st.markdown(f"**Travel tips**: {suggestion.travel_tips}")
            st.markdown(f"**Activities**: {", ".join(suggestion.activities)}")
            st.markdown(f"**Language**: {suggestion.language}")
            st.markdown(f"**Best time to visit**: {", ".join(suggestion.best_time_to_visit)}")
            st.markdown(f"**Transportation**: {", ".join(suggestion.transportation)}")

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

    st.title(f"Nice, it's a match: {destination.name}!")

    # Display the image for the location
    st.image(destination.image_url)

    # Mock temperature data for Ibiza for the months of June, July, and August
    temperature_data = {
        "Day": list(range(1, 32)),  # Assuming 31 days for each month
        "July": [28 + (i % 2) for i in range(31)],  # Example data for July
    }

    # Convert the data into a DataFrame
    df = pd.DataFrame(temperature_data)

    # Streamlit Line Chart
    st.write("**Temperature Data prediction for Ibiza (July)**")
    st.line_chart(df.set_index("Day"))

    tabs = ["Overview", "Hotels", "Flights"]
    tab1, tab2, tab3 = st.tabs(tabs)

    with tab1:
        st.header("Overview")
        overview_text = """
        **Ibiza**, one of Spain's Balearic Islands in the Mediterranean Sea, is renowned for its vibrant nightlife, pristine beaches, and charming villages. Known as the "White Isle," Ibiza offers a perfect blend of relaxation, adventure, and culture, making it a top destination for travelers worldwide.

- **Location**: Balearic Islands, Spain
- **Climate**: Mediterranean (Warm summers, mild winters)
- **Best Time to Visit**: May to October
- **Currency**: Euro (€)
- **Language**: Spanish (Catalan is also widely spoken)

---

## 🌅 **Why Visit Ibiza?**
1. **Stunning Beaches**:
   - Ibiza is home to over 80 picturesque beaches, ranging from secluded coves to lively beach clubs.
   - Popular spots include **Cala Comte**, **Cala Bassa**, and **Playa d’en Bossa**.

2. **World-Class Nightlife**:
   - Ibiza is synonymous with its legendary nightlife, featuring world-renowned DJs and clubs like **Pacha**, **Amnesia**, and **Ushuaïa**.
   - Nightlife runs from late spring to early autumn, making it a hotspot for party enthusiasts.

3. **Rich Culture and History**:
   - The fortified old town of **Dalt Vila** (a UNESCO World Heritage Site) offers a glimpse into Ibiza’s ancient history, with cobblestone streets and breathtaking views.
   - Explore the **Ibiza Cathedral** and **Necropolis of Puig des Molins** for a cultural dive.

4. **Charming Villages**:
   - Beyond the glitz and glamour, Ibiza boasts quaint villages like **Santa Gertrudis** and **Sant Josep**, where you can enjoy authentic Balearic cuisine and local art.

5. **Wellness and Nature**:
   - Ibiza is a hub for wellness retreats, offering yoga classes, meditation, and holistic therapies.
   - Natural wonders include the mystical **Es Vedrà rock** and lush pine forests perfect for hiking.

---

## 🏖️ **Top Attractions**
1. **Dalt Vila**: Wander through this historic old town, filled with ancient walls, boutique shops, and panoramic vistas.
2. **Es Vedrà**: A dramatic limestone rock rising from the sea, shrouded in myths and legends.
3. **Formentera**: Take a short ferry ride to Ibiza’s sister island for crystal-clear waters and unspoiled beaches.
4. **Hippy Markets**: Shop for unique souvenirs and handmade crafts at markets like **Las Dalias** and **Punta Arabí**.

---

## 🍽️ **Food and Drink**
- **Local Delicacies**:
  - **Bullit de Peix**: A traditional fish stew.
  - **Flaó**: A delicious cheesecake flavored with mint.
  - **Sobrasada**: A cured sausage unique to the Balearic Islands.

- **Cocktail Culture**:
  - Sip on refreshing **Hierbas Ibicencas**, a local herbal liqueur, while enjoying sunset views.

---

## 🚤 **Transportation**
- **Getting There**:
  - Fly into **Ibiza Airport (IBZ)**, which connects the island to major European cities.
  - Ferries are available from Barcelona, Valencia, and Mallorca.

- **Getting Around**:
  - Rent a car or scooter to explore the island at your own pace.
  - Taxis and public buses are available but may be limited in remote areas.

---

## ✨ **Travel Tips**
- Book accommodations early during peak season (June to September).
- Visit beach clubs early in the day to secure a spot.
- Respect local rules regarding noise and environmental preservation.

---

Ibiza is more than just a party destination; it’s a haven of beauty, culture, and adventure. Whether you’re looking to dance the night away, relax by turquoise waters, or explore centuries-old heritage, Ibiza has something for everyone."""
        st.write(overview_text)

    with tab2:
        st.header("Hotels")
        st.markdown("Some text...")

    with tab3:
        st.header("Flights")
        st.markdown("Some text...")
