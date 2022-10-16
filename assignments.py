"""Implements all the logic for the assigning drivers and riders.
Includes group optimization for common pickup locations.
"""

from sqlite3 import Timestamp
from constants import *
from datetime import date
import numpy as np
import pandas as pd
from rides_data import *

MARSHALL = 'Marshall'
MUIR = 'Muir'
ERC = 'ERC'
REVELLE = 'Revelle'
SIXTH = 'Sixth'
SEVENTH = 'Seventh'
WARREN = 'Warren'
PEPPER_CANYON = 'Pepper Canyon'

DRIVER_OPENINGS_KEY = 'Open seats'
DRIVER_LOCS_KEY = 'Locations'
DEFAULT_LOCS_CODE = 0b0
DRIVER_SECTION_KEY = 'Area'
DEFAULT_AREA_CODE = 0b0

CAMPUS_SOUTHWEST_CODE = 0b00000111
CAMPUS_NORTHWEST_CODE = 0b00111000
CAMPUS_EAST_CODE      = 0b11000000
ELSEWHERE_CODE        =~0b11111111

LOC_MAP = {
    REVELLE:       0b1,
    MUIR:          0b10,
    SIXTH:         0b100,
    MARSHALL:      0b1000,
    ERC:           0b10000,
    SEVENTH:       0b100000,
    WARREN:        0b1000000,
    PEPPER_CANYON: 0b10000000
}

SECTION_MAP = {
    LOC_MAP[REVELLE]:       CAMPUS_SOUTHWEST_CODE,
    LOC_MAP[MUIR]:          CAMPUS_SOUTHWEST_CODE,
    LOC_MAP[SIXTH]:         CAMPUS_SOUTHWEST_CODE,
    LOC_MAP[MARSHALL]:      CAMPUS_NORTHWEST_CODE,
    LOC_MAP[ERC]:           CAMPUS_NORTHWEST_CODE,
    LOC_MAP[SEVENTH]:       CAMPUS_NORTHWEST_CODE,
    LOC_MAP[WARREN]:        CAMPUS_EAST_CODE,
    LOC_MAP[PEPPER_CANYON]: CAMPUS_EAST_CODE,
    ELSEWHERE_CODE:         ELSEWHERE_CODE
}


def assign(df: pd.DataFrame, rf: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
    """Assigns rider to drivers in the returned dataframe, and updates driver timestamp for the last time they drove.
    """
    out = pd.concat([pd.DataFrame(columns=[OUTPUT_DRIVER_NAME_KEY, OUTPUT_DRIVER_PHONE_KEY]), rf[[RIDER_NAME_KEY, RIDER_PHONE_KEY, RIDER_LOCATION_KEY, RIDER_NOTES_KEY]]], axis='columns')
    out.reset_index(inplace=True, drop=True)
    df[DRIVER_OPENINGS_KEY] = df[DRIVER_CAPACITY_KEY]
    df[DRIVER_LOCS_KEY] = DEFAULT_LOCS_CODE
    df[DRIVER_SECTION_KEY] = DEFAULT_AREA_CODE

    for r_idx in range(len(out)):
        rider_loc = LOC_MAP.get(out.at[r_idx, RIDER_LOCATION_KEY], ELSEWHERE_CODE)

        if rider_loc == ELSEWHERE_CODE:
            #TODO: do not assign for now
            if debug:
                print(f'{out.at[r_idx, RIDER_NAME_KEY]} is off campus, assigning skipped')
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
            if _is_available(driver):
                _add_rider(out, r_idx, df, d_idx)
                is_matched = True
                break

    for _, rider in out.iterrows():
        if rider[OUTPUT_DRIVER_NAME_KEY] is np.NaN:
            if debug:
                print(f'{rider[RIDER_NAME_KEY]} has no driver')

    df.drop(columns=[DRIVER_OPENINGS_KEY, DRIVER_SECTION_KEY])
    _format_output(out)

    return out


def assign_sunday(df: pd.DataFrame, rf: pd.DataFrame, debug: bool) -> pd.DataFrame:
    """Assigns Sunday rides.
    """
    rf = prep.filter_sunday(rf)
    return assign(df, rf, debug)


def assign_friday(df: pd.DataFrame, rf: pd.DataFrame, debug: bool) -> pd.DataFrame:
    """Assigns Friday rides.
    """
    rf = prep.filter_friday(rf)
    return assign(df, rf, debug)


def _add_rider(out: pd.DataFrame, r_idx: int, df: pd.DataFrame, d_idx: int):
    """Assigns rider to driver and updates driver openings and locations.
    """
    out.at[r_idx, OUTPUT_DRIVER_NAME_KEY] = df.at[d_idx, DRIVER_NAME_KEY]
    out.at[r_idx, OUTPUT_DRIVER_PHONE_KEY] = df.at[d_idx, DRIVER_PHONE_KEY]
    rider_loc = LOC_MAP.get(out.at[r_idx, RIDER_LOCATION_KEY], ELSEWHERE_CODE)
    df.at[d_idx, DRIVER_OPENINGS_KEY] -= 1
    df.at[d_idx, DRIVER_LOCS_KEY] |= rider_loc
    df.at[d_idx, DRIVER_SECTION_KEY] = SECTION_MAP[rider_loc]
    df.at[d_idx, DRIVER_TIMESTAMP_KEY] = Timestamp.now()


def _is_available(driver: pd.Series) -> bool:
    """Checks if driver has space to take a rider.
    """
    return driver[DRIVER_OPENINGS_KEY] > 0


def _is_nearby_or_open(driver: pd.Series, rider_loc: int) -> bool:
    """Checks if driver has no assignments or is already picking up at the same area as the rider.
    """
    driver_area = driver[DRIVER_SECTION_KEY]
    return _is_available(driver) and (driver_area == DEFAULT_AREA_CODE or _is_intersecting(driver_area, rider_loc))


def _is_there_or_open(driver: pd.Series, rider_loc: int) -> bool:
    """Checks if driver has no assignments or is already picking up at the same college as the rider.
    """
    driver_loc = driver[DRIVER_LOCS_KEY]
    return _is_available(driver) and (driver_loc == DEFAULT_LOCS_CODE or _is_intersecting(driver_loc, rider_loc))


def _is_intersecting(loc1: int, loc2: int) -> bool:
    return (loc1 & loc2) != 0


def _format_output(out: pd.DataFrame):
    """Organizes the output to order by driver then driver. Removes redundant driver details.
    """
    out.sort_values(by=[OUTPUT_DRIVER_NAME_KEY, RIDER_LOCATION_KEY], inplace=True)
    out.reset_index(inplace=True, drop=True)

    for idx in range(len(out) - 1, 0, -1):
        if out.at[idx, OUTPUT_DRIVER_NAME_KEY] is np.nan:
            # Denote unassigned riders.
            out.at[idx, OUTPUT_DRIVER_NAME_KEY] = '?'
        elif out.at[idx, OUTPUT_DRIVER_NAME_KEY] == out.at[idx-1, OUTPUT_DRIVER_NAME_KEY]:
            # Remove redundant driver details.
            out.at[idx, OUTPUT_DRIVER_NAME_KEY] = ''
            out.at[idx, OUTPUT_DRIVER_PHONE_KEY] = ''