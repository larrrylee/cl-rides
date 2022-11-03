"""Test script for the rides automation.
"""

import assignments as group
import preprocessing as prep
import rides
import rides_data as data


def main():
    run_sunday()


def run_sunday():
    rides.main(True, False, True, True)


def test_sync():
    prep.load_map()
    (drivers, riders) = data.get_cached_data()
    prev_out = data.get_prev_assignments()
    prep.clean_data(drivers, riders)

    print('Drivers ------------------------------------')
    print(drivers)
    print()
    print('Riders -------------------------------------')
    print(riders)
    print()
    print('Previous assignments -----------------------')
    print(prev_out)
    print()

    riders = prep.filter_sunday(riders)
    prep._add_temporaries(drivers)
    out = group.sync_to_last_assignments(drivers, riders, prev_out)

    print('Drivers OUT --------------------------------')
    print(drivers)
    print()
    print('Riders OUT ---------------------------------')
    print(riders)
    print()
    print('Assignments OUT ----------------------------')
    print(out)
    print()


if __name__ == '__main__':
    main()