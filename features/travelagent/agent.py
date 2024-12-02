from datetime import datetime

from features.travelagent.recommendation_engine import RecommendationEngine
from features.travelagent.trip_advisor import TripAdvisor

class Agent:
    """
    Agent class
    A class to represent a travel agent.
    """
    def __init__(self, openai_key: str, tripadvisor_key: str):
        """
        Initializes the Travel Agent instance.

        Args:
            openai_key (str): The API key for accessing the recommendation engine (OpenAI API).
            tripadvisor_key (str): The API key for accessing TripAdvisor (TripAdvisor API).
        """
        self.recommendation_engine = RecommendationEngine(openai_key)
        #self.flight_provider = FlightProvider()
        self.trip_advisor = TripAdvisor(tripadvisor_key)

    def get_travel_recommendations(self, preferences, user_information, exclude_destinations = None):
        """
        Generates travel recommendations based on user preferences.

        Args:
            preferences (dict): A dictionary of user preferences for the travel destination.
                Example keys might include "climate", "budget", "activities", etc.
            user_information (UserInformation): An object that holds the user information.
            exclude_destinations (list, optional): A list of destinations to exclude from the recommendations.
                Defaults to None.

        Returns:
            list[Destination]: A list of recommended travel destinations.
        """
        return self.recommendation_engine.generate_destination_recommendations(preferences, user_information, exclude_destinations=exclude_destinations)

    def get_location_overview(self, location_name, preferences, user_information):
        """"""
        return self.recommendation_engine.generate_destination_overview(location_name, preferences, user_information)

    async def get_location_async(self, search_query, category = "geos"):
        return await self.trip_advisor.location_search_async(search_query, category)

    async def get_location_photo_async(self, location_name):
        location = await self.get_location_async(location_name)
        if "data" in location and location["data"]:
            location_id = location["data"][0]["location_id"]
            photos = await self.trip_advisor.location_photos_async(location_id)
            return photos
        else:
            print("Location not found")
            return None

    async def get_location_details_async(self, location_name):
        location = await self.get_location_async(location_name)
        if "data" in location and location["data"]:
            location_id = location["data"][0]["location_id"]
            details = await self.trip_advisor.location_details_async(location_id)
            return details
        else:
            print("Location not found")
            return None

    async def get_flights_to_destination(self):
        pass