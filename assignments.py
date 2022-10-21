"""Implements all the logic for the assigning drivers and riders.
Includes group optimization for common pickup locations.
"""

from sqlite3 import Timestamp
from constants import *
import numpy as np
import pandas as pd
import postprocessing as post
import preprocessing as prep
from rides_data import *


def assign(df: pd.DataFrame, rf: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
    """Assigns rider to drivers in the returned dataframe, and updates driver timestamp for the last time they drove.
    """
    out = pd.concat([pd.DataFrame(columns=[OUTPUT_DRIVER_NAME_KEY, OUTPUT_DRIVER_PHONE_KEY]), rf[[RIDER_NAME_KEY, RIDER_PHONE_KEY, RIDER_LOCATION_KEY, RIDER_NOTES_KEY]]], axis='columns')
    out.reset_index(inplace=True, drop=True)

    if debug:
        print('Drivers')
        print(df)
        print('Riders')
        print(rf)
        print('Assigning started')

    for r_idx in range(len(out)):
        rider_loc = LOC_MAP.get(out.at[r_idx, RIDER_LOCATION_KEY], ELSEWHERE_CODE)

        if rider_loc == ELSEWHERE_CODE:
            #TODO: do not assign for now
            if debug:
                print(f'\t{out.at[r_idx, RIDER_NAME_KEY]} is not from a prerecorded location, assigning skipped')
            continue

        is_matched = False

        # Check if a driver is already there.
        for d_idx, driver in df.iterrows():
            if _is_there_or_open(driver, rider_loc):
                _add_rider(out, r_idx, df, d_idx)
                is_matched = True
                break

        if is_matched:
            continue

        # Check if a driver is in the same section on campus.
        for d_idx, driver in df.iterrows():
            if _is_nearby_or_open(driver, rider_loc):
                _add_rider(out, r_idx, df, d_idx)
                is_matched = True
                break

        if is_matched:
            continue

        # Check if any driver is available.
        for d_idx, driver in df.iterrows():
            if _has_opening(driver):
                _add_rider(out, r_idx, df, d_idx)
                is_matched = True
                break

    return out


def assign_sunday(df: pd.DataFrame, rf: pd.DataFrame, debug: bool) -> pd.DataFrame:
    """Assigns Sunday rides.
    """
    rf = prep.filter_sunday(rf)
    prep.add_temporaries(df)
    out = assign(df, rf, debug)
    post.alert_skipped_riders(out, debug)
    post.clean_output(out, df)
    return out


def assign_friday(df: pd.DataFrame, rf: pd.DataFrame, debug: bool) -> pd.DataFrame:
    """Assigns Friday rides.
    """
    rf = prep.filter_friday(rf)
    prep.add_temporaries(df)
    out = assign(df, rf, debug)
    post.alert_skipped_riders(out, debug)
    post.clean_output(out, df)
    return out


def _add_rider(out: pd.DataFrame, r_idx: int, df: pd.DataFrame, d_idx: int):
    """Assigns rider to driver and updates driver openings and locations.
    """
    out.at[r_idx, OUTPUT_DRIVER_NAME_KEY] = df.at[d_idx, DRIVER_NAME_KEY]
    out.at[r_idx, OUTPUT_DRIVER_PHONE_KEY] = df.at[d_idx, DRIVER_PHONE_KEY]
    rider_loc = LOC_MAP.get(out.at[r_idx, RIDER_LOCATION_KEY], ELSEWHERE_CODE)
    df.at[d_idx, DRIVER_OPENINGS_KEY] -= 1
    df.at[d_idx, DRIVER_ROUTE_KEY] |= rider_loc
    df.at[d_idx, DRIVER_TIMESTAMP_KEY] = Timestamp.now()


def _has_opening(driver: pd.Series) -> bool:
    """Checks if driver has space to take a rider.
    """
    return driver[DRIVER_OPENINGS_KEY] > 0


def _is_free(driver: pd.Series) -> bool:
    """Checks if driver is completely free (no riders assigned).
    """
    return driver[DRIVER_ROUTE_KEY] == DEFAULT_LOCS_CODE


def _is_nearby_or_open(driver: pd.Series, rider_loc: int) -> bool:
    """Checks if driver has no assignments or is already picking up at the same area as the rider.
    """
    driver_loc = driver[DRIVER_ROUTE_KEY]
    return _has_opening(driver) and (_is_free(driver) or _is_intersecting(driver_loc << 1, rider_loc) or _is_intersecting(driver_loc >> 1, rider_loc))


def _is_there_or_open(driver: pd.Series, rider_loc: int) -> bool:
    """Checks if driver has no assignments or is already picking up at the same college as the rider.
    """
    driver_loc = driver[DRIVER_ROUTE_KEY]
    return _has_opening(driver) and (driver_loc == DEFAULT_LOCS_CODE or _is_intersecting(driver_loc, rider_loc))


def _is_intersecting(loc1: int, loc2: int) -> bool:
    return (loc1 & loc2) != 0