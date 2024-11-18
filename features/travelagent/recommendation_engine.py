import json
import openai
from datetime import datetime
from pydantic import TypeAdapter
from typing import List

from features.travelagent.destination import Destination


class RecommendationEngine:
    """Recoomendation Engine class to interact with the OpenAI API."""
    def __init__(self, api_key: str):
        openai.api_key = api_key
        # Define a list to store the responses
        self.response_history = list()
        # Define the tokens used by the AI model to control the costs
        self.__tokes_used = dict()
        # Define the function signature to get structured suggestions from the AI model
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
                                "trending": {"type": "boolean", "description": "Whether the destination is trending or not"},
                                "transportation": {"type": "array", "description": "Transportation options to reach the destination", "items": {"type": "string", "description": "Transportation mode"}},
                            },
                            "required": ["name", "description", "climate", "activities", "budget", "travel_tips", "image", "best_time_to_visit", "currency", "language", "trending"]
                        }
                    }
                }
            }
        }

    def generate_destination_recommendations(self, preferences, model = "gpt-4o"):
        """ Get response from the AI model. """
        prompt = f"Suggest 5 distinct travel destinations for the following user preferences: {preferences}. To consider transportation options and travel time to destination, assume the user starts his trip in Switzerland. Only suggest locations where it can reasonably be assumed that the budget is sufficient for transport and accomodation."

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
        recommendations = TypeAdapter(List[Destination]).validate_python(json_result["destinations"])
        content = {
            'timestamp': datetime.now(),
            'preferences': preferences,
            'response': recommendations
        }
        self.response_history.append(content)

        return recommendations