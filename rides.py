""" Main file for automatic driver assignments.

Usage:
    python rides.py
"""

from assignments import assign
import preprocessing as prep
import rides_data as data
import sys


def show_usage() -> None:
    """ Show usage of rides.py
    """
    print('USAGE:')
    print('python rides.py [FLAG] [[FLAG] ...]')
    print()
    print('FLAG')
    print('    --update              Fetches new data from the sheet and updates the output sheet')
    print('    --debug               Prints out debug statements while running')
    print('    --help                Shows usage')
    print('    --friday              Switches to Friday College Life rides instead of Sunday service')
    print()


def main(update: bool, debug: bool, friday: bool) -> None:
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
        riders = prep.filter_friday(riders)
    else:
        riders = prep.filter_sunday(riders)
    
    if debug:
        print(drivers)
        print(riders)

    out = assign(drivers, riders, debug)

    # Print output
    if debug:
        print(out)

    if update:
        data.write_assignments(out)


if __name__ == '__main__':
    execute = True
    update = False
    debug = False
    friday = False

    for argv in sys.argv[1:]:
        if argv == '--update':
            update = True
        elif argv == '--debug':
            debug = True
        elif argv == '--help':
            execute = False
        elif argv == '--friday':
            friday = True

    if execute:
        main(update, debug, friday)
    else:
        show_usage()
