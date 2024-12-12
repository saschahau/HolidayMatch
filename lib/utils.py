import asyncio
from datetime import datetime
import streamlit as st

def run_async_task(task, *args, **kwargs):
    """
    Helper function to run an asynchronous task in a blocking way.
    
    :param task: The asynchronous task to run.
    :param args: The arguments to pass to the task.
    :param kwargs: The keyword arguments to pass to the task

    returns: The result of the asynchronous task.

    Inspired by:
    - Solomon, B. (2019, January 16). Async IO in Python: A Complete Walkthrough. https://realpython.com/async-io-python
    """
    return asyncio.run(task(*args, **kwargs))

async def fetch_recommendations_with_images_async(travel_agent, destination_recommendations):
    """
    Fetch images for all destination recommendations asynchronously.

    :param: travel_agent: The travel agent to use for fetching images.
    :param: destination_recommendations: The destination recommendations to fetch images for.

    Inspired by:
    - Solomon, B. (2019, January 16). Async IO in Python: A Complete Walkthrough. https://realpython.com/async-io-python
    """
    async def fetch_image(recommendation):
        # Fetch the location photo asynchronously from the travel agent
        photos = await travel_agent.get_location_photo_async(recommendation.name)
        if photos and "data" in photos and photos["data"]:
            first_photo = photos["data"][0]
            recommendation.image_url = first_photo["images"]["original"]["url"]
        else:
            recommendation.image_url = None  # Set to None if no image is found

    # Pass a list of awaitables and upack them with the asterix operator (*).
    # Then, await for all of them to be completed.
    await asyncio.gather(*(fetch_image(recommendation) for recommendation in destination_recommendations))

@st.cache_data
def get_question_groups():
    """
    Get the question groups containing the preference options for the travel recommender.

    returns: A list of question groups with questions and options.
    """
    return [
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
                    "options": ["Culture / Museums", "Hiking / Nature", "Beach / Relaxation", "Party", "Sports", "Adventure"]
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
                    "options": ["Doesn't matter", "Cool < 10°C", "Mild > 10°C", "Warm > 20°C", "Very warm > 30°C"]
                },
                {
                    "title": "Destination",
                    "question": "Where would you like to travel?",
                    "type": "radio",
                    "options": ["Stay in Europe", "North America", "South America", "Asia",
                                "Africa", "Australia / Oceania", "Doesn't matter"]
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
                                "Resort", "Camping", "Doesn't matter"]
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

def get_current_plus_two_years():
    """
    Get the current year and the next two years.
    
    returns: A list of the current year and the next two years.
    """
    # Get current year
    current_year = datetime.now().year

    # Generate list of years from current year to current year + 2
    # e.g. [2024, 2025, 2026]
    return [int(year) for year in range(current_year, current_year + 3)]