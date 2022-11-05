""" Main file for automatic driver assignments.

Usage:
    python rides.py
"""

import assignments as group
from config import GLOBALS, GROUPING_THRESHOLD
import preprocessing as prep
import rides_data as data
import sys


def show_usage() -> None:
    """ Show usage of rides.py
    """
    print('USAGE:')
    print('python rides.py <--friday | --sunday> <--clear | --no-clear> [[FLAG] ...]')
    print()
    print('FLAG')
    print('    --help                Shows usage')
    print('    --debug               Prints out debug statements while running')
    print('    --no-fetch            Prevents new sheet data from being fetched')
    print('    --no-update           Prevents the output sheet from being updated')
    print('    --rotate              Previous assignments are cleared and drivers are rotated based on date last driven')
    print('    --edit                Previous assignments are retained and new assignments are appended')
    print('    --friday              Assigns rides for Friday College Life')
    print('    --sunday              Assigns rides for Sunday service')
    print('    --threshold=<num>     Sets how many open spots a driver must have to spontaneously pick up at a neighboring location. The default is 2.')
    print()


def main(fetch: bool, update: bool, rotate: bool, edit: bool, friday: bool, debug: bool) -> None:
    """ Assign riders to drivers, updating the sheet if specified
    """
    prep.load_map()

    # Fetch data from sheets
    if fetch:
        data.update_pickles()

    # Print input
    if debug:
        data.print_pickles()
    
    (drivers, riders) = data.get_cached_data()
    prep.clean_data(drivers, riders)

    # Do requested preprocessing
    if rotate or edit:
        prev_out = data.get_prev_assignments()
        if rotate:
            # Rotate drivers by last date driven
            prep.rotate_drivers(drivers, prep.get_prev_driver_phones(prev_out))
            data.update_drivers_locally(drivers)
        elif edit:
            #TODO: Load previous output into assignments
            pass

    # Execute the assignment algorithm
    if friday:
        out = group.assign_friday(drivers, riders, debug)
    else:
        out = group.assign_sunday(drivers, riders, debug)
    
    # Print output
    if debug:
        print('Assignments output')
        print(out)

    if update:
        data.write_assignments(out)


if __name__ == '__main__':
    execute = True
    update = True
    fetch = True
    debug = False
    rotate = False
    edit = False
    friday = False
    sunday = False

    for argv in sys.argv[1:]:
        if argv == '--help':
            execute = False
        elif argv == '--debug':
            debug = True
        elif argv == '--no-fetch':
            fetch = False
        elif argv == '--no-update':
            update = False
        elif argv == '--rotate':
            rotate = True
        elif argv == '--edit':
            edit = True
        elif argv == '--friday':
            friday = True
        elif argv == '--sunday':
            sunday = True
        elif argv.find('--threshold') != -1:
            try:
                GLOBALS[GROUPING_THRESHOLD] = int(argv.split('=').pop())
            except:
                execute = False
    
    valid_day = friday != sunday
    valid_clear_opt = not (rotate and edit)
    execute = execute and valid_day and valid_clear_opt

    if execute:
        main(fetch, update, rotate, edit, friday, debug)
    else:
        show_usage()
