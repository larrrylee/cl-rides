import gspread
from gspread_dataframe import set_with_dataframe
import json
from models import *
import os
import pandas as pd
import pickle
from typing import Tuple


DATA_PATH = 'pickle'
SHEET_ID_FILE = 'sheet_ids.json'
FINAL_SHEET_KEY = "15KJPVqZT6pMq8Qg4qufx9iZOArzjxeD_MN-A-ka6Jnk"

OUTPUT_DRIVER_NAME_KEY = 'Driver'
OUTPUT_DRIVER_PHONE_KEY = 'Driver Phone #'

DRIVER_TIMESTAMP_KEY = 'Timestamp'
DRIVER_NAME_KEY = 'Name'
DRIVER_PHONE_KEY = 'Phone Number'
DRIVER_CAPACITY_KEY = 'Number of Seats in Car (not including you)'

RIDER_TIMESTAMP_KEY = 'Timestamp'
RIDER_NAME_KEY = 'Rider'
RIDER_PHONE_KEY = 'Rider Phone #'
RIDER_LOCATION_KEY = 'Location'
RIDER_FRIDAY_KEY = 'Friday'
RIDER_SUNDAY_KEY = 'Sunday'
RIDER_NOTES_KEY = 'Notes'

PERMANENT_RIDER_TIMESTAMP_KEY = 'Timestamp'
PERMANENT_RIDER_NAME_KEY = 'Full Name:'
PERMANENT_RIDER_PHONE_KEY = 'Phone Number: '
PERMANENT_RIDER_LOCATION_KEY = 'Where should we pick you up?'
PERMANENT_RIDER_FRIDAY_KEY = 'Which service(s) do you need a permanent ride for? [Friday Night Bible Study | 6:30 pm]'
PERMANENT_RIDER_SUNDAY_KEY = 'Which service(s) do you need a permanent ride for? [Sunday Service | 8:30 am/10:45 am]'
PERMANENT_RIDER_NOTES_KEY = 'Other Notes'

WEEKLY_RIDER_TIMESTAMP_KEY = 'Timestamp'
WEEKLY_RIDER_NAME_KEY = 'Name (Include your last name if this is your first time)'
WEEKLY_RIDER_PHONE_KEY = 'Phone Number '
WEEKLY_RIDER_LOCATION_KEY = 'Where should we pick you up from?'
WEEKLY_RIDER_FRIDAY_KEY = 'Friday Night Bible Study (Friday @7pm) (Rides from Campus will be provided at Peterson Loop at 6:30 pm)'
WEEKLY_RIDER_SUNDAY_KEY = 'Sunday Service '
WEEKLY_RIDER_NOTES_KEY = 'Additional Comments / Questions / Concerns'


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
    
    # Reorder and rename columns before merging
    weekly_riders = weekly_riders[[WEEKLY_RIDER_TIMESTAMP_KEY, WEEKLY_RIDER_NAME_KEY, WEEKLY_RIDER_PHONE_KEY, WEEKLY_RIDER_LOCATION_KEY, WEEKLY_RIDER_FRIDAY_KEY, WEEKLY_RIDER_SUNDAY_KEY, WEEKLY_RIDER_NOTES_KEY]]
    weekly_riders.rename(columns={WEEKLY_RIDER_TIMESTAMP_KEY: RIDER_TIMESTAMP_KEY, WEEKLY_RIDER_NAME_KEY: RIDER_NAME_KEY, WEEKLY_RIDER_PHONE_KEY: RIDER_PHONE_KEY, WEEKLY_RIDER_LOCATION_KEY: RIDER_LOCATION_KEY, WEEKLY_RIDER_FRIDAY_KEY: RIDER_FRIDAY_KEY, WEEKLY_RIDER_SUNDAY_KEY: RIDER_SUNDAY_KEY, WEEKLY_RIDER_NOTES_KEY: RIDER_NOTES_KEY}, inplace=True)
    permanent_riders.rename(columns={PERMANENT_RIDER_TIMESTAMP_KEY: RIDER_TIMESTAMP_KEY, PERMANENT_RIDER_NAME_KEY: RIDER_NAME_KEY, PERMANENT_RIDER_PHONE_KEY: RIDER_PHONE_KEY, PERMANENT_RIDER_LOCATION_KEY: RIDER_LOCATION_KEY, PERMANENT_RIDER_FRIDAY_KEY: RIDER_FRIDAY_KEY, PERMANENT_RIDER_SUNDAY_KEY: RIDER_SUNDAY_KEY, PERMANENT_RIDER_NOTES_KEY: RIDER_NOTES_KEY}, inplace=True)
    riders = pd.concat([permanent_riders, weekly_riders])
    return (drivers, riders)


def clean_data(df: pd.DataFrame, rf: pd.DataFrame):
    """Filters out the unneeded columns and and validates the data.
    """
    _validate_data(df, rf)
    _filter_data(df, rf)


def _filter_data(df: pd.DataFrame, rf: pd.DataFrame):
    _filter_drivers(df)
    _filter_riders(rf)


def _filter_drivers(df: pd.DataFrame):
    # Currently nothing to filter :)
    pass


def _filter_riders(rf: pd.DataFrame):
    #TODO
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
    rf.drop(rf[ rf[RIDER_PHONE_KEY] == ''].index, inplace=True)
    rf[RIDER_TIMESTAMP_KEY] = pd.to_datetime(rf[RIDER_TIMESTAMP_KEY])
    rf.sort_values(by=RIDER_TIMESTAMP_KEY, inplace=True)
    rf.drop_duplicates(subset=RIDER_PHONE_KEY, inplace=True, keep='last')


def write_assignments(assignments: pd.DataFrame):
    """Write the given dataframe to the final Google Sheet.
    """
    # connect Google Sheets
    gc = gspread.service_account(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), "service_account.json"))
    ws = gc.open_by_key(FINAL_SHEET_KEY).get_worksheet(0)

    #TODO: use batch updates to use only one API call
    ws.clear()
    set_with_dataframe(worksheet=ws, dataframe=assignments)