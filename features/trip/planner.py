""" This module contains the trip planner feature. """
import uuid

class TripPlanner:
    """ This class is responsible for planning trips. """
    STAGES = {
        0: "Start",
        1: "Set preferences",
        2: "Present suggestions",
        3: "Destination selected",
        5: "End"
    }

    def __init__(self):
        self.__trip_id = uuid.uuid4()
        self.__stage = 0

    def plan(self, destination):
        print(f"Planning trip to {destination} for trip ID {self.__trip_id}")

    def get_stage(self):
        """ Get the current stage. """
        return self.STAGES[self.__stage]

    def go_to_next_stage(self):
        """ Go to the next stage. """
        if self.__stage < 5:
            self.__stage += 1

    def go_to_previous_stage(self):
        """ Go to the previous stage. """
        if self._stage > 0:
            self.__stage -= 1

    