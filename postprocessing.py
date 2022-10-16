"""Implements all the postprocessing functionality for the results.
"""

from constants import *
import pandas as pd


def rotate_drivers(drivers: pd.DataFrame):
    drivers.sort_values(by=DRIVER_TIMESTAMP_KEY, inplace=True)