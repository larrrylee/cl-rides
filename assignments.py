from cmath import nan
from datetime import date
import numpy as np
import pandas as pd
from rides_data import *

DRIVER_OPENINGS_KEY = 'Open seats'
DRIVER_AREA_KEY = 'Area'
DEFAULT_AREA_CODE = 0
CAMPUS_SOUTHWEST_CODE = 1
CAMPUS_NORTHWEST_CODE = 2
CAMPUS_EAST_CODE = 3
OFF_CAMPUS_CODE = 4
AREA_MAP = {
    'Marshall': CAMPUS_NORTHWEST_CODE,
    'Muir': CAMPUS_SOUTHWEST_CODE,
    'ERC': CAMPUS_NORTHWEST_CODE,
    'Revelle': CAMPUS_SOUTHWEST_CODE,
    'Sixth': CAMPUS_SOUTHWEST_CODE,
    'Seventh': CAMPUS_NORTHWEST_CODE,
    'Warren': CAMPUS_EAST_CODE,
    'Pepper Canyon': CAMPUS_EAST_CODE,
    None: OFF_CAMPUS_CODE
}


def assign(df: pd.DataFrame, rf: pd.DataFrame) -> pd.DataFrame:
    out = pd.concat([pd.DataFrame(columns=[OUTPUT_DRIVER_NAME_KEY, OUTPUT_DRIVER_PHONE_KEY]), rf[[RIDER_NAME_KEY, RIDER_PHONE_KEY, RIDER_LOCATION_KEY, RIDER_NOTES_KEY]]], axis='columns')
    out.reset_index(inplace=True)
    df[DRIVER_OPENINGS_KEY] = df[DRIVER_CAPACITY_KEY]
    df[DRIVER_AREA_KEY] = DEFAULT_AREA_CODE
    print(df)

    for r_idx in range(len(out)):
        for d_idx, driver in df.iterrows():
            if driver[DRIVER_OPENINGS_KEY] > 0 and (driver[DRIVER_AREA_KEY] == DEFAULT_AREA_CODE or driver[DRIVER_AREA_KEY] == AREA_MAP.get(out.at[r_idx, RIDER_LOCATION_KEY], OFF_CAMPUS_CODE)):
                out.at[r_idx, OUTPUT_DRIVER_NAME_KEY] = driver[DRIVER_NAME_KEY]
                out.at[r_idx, OUTPUT_DRIVER_PHONE_KEY] = driver[DRIVER_PHONE_KEY]
                df.at[d_idx, DRIVER_OPENINGS_KEY] -= 1
                df.at[d_idx, DRIVER_AREA_KEY] = AREA_MAP.get(out.at[r_idx, RIDER_LOCATION_KEY], OFF_CAMPUS_CODE)
                df.at[d_idx, DRIVER_TIMESTAMP_KEY] = date.today()
                break
    
    for _, rider in out.iterrows():
        if rider[OUTPUT_DRIVER_NAME_KEY] == np.NaN:
            print(f'{rider[RIDER_NAME_KEY]} has no driver')

    df.drop(columns=[DRIVER_OPENINGS_KEY, DRIVER_AREA_KEY])
    out.sort_values(by=[OUTPUT_DRIVER_NAME_KEY, RIDER_LOCATION_KEY], inplace=True)
    return out


def assign_sunday(df: pd.DataFrame, rf: pd.DataFrame) -> pd.DataFrame:
    #TODO
    pass


def assign_friday(df: pd.DataFrame, rf: pd.DataFrame) -> pd.DataFrame:
    #TODO
    pass