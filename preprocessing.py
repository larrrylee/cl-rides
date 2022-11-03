"""Implements all the preprocessing functionality for the data.
"""

from config import *
import pandas as pd


def load_map():
    """Loads map.txt into a dictionary of bitmaps for the hardcoded locations.
    """
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


def clean_data(drivers_df: pd.DataFrame, riders_df: pd.DataFrame):
    """Filters out the unneeded columns and and validates the data before assigning.
    """
    _validate_data(drivers_df, riders_df)
    _filter_data(drivers_df, riders_df)


def standardize_permanent_responses(riders_df: pd.DataFrame):
    """Standardize the permanent responses for Friday and Sunday rides.
    """
    for idx in riders_df.index:
        response = riders_df.at[idx, PERMANENT_RIDER_FRIDAY_KEY]
        riders_df.at[idx, PERMANENT_RIDER_FRIDAY_KEY] = RIDE_THERE_KEYWORD if PERMANENT_RIDE_THERE_KEYWORD in response.lower() else ''
        response = riders_df.at[idx, PERMANENT_RIDER_SUNDAY_KEY]
        riders_df.at[idx, PERMANENT_RIDER_SUNDAY_KEY] = RIDE_THERE_KEYWORD if PERMANENT_RIDE_THERE_KEYWORD in response.lower() else ''


def standardize_weekly_responses(riders_df: pd.DataFrame):
    """Standardize the weekly responses for Friday and Sunday rides.
    """
    for idx in riders_df.index:
        response = riders_df.at[idx, WEEKLY_RIDER_FRIDAY_KEY]
        riders_df.at[idx, WEEKLY_RIDER_FRIDAY_KEY] = RIDE_THERE_KEYWORD if WEEKLY_RIDE_THERE_KEYWORD in response.lower() else ''
        response = riders_df.at[idx, WEEKLY_RIDER_SUNDAY_KEY]
        riders_df.at[idx, WEEKLY_RIDER_SUNDAY_KEY] = RIDE_THERE_KEYWORD if WEEKLY_RIDE_THERE_KEYWORD in response.lower() else ''


def filter_friday(riders_df: pd.DataFrame) -> pd.DataFrame:
    """Filters riders that will attend Friday College Life.
    """
    return riders_df[riders_df[RIDER_FRIDAY_KEY] == RIDE_THERE_KEYWORD]


def filter_sunday(riders_df: pd.DataFrame) -> pd.DataFrame:
    """Filters riders that will attend Sunday service.
    """
    return riders_df[riders_df[RIDER_SUNDAY_KEY] == RIDE_THERE_KEYWORD]


def prep_necessary_drivers(drivers_df: pd.DataFrame, cnt_riders: int) -> pd.DataFrame:
    driver_cnt = _find_driver_cnt(drivers_df, cnt_riders)
    drivers = drivers_df[:driver_cnt]
    drivers.sort_values(by=DRIVER_CAPACITY_KEY, ascending=False, inplace=True)
    _add_temporaries(drivers)
    return drivers


def _add_temporaries(drivers_df: pd.DataFrame):
    """Adds temporary columns to the dataframes for calculating assignments.
    """
    drivers_df[DRIVER_OPENINGS_KEY] = drivers_df[DRIVER_CAPACITY_KEY]
    drivers_df[DRIVER_ROUTE_KEY] = DEFAULT_LOCS_CODE


def _find_driver_cnt(drivers_df: pd.DataFrame, cnt_riders: int) -> int:
    """Determines how many drivers are needed to give rides to all the riders.
    """
    for cnt, idx in enumerate(drivers_df.index):
        if cnt_riders > 0:
            cnt_riders -= drivers_df.at[idx, DRIVER_CAPACITY_KEY]
        else:
            break
    return cnt


def _filter_data(drivers_df: pd.DataFrame, riders_df: pd.DataFrame):
    _filter_drivers(drivers_df)
    _filter_riders(riders_df)


def _filter_drivers(drivers_df: pd.DataFrame):
    # Currently nothing to filter :)
    pass


def _filter_riders(riders_df: pd.DataFrame):
    riders_df.drop(columns=[RIDER_TIMESTAMP_KEY], inplace=True)


def _validate_data(drivers_df: pd.DataFrame, riders_df: pd.DataFrame):
    """Recovers proper datatypes and removes duplicates
    """
    _validate_drivers(drivers_df)
    _validate_riders(riders_df)


def _validate_drivers(drivers_df: pd.DataFrame):
    """Enforces datetime datatype on the timestamp and drops duplicates from the drivers list.

    Enforcing the datetime datatype allows us to order the drivers when rewriting them to the sheet to implement cycling.
    """
    drivers_df.drop(drivers_df[ drivers_df[DRIVER_PHONE_KEY] == '' ].index, inplace=True)
    drivers_df.drop_duplicates(subset=DRIVER_PHONE_KEY, inplace=True, keep='last')
    drivers_df[DRIVER_TIMESTAMP_KEY] = pd.to_datetime(drivers_df[DRIVER_TIMESTAMP_KEY])
    drivers_df[DRIVER_CAPACITY_KEY] = drivers_df[DRIVER_CAPACITY_KEY].astype(int)


def _validate_riders(riders_df: pd.DataFrame):
    """Drops the oldest duplicates from the riders list.
    """
    riders_df.drop(riders_df[ riders_df[RIDER_PHONE_KEY] == '' ].index, inplace=True)
    riders_df[RIDER_TIMESTAMP_KEY] = pd.to_datetime(riders_df[RIDER_TIMESTAMP_KEY])
    riders_df.sort_values(by=RIDER_TIMESTAMP_KEY, inplace=True)
    riders_df.drop_duplicates(subset=RIDER_PHONE_KEY, inplace=True, keep='last')