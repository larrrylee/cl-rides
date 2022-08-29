import gspread
import json
import os
import pandas as pd
import pickle
from typing import Tuple


def update_pickles():
    # connect Google Sheets
    gc = gspread.service_account(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), "service_account.json"))

    with open('sheet_ids.json') as gid_json:
        gid_data = json.load(gid_json)

    for key in gid_data:
        ws = gc.open_by_key(gid_data[key]).get_worksheet(0)
        records = ws.get_all_records()
        with open(os.path.join('pickle', key), 'wb') as pickle_file:
            pickle.dump(records, pickle_file)


def print_pickles():
    with open('sheet_ids.json') as gid_json:
        keys = json.load(gid_json).keys()

    for key in keys:
        with open(os.path.join('pickle', key), 'rb') as pickle_file:
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
    with open(os.path.join('pickle', 'permanent'), 'rb') as pickle_file:
        permanent_riders = pd.DataFrame(pickle.load(pickle_file))
    
    with open(os.path.join('pickle', 'weekly'), 'rb') as pickle_file:
        weekly_riders = pd.DataFrame(pickle.load(pickle_file))
    
    with open(os.path.join('pickle', 'drivers'), 'rb') as pickle_file:
        drivers = pd.DataFrame(pickle.load(pickle_file))
    
    return (permanent_riders, weekly_riders, drivers)