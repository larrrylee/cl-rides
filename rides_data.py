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

DRIVER_NAME_IDX = 2
DRIVER_PHONE_IDX = 3
DRIVER_CAPACITY_IDX = 6

PERMANENT_RIDER_NAME_IDX = 2
PERMANENT_RIDER_PHONE_IDX = 3
PERMANENT_RIDER_LOCATION_IDX = 4

WEEKLY_RIDER_NAME_IDX = 2
WEEKLY_RIDER_PHONE_IDX = 6
WEEKLY_RIDER_LOCATION_IDX = 4


def update_pickles():
    # connect Google Sheets
    gc = gspread.service_account(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), "service_account.json"))

    with open(SHEET_ID_FILE) as gid_json:
        gid_data = json.load(gid_json)

    for key in gid_data:
        ws = gc.open_by_key(gid_data[key]).get_worksheet(0)
        records = ws.get_all_records()
        with open(os.path.join(DATA_PATH, key), 'wb') as pickle_file:
            pickle.dump(records, pickle_file)


def print_pickles():
    with open(SHEET_ID_FILE) as gid_json:
        keys = json.load(gid_json).keys()

    for key in keys:
        with open(os.path.join(DATA_PATH, key), 'rb') as pickle_file:
            records = pickle.load(pickle_file)
            df = pd.DataFrame(records)
            print(df)


def get_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return a tuple of pandas DataFrames, ordered as (permanent riders, weekly riders, drivers)

    Updates rides data on call, use get_cached_data() if data was already updated.
    """
    update_pickles()
    return get_cached_data()


def get_cached_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return a tuple of pandas DataFrames, ordered as (permanent riders, weekly riders, drivers)
    
    If the rides data has not been read previously, the results may be outdated or an error might occur.
    """
    with open(os.path.join(DATA_PATH, 'permanent'), 'rb') as pickle_file:
        permanent_riders = pd.DataFrame(pickle.load(pickle_file))
    
    with open(os.path.join(DATA_PATH, 'weekly'), 'rb') as pickle_file:
        weekly_riders = pd.DataFrame(pickle.load(pickle_file))
    
    with open(os.path.join(DATA_PATH, 'drivers'), 'rb') as pickle_file:
        drivers = pd.DataFrame(pickle.load(pickle_file))
    
    return (permanent_riders, weekly_riders, drivers)


def riders_to_list() -> list[Rider]:
    """Return the list of riders, combining the permanent and weekly rider forms
    """
    riders = []

    with open(os.path.join(DATA_PATH, 'permanent'), 'rb') as pickle_file:
        df_permanent = pd.DataFrame(pickle.load(pickle_file))
        for row in df_permanent.itertuples():
            riders.append(Rider(row[PERMANENT_RIDER_NAME_IDX], row[PERMANENT_RIDER_PHONE_IDX], row[PERMANENT_RIDER_LOCATION_IDX]))
    
    with open(os.path.join(DATA_PATH, 'weekly'), 'rb') as pickle_file:
        df_weekly = pd.DataFrame(pickle.load(pickle_file))
        for row in df_weekly.itertuples():
            riders.append(Rider(row[WEEKLY_RIDER_NAME_IDX], row[WEEKLY_RIDER_PHONE_IDX], row[WEEKLY_RIDER_LOCATION_IDX]))

    return riders


def drivers_to_list() -> list[Driver]:
    """Return the list of drivers.
    """
    drivers = []

    with open(os.path.join(DATA_PATH, 'drivers'), 'rb') as pickle_file:
        df = pd.DataFrame(pickle.load(pickle_file))

    for row in df.itertuples():
        drivers.append(Driver(row[DRIVER_NAME_IDX], row[DRIVER_PHONE_IDX], row[DRIVER_CAPACITY_IDX]))

    return drivers


def write_assignments(assignments: pd.DataFrame):
    # connect Google Sheets
    gc = gspread.service_account(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), "service_account.json"))
    ws = gc.open_by_key(FINAL_SHEET_KEY).get_worksheet(0)
    
    #reset the formatting of the sheet
    #requests = {"requests": [{"updateCells": {"range": {"sheetId": ws._properties['sheetId']}, "fields": "*"}}]}
    #res = ws.batch_update(requests)
    #print(res)

    ws.clear()
    set_with_dataframe(worksheet=ws, dataframe=assignments)
