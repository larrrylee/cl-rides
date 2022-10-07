""" Main file for automatic driver assignments.

Usage:
    python rides.py
"""

from assignments import assign
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
    print()


def main(update: bool, debug: bool) -> None:
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
    data.clean_data(drivers, riders)
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

    for argv in sys.argv[1:]:
        if argv == '--update':
            update = True
        elif argv == '--debug':
            debug = True
        elif argv == '--help':
            execute = False

    if execute:
        main(update, debug)
    else:
        show_usage()
