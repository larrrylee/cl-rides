"""Implements all the logic for the assigning drivers and riders.
Includes group optimization for common pickup locations.
"""

from sqlite3 import Timestamp
from config import *
import pandas as pd
import postprocessing as post
import preprocessing as prep
from rides_data import *


def assign(df: pd.DataFrame, rf: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
    """Assigns rider to drivers in the returned dataframe, and updates driver timestamp for the last time they drove.

    PRECONDITION: add_temporaries must have been called on df.
    """
    rf.sort_values(by=RIDER_LOCATION_KEY, inplace=True, key=lambda col: col.apply(lambda loc: loc_map.get(loc, loc_map[ELSEWHERE])))
    out = pd.concat([pd.DataFrame(columns=[OUTPUT_DRIVER_NAME_KEY, OUTPUT_DRIVER_PHONE_KEY]), rf[[RIDER_NAME_KEY, RIDER_PHONE_KEY, RIDER_LOCATION_KEY, RIDER_NOTES_KEY]]], axis='columns')
    out.reset_index(inplace=True, drop=True)    # TODO: possibly remove

    if debug:
        print('Drivers')
        print(df)
        print('Riders')
        print(rf)
        print('Assigning started')

    for r_idx in out.index:
        rider_loc = loc_map.get(out.at[r_idx, RIDER_LOCATION_KEY], loc_map[ELSEWHERE])

        if rider_loc == loc_map[ELSEWHERE]:
            #TODO: do not assign for now
            if debug:
                print(f'\t{out.at[r_idx, RIDER_NAME_KEY]} is not from a prerecorded location, assigning skipped')
            continue

        is_matched = False

        # Check if a driver is already there or one place away.
        for d_idx, driver in df.iterrows():
            if _is_there_or_open(driver, rider_loc):
                _add_rider(out, r_idx, df, d_idx)
                is_matched = True
                break
            if _is_nearby_n(driver, rider_loc, 1):
                _add_rider(out, r_idx, df, d_idx)
                is_matched = True
                break

        if is_matched:
            continue

        # Check if a driver route is two places away.
        for d_idx, driver in df.iterrows():
            if _is_nearby_n(driver, rider_loc, 2):
                _add_rider(out, r_idx, df, d_idx)
                is_matched = True
                break

        if is_matched:
            continue

        # Check if any driver is available.
        for d_idx, driver in df.iterrows():
            if _has_opening(driver):
                _add_rider(out, r_idx, df, d_idx)
                is_matched = True
                break

    return out


def sync_to_last_assignments(df: pd.DataFrame, rf: pd.DataFrame, out: pd.DataFrame) -> pd.DataFrame:
    """Synchronize driver stats to reflect the precalculated assignments. Preassigned riders will be removed from `rf`.

    If synchronization is not possible with the given drivers, the output will be adjusted to match driver availability.
    PRECONDITION: add_temporaries must have been called on df.
    """
    synced_out = pd.DataFrame()
    d_idx = None
    valid = False
    for idx in out.index:
        phone = out.at[idx, OUTPUT_DRIVER_PHONE_KEY]
        if phone != '':
            # Found new driver phone
            d_idx = df[df[DRIVER_PHONE_KEY] == phone].first_valid_index()
            valid = d_idx is not None

        if valid:
            # update driver stats, remove rider from form, transfer to synced dataframe
            df.at[d_idx, DRIVER_OPENINGS_KEY] -= 1
            entry = out.iloc[[idx]]
            rider_loc = loc_map.get(entry.at[entry.index[0], RIDER_LOCATION_KEY], loc_map[ELSEWHERE])
            df.at[d_idx, DRIVER_ROUTE_KEY] |= rider_loc
            rf.drop(rf[rf[RIDER_PHONE_KEY] == entry.at[entry.index[0], RIDER_PHONE_KEY]].index, inplace=True)
            synced_out = pd.concat([synced_out, entry])
    return synced_out


def assign_sunday(df: pd.DataFrame, rf: pd.DataFrame, clear: bool, debug: bool) -> pd.DataFrame:
    """Assigns Sunday rides.
    """
    riders = prep.filter_sunday(rf)
    drivers = prep.prep_necessary_drivers(df, len(riders))
    out = assign(drivers, riders, debug)
    post.alert_skipped_riders(out, debug)
    post.clean_output(out, df)
    return out


def assign_friday(df: pd.DataFrame, rf: pd.DataFrame, clear: bool, debug: bool) -> pd.DataFrame:
    """Assigns Friday rides.
    """
    riders = prep.filter_friday(rf)
    drivers = prep.prep_necessary_drivers(df, len(riders))
    out = assign(drivers, riders, debug)
    post.alert_skipped_riders(out, debug)
    post.clean_output(out, df)
    return out


def _add_rider(out: pd.DataFrame, r_idx: int, df: pd.DataFrame, d_idx: int):
    """Assigns rider to driver and updates driver openings and locations.
    """
    out.at[r_idx, OUTPUT_DRIVER_NAME_KEY] = df.at[d_idx, DRIVER_NAME_KEY]
    out.at[r_idx, OUTPUT_DRIVER_PHONE_KEY] = df.at[d_idx, DRIVER_PHONE_KEY]
    rider_loc = loc_map.get(out.at[r_idx, RIDER_LOCATION_KEY], loc_map[ELSEWHERE])
    df.at[d_idx, DRIVER_OPENINGS_KEY] -= 1
    df.at[d_idx, DRIVER_ROUTE_KEY] |= rider_loc
    df.at[d_idx, DRIVER_TIMESTAMP_KEY] = Timestamp.now()


def _is_nearby_n(driver: pd.Series, rider_loc: int, dist: int) -> bool:
    """Checks if driver has no assignments or is already picking up at the same area as the rider.
    """
    return _has_opening(driver) and (_is_free(driver) or _is_intersecting(driver, rider_loc << dist) or _is_intersecting(driver, rider_loc >> dist))


def _is_there_or_open(driver: pd.Series, rider_loc: int) -> bool:
    """Checks if driver has no assignments or is already picking up at the same college as the rider.
    """
    return _has_opening(driver) and (_is_free(driver) or _is_intersecting(driver, rider_loc))


def _has_opening(driver: pd.Series) -> bool:
    """Checks if driver has space to take a rider.
    """
    return driver[DRIVER_OPENINGS_KEY] > 0


def _is_free(driver: pd.Series) -> bool:
    """Checks if driver is completely free (no riders assigned).
    """
    return driver[DRIVER_ROUTE_KEY] == DEFAULT_LOCS_CODE


def _is_intersecting(driver: pd.Series, rider_loc: int) -> bool:
    """Checks if a driver route intersects with a rider's location.
    """
    driver_loc = driver[DRIVER_ROUTE_KEY]
    return (driver_loc & rider_loc) != 0