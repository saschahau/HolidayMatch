from features.travelagent.destination import Destination


class Matcher:
    def __init__(self, recommendations):
        self.__current_index = 0
        self.__destination_recommendations = recommendations

    def get_index(self):
        return self.__current_index

    def get_recommendations_count(self):
        return len(self.__destination_recommendations)

    def replace_suggestions(self, suggestions):
        if not isinstance(suggestions, list):
            raise TypeError("Please provide a list of suggestions.")
        self.__destination_recommendations = suggestions
        self.__current_index = 0

    def add_suggestions(self, suggestions):
        if not isinstance(suggestions, list):
            raise TypeError("Please provide a list of suggestions.")
        self.__destination_recommendations.extend(suggestions)

    def list_suggestions(self):
        return self.__destination_recommendations

    def suggest(self) -> Destination | None:
        try:
            return self.__destination_recommendations[self.__current_index]
        except IndexError:
            return None

    def dislike(self):
        if self.__current_index < len(self.__destination_recommendations):
            self.__current_index = self.__current_index + 1
