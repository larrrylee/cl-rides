from calendar import week
import pandas as pd
import numpy as np

class RideAssignment:
    def __init__(self, permanent_riders: pd.DataFrame, weekly_riders: pd.DataFrame, drivers: pd.DataFrame):
        self.permanent_riders = permanent_riders
        self.weekly_riders = weekly_riders
        self.drivers = drivers
        self.assignments = pd.DataFrame()

    def assign_riders(self):
        self.__assign_on_campus()
        self.__assign_off_campus()
        return

    def __assign_on_campus(self):
        return

    def __assign_off_campus(self):
        return