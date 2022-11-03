""" Main file for automatic driver assignments.

Usage:
    python rides.py
"""

import assignments as group
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
    print('    --update              Fetches new data from the sheet and updates the output sheet')
    print('    --debug               Prints out debug statements while running')
    print('    --help                Shows usage')
    print('    --friday              Assigns rides for Friday College Life')
    print('    --sunday              Assigns rides for sunday service')
    print('    --clear               Previous assignments are cleared and drivers are rotated based on date last driven')
    print('    --no-clear            Previous assignments are retained and new assignments are appended')
    print()


def main(update: bool, friday: bool, clear: bool, debug: bool) -> None:
    """ Assign riders to drivers, updating the sheet if specified
    """

    # Fetch data from sheets
    if update:
        data.update_pickles()

    # Print input
    if debug:
        data.print_pickles()

    # Execute the assignment algorithm
    (drivers, riders) = data.get_cached_data()
    prep.clean_data(drivers, riders)
    if friday:
        out = group.assign_friday(drivers, riders, clear, debug)
    else:
        out = group.assign_sunday(drivers, riders, clear, debug)
    
    data.update_drivers_locally(drivers)

    # Print output
    if debug:
        print('Driver output')
        print(drivers)
        print('Assignments output')
        print(out)

    if update:
        data.write_assignments(out)
        #data.update_drivers(drivers)


if __name__ == '__main__':
    execute = True
    update = False
    debug = False
    friday = False
    sunday = False
    clear = False
    no_clear = False

    for argv in sys.argv[1:]:
        if argv == '--update':
            update = True
        elif argv == '--debug':
            debug = True
        elif argv == '--help':
            execute = False
        elif argv == '--friday':
            friday = True
        elif argv == '--sunday':
            sunday = True
        elif argv == '--clear':
            clear = True
        elif argv == '--no-clear':
            no_clear = True
    
    valid_day = friday != sunday
    valid_clear_opt = clear != no_clear
    execute = execute and valid_day and valid_clear_opt

    if execute:
        main(update, friday, clear, debug)
    else:
        show_usage()
