"""Implements usage of the Google Sheets API, including reading driver/rider data and writing to the output sheet.
"""

from config import *
import gspread
from gspread_dataframe import set_with_dataframe
import json
import os
import pandas as pd
import pickle
import preprocessing as prep
from typing import Tuple


DATA_PATH = 'pickle'
SHEET_ID_FILE = 'sheet_ids.json'
DRIVER_SHEET_KEY = 'drivers'
FINAL_SHEET_ID = "15KJPVqZT6pMq8Qg4qufx9iZOArzjxeD_MN-A-ka6Jnk"


def update_pickles():
    """Pull riders and drivers from the Google Sheets and write to the pickle files.
    """
    # connect Google Sheets
    gc = gspread.service_account(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), "service_account.json"))

    with open(SHEET_ID_FILE) as gid_json:
        gid_data = json.load(gid_json)

    for key in gid_data:
        print(f'Fetching {key}')
        ws = gc.open_by_key(gid_data[key]).get_worksheet(0)
        records = ws.get_all_records()
        with open(os.path.join(DATA_PATH, key), 'wb') as pickle_file:
            pickle.dump(records, pickle_file)


def print_pickles():
    """Print the riders and drivers in the pickle files.

    There is no call to the Google Sheets API, so the printed data is from the last call to update_pickles.
    """
    with open(SHEET_ID_FILE) as gid_json:
        keys = json.load(gid_json).keys()

    for key in keys:
        print(f'Printing {key}')
        with open(os.path.join(DATA_PATH, key), 'rb') as pickle_file:
            records = pickle.load(pickle_file)
            df = pd.DataFrame(records)
            print(df)


def get_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return a tuple of pandas DataFrames, ordered as (permanent riders, weekly riders, drivers)

    Updates rides data on call. Use get_cached_data() to get prefetched data.
    """
    update_pickles()
    return get_cached_data()


def get_cached_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return a tuple of pandas DataFrames, ordered as (drivers, riders)
    
    If the rides data has not been read previously, the results may be outdated or an error might occur.
    """
    with open(os.path.join(DATA_PATH, 'permanent'), 'rb') as pickle_file:
        permanent_riders = pd.DataFrame(pickle.load(pickle_file))
    
    with open(os.path.join(DATA_PATH, 'weekly'), 'rb') as pickle_file:
        weekly_riders = pd.DataFrame(pickle.load(pickle_file))
    
    with open(os.path.join(DATA_PATH, 'drivers'), 'rb') as pickle_file:
        drivers = pd.DataFrame(pickle.load(pickle_file))
    
    prep.standardize_permanent_responses(permanent_riders)
    prep.standardize_weekly_responses(weekly_riders)
    
    # Reorder and rename columns before merging
    weekly_riders = weekly_riders[[WEEKLY_RIDER_TIMESTAMP_KEY, WEEKLY_RIDER_NAME_KEY, WEEKLY_RIDER_PHONE_KEY, WEEKLY_RIDER_LOCATION_KEY, WEEKLY_RIDER_FRIDAY_KEY, WEEKLY_RIDER_SUNDAY_KEY, WEEKLY_RIDER_NOTES_KEY]]
    weekly_riders.rename(columns={WEEKLY_RIDER_TIMESTAMP_KEY: RIDER_TIMESTAMP_KEY, WEEKLY_RIDER_NAME_KEY: RIDER_NAME_KEY, WEEKLY_RIDER_PHONE_KEY: RIDER_PHONE_KEY, WEEKLY_RIDER_LOCATION_KEY: RIDER_LOCATION_KEY, WEEKLY_RIDER_FRIDAY_KEY: RIDER_FRIDAY_KEY, WEEKLY_RIDER_SUNDAY_KEY: RIDER_SUNDAY_KEY, WEEKLY_RIDER_NOTES_KEY: RIDER_NOTES_KEY}, inplace=True)
    permanent_riders.rename(columns={PERMANENT_RIDER_TIMESTAMP_KEY: RIDER_TIMESTAMP_KEY, PERMANENT_RIDER_NAME_KEY: RIDER_NAME_KEY, PERMANENT_RIDER_PHONE_KEY: RIDER_PHONE_KEY, PERMANENT_RIDER_LOCATION_KEY: RIDER_LOCATION_KEY, PERMANENT_RIDER_FRIDAY_KEY: RIDER_FRIDAY_KEY, PERMANENT_RIDER_SUNDAY_KEY: RIDER_SUNDAY_KEY, PERMANENT_RIDER_NOTES_KEY: RIDER_NOTES_KEY}, inplace=True)
    riders = pd.concat([permanent_riders, weekly_riders])
    riders.reset_index(inplace=True, drop=True)

    return (drivers, riders)


def write_assignments(assignments: pd.DataFrame):
    """Write the given dataframe to the final Google Sheet.
    """
    # connect Google Sheets
    gc = gspread.service_account(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), "service_account.json"))
    ws = gc.open_by_key(FINAL_SHEET_ID).get_worksheet(0)

    #TODO: use batch updates to use only one API call
    ws.clear()
    set_with_dataframe(worksheet=ws, dataframe=assignments)


def get_prev_assignments() -> pd.DataFrame:
    """Get the assignments that were calculated from the last grouping.
    """
    print('Fetching previous output')
    gc = gspread.service_account(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), "service_account.json"))
    ws = gc.open_by_key(FINAL_SHEET_ID).get_worksheet(0)
    records = ws.get_all_records()
    return pd.DataFrame(records)


def update_drivers(drivers_df: pd.DataFrame):
    """Write the given dataframe to the driver sheet.
    """
    with open(SHEET_ID_FILE) as gid_json:
        gid_data = json.load(gid_json)

    # connect Google Sheets
    gc = gspread.service_account(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), "service_account.json"))
    ws = gc.open_by_key(gid_data[DRIVER_SHEET_KEY]).get_worksheet(0)

    #TODO: use batch updates to use only one API call
    ws.clear()
    set_with_dataframe(worksheet=ws, dataframe=drivers_df)


def update_drivers_locally(drivers_df: pd.DataFrame):
    """Write the given dataframe to the drivers pickle file.
    """
    drivers_df.to_pickle(os.path.join(DATA_PATH, DRIVER_SHEET_KEY))