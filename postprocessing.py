"""Implements all the postprocessing functionality for the results.
"""

from constants import *
import pandas as pd


def clean_data(drivers: pd.DataFrame):
    """Filters out the unneeded columns and and validates the data before writing.
    """
    clean_drivers(drivers)
    rotate_drivers(drivers)


def clean_drivers(drivers: pd.DataFrame):
    drivers.drop(columns=[DRIVER_OPENINGS_KEY, DRIVER_ROUTE_KEY])


def rotate_drivers(drivers: pd.DataFrame):
    drivers.sort_values(by=DRIVER_TIMESTAMP_KEY, inplace=True)