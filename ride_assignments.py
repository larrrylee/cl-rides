from calendar import week
import pandas as pd
import numpy as np

class RideAssignment:
    def __init__(self, permanent_riders: pd.DataFrame, weekly_riders: pd.DataFrame, drivers: pd.DataFrame, assignments: pd.DataFrame = pd.DataFrame()):
        """Initializes an driver-rider assignment with the given dataframes.
        
        Optionally, precalculated assignments can be passed in.
        This is useful for when assignments have already been sent out to drivers and riders that we don't want to change.
        """
        self.permanent_riders = permanent_riders
        self.weekly_riders = weekly_riders
        self.drivers = drivers
        self.assignments = assignments


    def assign_riders(self):
        self._consolidate_riders()
        self._match_preassignments()
        self._assign_on_campus()
        self._assign_off_campus()
        return
    

    def _consolidate_riders(self):
        """Combines the permanent and weekly riders list.

        Removes duplicates and alerts the user of said duplicates.
        """
        # TODO: since the sheets are formatted differently for permanent vs weekly riders, concat may not work
        self.riders = pd.concat([self.permanent_riders, self.weekly_riders])
        # TODO: checking duplicates
    

    def _match_preassignments(self):
        """Takes the preexisting assignments and preprocesses the input data to be consistent with those assignments.
        This allows us to preserve assignments from previous runs of the program.
        """
        #TODO after _assign_on_campus
        for i in self.drivers:
            break
        return


    def _assign_on_campus(self):
        #TODO
        return


    def _assign_off_campus(self):
        #TODO after _assign_on_campus
        return
