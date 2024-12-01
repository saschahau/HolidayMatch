from enum import Enum

class Stage(Enum):
    """"""
    START = "start"
    USER_PREFERENCES = "user_preferences"
    RETRIEVE_SUGGESTIONS = "retrieve_suggestions"
    MATCHER = "matcher"
    PRESENT_DETAILS = "present_details"
    RETRIEVE_NEW_SUGGESTIONS = "retrieve_new_suggestions"