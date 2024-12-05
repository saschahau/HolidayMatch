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
        The travel agent is used to abstract the interaction with the recommendation engine and the travel providers.

        param openai_key: The OpenAI API key.
        param tripadvisor_key: The TripAdvisor API key.
        """
        self.recommendation_engine = RecommendationEngine(openai_key)
        #self.flight_provider = FlightProvider()
        self.trip_advisor = TripAdvisor(tripadvisor_key)

    def get_travel_recommendations(self, preferences, user_information, exclude_destinations = None):
        """
        Generates travel recommendations based on user preferences.

        param preferences: A dictionary of user preferences for the travel destination.
        param user_information: An object that holds the user information.
        param exclude_destinations: A list of destinations to exclude from the recommendations.

        return: A list of recommended travel destinations.
        """
        return self.recommendation_engine.generate_destination_recommendations(preferences, user_information, exclude_destinations=exclude_destinations)

    def get_location_overview(self, location_name, preferences, user_information):
        """
        Get the overview of a location.

        param location_name: The name of the location to get the overview for.
        param preferences: The user preferences for the location.
        param user_information: The user information.

        return: The overview of the location.        
        """
        return self.recommendation_engine.generate_destination_overview(location_name, preferences, user_information)

    async def get_location_async(self, search_query, category = "geos"):
        """
        Get the location details.

        param search_query: The search query to search for locations.
        param category: The category of the location to search for.

        return: The location details.
        """
        return await self.trip_advisor.location_search_async(search_query, category)

    async def get_location_photo_async(self, location_name):
        """
        Get photos of a location.

        param location_name: The name of the location to get photos for.

        return: The photos of the location.
        """
        location = await self.get_location_async(location_name)
        if "data" in location and location["data"]:
            location_id = location["data"][0]["location_id"]
            photos = await self.trip_advisor.location_photos_async(location_id)
            return photos
        else:
            print("Location not found")
            return None

    async def get_location_details_async(self, location_name):
        """
        Get details of a location.

        param location_name: The name of the location to get details for.

        return: The details of the location.
        """
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