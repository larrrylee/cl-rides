import gspread
import json
import pickle
import pandas as pd
import os

FINAL_SHEET_KEY = "15KJPVqZT6pMq8Qg4qufx9iZOArzjxeD_MN-A-ka6Jnk"

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

def main():
    # update_pickles()
    print_pickles()

if __name__ == "__main__":
    main()