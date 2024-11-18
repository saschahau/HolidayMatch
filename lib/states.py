import enum
from enum import Enum

class Stage(Enum):
    """"""
    START = "start"
    USER_PREFERENCES = "user_preferences"
    RETRIEVE_SUGGESTIONS = "retrieve_suggestions"
    MATCHER = "matcher"
    PRESENT_DETAILS = "present_details"
    RETRIEVE_NEW_SUGGESTIONS = "retrieve_new_suggestions"

class AppState:
    """

    State pattern derived from: https://auth0.com/blog/state-pattern-in-python (18.11.2024)
    """
    def __init__(self):
        self.__anonymous = True 
        self.stage = Stage.START
        self.user_preferences = None
        self.matched_destination = None
        self.itinerary = None # Will be implemented if time allows.

    def reset(self):
        """ Reset the state. """
        self.__anonymous = True
        self.stage = Stage.START
        self.user_preferences = None
        self.matched_destination = None
        self.itinerary = None

    @property
    def stage(self):
        """Return the stage."""
        return self._stage

    @stage.setter
    def stage(self, stage: Stage):
        """ Set a new stage. """
        if isinstance(stage, Stage):
            self._stage = stage
        else:
            raise TypeError("Please provide a valid Stage object.")



    def get_is_anonymous(self):
        """ Check if the user is anonymous. """
        return self.__anonymous

    def set_authorized(self):
        """ Set the user as authorized. """
        self.__anonymous = False