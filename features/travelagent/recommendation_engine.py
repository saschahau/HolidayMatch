import json
import openai
from datetime import datetime
from pydantic import TypeAdapter
from typing import List

from features.travelagent.models import Destination

class RecommendationEngine:
    """ Recommendation Engine class to interact with the OpenAI API."""
    def __init__(self, api_key: str):
        """
        Initialize the Recommendation Engine with the OpenAI API key.

        :param api_key: The OpenAI API key.
        """
        openai.api_key = api_key
        # Define a list to store the responses
        self.response_history = list()
        # Define the function signature to get structured suggestions from the AI model.
        # According to: https://platform.openai.com/docs/guides/function-calling#function-definitions
        self.__function_definition = {
            "name": "get_travel_recommendations",
            "description": "Returns a structured list of travel destination suggestions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destinations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Name of the travel destination"},
                                "description": {"type": "string", "description": "Brief description of the destination"},
                                "climate": {"type": "string", "description": "Climate type during travel date (e.g., Warm, Cold, Mild)"},
                                "activities": {"type": "array", "items": {"type": "string", "description": "Activity to do at the destination and which it is famous for"}},
                                "budget": {"type": "string", "description": "Budget level (Low, Medium, High)"},
                                "travel_tips": {"type": "string", "description": "Travel tips for the destination"},
                                "best_time_to_visit": {"type": "array", "description": "Best time to visit the destination", "items": {"type": "string", "description": "Month"}},
                                "currency": {"type": "string", "description": "Currency used at the destination"},
                                "language": {"type": "string", "description": "Language spoken at the destination"},
                                "trending": {"type": "boolean", "description": "Whether the destination is trending or not for the travel date"},
                                "transportation": {"type": "array", "description": "Transportation options to reach the destination", "items": {"type": "string", "description": "Transportation mode"}},
                                "image_url": {"type": "string", "description": "Link to an image of the travel destination"},
                            },
                            "required": ["name", "description", "climate", "activities", "budget", "travel_tips", "image", "best_time_to_visit", "currency", "language", "trending", "image_url"]
                        }
                    }
                }
            }
        }

    def generate_destination_recommendations(self, preferences, user_information, model = "gpt-4o", exclude_destinations = None):
        """ 
        Generate travel destination recommendations based on user preferences and information.
        
        :param preferences: The user preferences for the travel destination.
        :param user_information: The user information
        :param model: The AI model to use for generating recommendations (default is set to 'gpt-4o').
        :param exclude_destinations: The destinations to exclude from the recommendations.

        returns: The travel destination recommendations. (List of Destination objects)
        """

        # Prepare the prompt for the AI model
        prompt = f"""Suggest 5 distinct travel destinations for the following user preferences: {preferences}. 
        User information: Age: {user_information.age}. Gender: {user_information.gender}.
        To consider transportation options and travel time to destination, assume the user starts his trip in Switzerland. If you have other transportation options than a plane, always specify how to get there exactly.
        Only suggest locations where it can reasonably be assumed that the budget is sufficient for transport and accommodation.
        Budget is always per person."""
        if exclude_destinations is not None:
            prompt += f"These destinations have already been presented but are no option for the user: {", ".join(exclude_destinations)}"

        # Get the response from OpenAI
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system","content": "Act as experienced travel agent helping students to find destinations for their holidays. You will get the preferences from the students and suggest them the destination by trying to fulfill their preferences. Always return responses in JSON format."},
                {"role": "user", "content": prompt},
            ],
            functions=[self.__function_definition],
            function_call = {"name": "get_travel_recommendations"}

        )
        output = response.choices[0].message.function_call.arguments
        json_result = json.loads(output)

        # Validate the response and convert it into a list of Destination objects
        # by using the TypeAdapter class of Pydantic.
        recommendations = TypeAdapter(List[Destination]).validate_python(json_result["destinations"])

        # Store the response in the response history
        content = {
            'timestamp': datetime.now(),
            'preferences': preferences,
            'response': recommendations
        }
        self.response_history.append(content)
        
        return recommendations

    def generate_destination_overview(self, destination, preferences, user_information, model = "gpt-4o"):
        """
        Generate a short and concise overview about the travel destination the user asks for.

        :param destination: The travel destination to provide an overview for.
        :param preferences: The user preferences for the travel destination.
        :param user_information: The user information.
        :param model: The AI model to use for generating the overview (default is set to 'gpt-4o').

        returns: The overview about the travel destination.
        """
        system_instructions = f"""Act as experienced travel agent and provide a short and concise overview about the travel destination, the user asks for."""
        prompt = f"""
            Destination: {destination}.
            Here are some background information about the traveller: 
                User Information: Age: {user_information.age}. Gender: {user_information.gender}.
                Preferences: {preferences}
            Give your response as markdown-text, so that it can be used in Streamlit using st.markdown(). Don't use '```markdown' at the beginning, as it will not be rendered properly!
        """
        # Get the response from OpenAI
        response = openai.chat.completions.create(
            model=model,
            messages=[
                { "role": "system","content": system_instructions },
                { "role": "user", "content": prompt },
            ]
        )
        content = response.choices[0].message.content

        return content