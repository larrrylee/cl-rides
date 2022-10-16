"""Implements data cleaning and filtering before assigning groups.
"""

from constants import *
import pandas as pd


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
