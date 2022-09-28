from calendar import week
import pandas as pd
from models import *

class RideAssignment:
    def __init__(self, riders: list[Rider], drivers: list[Driver], assignments: pd.DataFrame = pd.DataFrame()):
        """Initializes an driver-rider assignment with the given dataframes.
        
        Optionally, precalculated assignments can be passed in.
        This is useful for when assignments have already been sent out to drivers and riders that we don't want to change.
        """
        self.riders = riders
        self.drivers = drivers
        self.assignments = assignments


    def assign_riders(self):
        self._match_preassignments()
        self._assign_on_campus()
        self._assign_off_campus()
        return
    

    def _match_preassignments(self):
        """Takes the preexisting assignments and preprocesses the input data to be consistent with those assignments.
        This allows us to preserve assignments from previous runs of the program.
        """
        #TODO after _assign_on_campus


    def _assign_on_campus(self):
        #TODO: optimize
        for rider in self.riders:
            for driver in self.drivers:
                if driver.add_rider(rider):
                    break

        # TODO: add to assignments
        #for rider in self.riders:
        #    self.assignments.append()


    def _assign_off_campus(self):
        #TODO after _assign_on_campus
        return
