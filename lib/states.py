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
    def __init__(self):
        self.__anonymous = True 
        self.stage = Stage.START
        self.preferences = None
        self.suggestions = list()
        self.current_index = 0
        self.matched_destination = None
        self.itiernary = None # Will be impolemented if time allows.

    def reset(self):
        """ Reset the state. """
        self.stage = Stage.START
        self.preferences = None
        self.suggestions = list()
        self.current_index = 0
        self.matched_destination = None
        self.itiernary = None

    def set_stage(self, stage: Stage):
        """ Set a new stage. """
        self.stage = stage

    def next_stage(self):
        """ Move to the next stage. """
        self.stage = Stage(self.stage.value + 1)

    def get_is_anonymous(self):
        """ Check if the user is anonymous. """
        return self.__anonymous

    def set_authorized(self):
        """ Set the user as authorized. """
        self.__anonymous = False