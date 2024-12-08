""" This module contains the AppState class. """
from lib.enums import Stage
from features.travelagent.models import UserInfo

class AppState:
    """
    A class to represent the state of the application.

    State pattern derived from: https://auth0.com/blog/state-pattern-in-python (18.11.2024)
    """
    def __init__(self):
        self.__anonymous = True 
        self.stage = Stage.START
        self.user_preferences = None
        self.matched_destination = None
        self.itinerary = None # Will be implemented if time allows.
        self.user_info = None

    def reset(self):
        """ Reset the state. """
        self.__anonymous = True
        self.stage = Stage.START
        self.user_preferences = None
        self.matched_destination = None
        self.itinerary = None
        self.user_info = None

    @property
    def stage(self):
        """Return the stage."""
        return self._stage

    @stage.setter
    def stage(self, stage: Stage):
        """ 
        Set a new stage. 

        :param stage: The new stage to set.

        :raises TypeError: If the stage is not of type Stage.        
        """
        if isinstance(stage, Stage):
            self._stage = stage
        else:
            raise TypeError("Please provide a valid Stage object.")

    @property
    def user_info(self):
        """Return the user information."""
        return self._user_info

    @user_info.setter
    def user_info(self, user_info: UserInfo):
        """ 
        Set the user information. 
        
        :param user_info: The user information to set.

        :raises TypeError: If the user information is not of type UserInfo.        
        """
        # Check if the user information is valid.
        # If not, raise an error.
        if user_info is not None and not isinstance(user_info, UserInfo):
            raise TypeError("Please provide valid user information.")
        
        # If the user information is valid, set it.        
        self._user_info = user_info

    def get_is_anonymous(self):
        """ Check if the user is anonymous. """
        return self.__anonymous

    def set_authorized(self):
        """ Set the user as authorized. """
        self.__anonymous = False