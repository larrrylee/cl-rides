"""Implements all the preprocessing functionality for the data.
"""

from config import *
import pandas as pd


def load_map():
    """Loads map.txt into a dictionary of bitmaps for the hardcoded locations."""
    global elsewhere_code

    with open("map.txt", "r") as map:
        loc = 0b1
        for line in map.readlines():
            if (line.startswith('#')):
                continue
            places = line.split(',')
            places = [place.strip() for place in places]
            for key in loc_map:
                if key in places:
                    loc_map[key] |= loc
            loc <<= 1
        
        elsewhere_code = loc << 1


def clean_data(df: pd.DataFrame, rf: pd.DataFrame):
    """Filters out the unneeded columns and and validates the data before assigning.
    """
    _validate_data(df, rf)
    _filter_data(df, rf)


def standardize_permanent_responses(rf: pd.DataFrame):
    """Standardize the permanent responses for Friday and Sunday rides.
    """
    for idx in rf.index:
        response = rf.at[idx, PERMANENT_RIDER_FRIDAY_KEY]
        rf.at[idx, PERMANENT_RIDER_FRIDAY_KEY] = RIDE_THERE_KEYWORD if PERMANENT_RIDE_THERE_KEYWORD in response.lower() else ''
        response = rf.at[idx, PERMANENT_RIDER_SUNDAY_KEY]
        rf.at[idx, PERMANENT_RIDER_SUNDAY_KEY] = RIDE_THERE_KEYWORD if PERMANENT_RIDE_THERE_KEYWORD in response.lower() else ''


def standardize_weekly_responses(rf: pd.DataFrame):
    """Standardize the weekly responses for Friday and Sunday rides.
    """
    for idx in rf.index:
        response = rf.at[idx, WEEKLY_RIDER_FRIDAY_KEY]
        rf.at[idx, WEEKLY_RIDER_FRIDAY_KEY] = RIDE_THERE_KEYWORD if WEEKLY_RIDE_THERE_KEYWORD in response.lower() else ''
        response = rf.at[idx, WEEKLY_RIDER_SUNDAY_KEY]
        rf.at[idx, WEEKLY_RIDER_SUNDAY_KEY] = RIDE_THERE_KEYWORD if WEEKLY_RIDE_THERE_KEYWORD in response.lower() else ''


def filter_friday(rf: pd.DataFrame) -> pd.DataFrame:
    """Filters riders that will attend Friday College Life.
    """
    return rf[rf[RIDER_FRIDAY_KEY] == RIDE_THERE_KEYWORD]


def filter_sunday(rf: pd.DataFrame) -> pd.DataFrame:
    """Filters riders that will attend Sunday service.
    """
    return rf[rf[RIDER_SUNDAY_KEY] == RIDE_THERE_KEYWORD]


def prep_necessary_drivers(df: pd.DataFrame, cnt_riders: int) -> pd.DataFrame:
    driver_cnt = _find_driver_cnt(df, cnt_riders)
    drivers = df[:driver_cnt]
    drivers.sort_values(by=DRIVER_CAPACITY_KEY, ascending=False, inplace=True)
    _add_temporaries(drivers)
    return drivers


def _add_temporaries(df: pd.DataFrame):
    """Adds temporary columns to the dataframes for calculating assignments.
    """
    df[DRIVER_OPENINGS_KEY] = df[DRIVER_CAPACITY_KEY]
    df[DRIVER_ROUTE_KEY] = DEFAULT_LOCS_CODE


def _find_driver_cnt(df: pd.DataFrame, cnt_riders: int) -> int:
    """Determines how many drivers are needed to give rides to all the riders.
    """
    for cnt, idx in enumerate(df.index):
        if cnt_riders > 0:
            cnt_riders -= df.at[idx, DRIVER_CAPACITY_KEY]
    return cnt


def _filter_data(df: pd.DataFrame, rf: pd.DataFrame):
    _filter_drivers(df)
    _filter_riders(rf)


def _filter_drivers(df: pd.DataFrame):
    # Currently nothing to filter :)
    pass


def _filter_riders(rf: pd.DataFrame):
    rf.drop(columns=[RIDER_TIMESTAMP_KEY], inplace=True)


def _validate_data(df: pd.DataFrame, rf: pd.DataFrame):
    """Recovers proper datatypes and removes duplicates
    """
    _validate_drivers(df)
    _validate_riders(rf)


def _validate_drivers(df: pd.DataFrame):
    """Enforces datetime datatype on the timestamp and drops duplicates from the drivers list.

    Enforcing the datetime datatype allows us to order the drivers when rewriting them to the sheet to implement cycling.
    """
    df.drop(df[ df[DRIVER_PHONE_KEY] == '' ].index, inplace=True)
    df.drop_duplicates(subset=DRIVER_PHONE_KEY, inplace=True, keep='last')
    df[DRIVER_TIMESTAMP_KEY] = pd.to_datetime(df[DRIVER_TIMESTAMP_KEY])
    df[DRIVER_CAPACITY_KEY] = df[DRIVER_CAPACITY_KEY].astype(int)


def _validate_riders(rf: pd.DataFrame):
    """Drops the oldest duplicates from the riders list.
    """
    rf.drop(rf[ rf[RIDER_PHONE_KEY] == '' ].index, inplace=True)
    rf[RIDER_TIMESTAMP_KEY] = pd.to_datetime(rf[RIDER_TIMESTAMP_KEY])
    rf.sort_values(by=RIDER_TIMESTAMP_KEY, inplace=True)
    rf.drop_duplicates(subset=RIDER_PHONE_KEY, inplace=True, keep='last')