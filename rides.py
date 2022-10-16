""" Main file for automatic driver assignments.

Usage:
    python rides.py
"""

import assignments as group
import postprocessing as post
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
        out = group.assign_friday(drivers, riders, debug)
    else:
        out = group.assign_sunday(drivers, riders, debug)
    
    post.rotate_drivers(drivers)
    data.update_drivers_locally(drivers)

    # Print output
    if debug:
        print(drivers)
        print(out)

    if update:
        data.write_assignments(out)
        data.update_drivers(drivers)


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
