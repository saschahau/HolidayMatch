from features.travelagent.models import Destination

class Matcher:
    """
    A class to represent a Matcher.
    
    The matcher is used to manage the recommendations and the user's preferences.
    Ultimately, the matcher is responsible for suggesting destinations to the user and managing the user's feedback.
    """
    def __init__(self, recommendations):
        self.__current_index = 0
        self.__destination_recommendations = recommendations
        self.disliked_destinations = list()

    def get_index(self):
        """Return the current index."""
        return self.__current_index

    def get_recommendations_count(self):
        """Return the number of recommendations."""
        return len(self.__destination_recommendations)

    def replace_suggestions(self, suggestions):
        """
        Replace the current suggestions with new suggestions.
        
        :param suggestions: A list of suggestions to replace the current suggestions.
        """
        if not isinstance(suggestions, list):
            raise TypeError("Please provide a list of suggestions.")
        self.__destination_recommendations = suggestions
        self.__current_index = 0

    def add_suggestions(self, suggestions):
        """
        Add new suggestions to the current list of suggestions.
        
        :param suggestions: A list of suggestions to add.
        """
        if not isinstance(suggestions, list):
            raise TypeError("Please provide a list of suggestions.")
        self.__destination_recommendations.extend(suggestions)

    def list_suggestions(self):
        """Return the list of suggestions."""
        return self.__destination_recommendations

    def suggest(self) -> Destination | None:
        """
        Return the current suggestion.
        
        :returns: The current suggestion or None if there are no more suggestions.
        """
        try:
            return self.__destination_recommendations[self.__current_index]
        except IndexError:
            return None

    def dislike(self):
        """Dislike the current suggestion and move to the next suggestion"""
        # Add the destination to the disliked list to avoid that the same destinations are loaded again
        # if another set of suggestions needs to be loaded for the current session.
        self.disliked_destinations.append(self.suggest().name)
        # Continue to the next suggestion
        if self.__current_index < len(self.__destination_recommendations):
            self.__current_index = self.__current_index + 1
