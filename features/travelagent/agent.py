from datetime import datetime

from features.travelagent.recommendation_engine import RecommendationEngine

class Agent:
    """"""
    def __init__(self, api_key: str):
        self.recommendation_engine = RecommendationEngine(api_key)

    def get_travel_recommendations(self, preferences):
        """ Get response from the AI model. """
        recommendations = self.recommendation_engine.generate_destination_recommendations(preferences)
        return recommendations
