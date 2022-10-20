"""Includes all constants used in the project.
"""

### Column headers for the dataframes
OUTPUT_DRIVER_NAME_KEY = 'Driver'
OUTPUT_DRIVER_PHONE_KEY = 'Driver Phone #'

DRIVER_TIMESTAMP_KEY = 'Timestamp'
DRIVER_NAME_KEY = 'Name'
DRIVER_PHONE_KEY = 'Phone Number'
DRIVER_CAPACITY_KEY = 'Number of Seats in Car (not including you)'

RIDER_TIMESTAMP_KEY = 'Timestamp'
RIDER_NAME_KEY = 'Rider'
RIDER_PHONE_KEY = 'Rider Phone #'
RIDER_LOCATION_KEY = 'Location'
RIDER_FRIDAY_KEY = 'Friday'
RIDER_SUNDAY_KEY = 'Sunday'
RIDER_NOTES_KEY = 'Notes'

PERMANENT_RIDER_TIMESTAMP_KEY = 'Timestamp'
PERMANENT_RIDER_NAME_KEY = 'Full Name:'
PERMANENT_RIDER_PHONE_KEY = 'Phone Number: '
PERMANENT_RIDER_LOCATION_KEY = 'Where should we pick you up?'
PERMANENT_RIDER_FRIDAY_KEY = 'Which service(s) do you need a permanent ride for? [Friday Night Bible Study | 6:30 pm]'
PERMANENT_RIDER_SUNDAY_KEY = 'Which service(s) do you need a permanent ride for? [Sunday Service | 8:30 am/10:45 am]'
PERMANENT_RIDER_NOTES_KEY = 'Other Notes'

WEEKLY_RIDER_TIMESTAMP_KEY = 'Timestamp'
WEEKLY_RIDER_NAME_KEY = 'Full Name'
WEEKLY_RIDER_PHONE_KEY = 'Phone Number '
WEEKLY_RIDER_LOCATION_KEY = 'Where should we pick you up from?'
WEEKLY_RIDER_FRIDAY_KEY = 'Friday Night Bible Study (Friday @7pm) (Rides from Campus will be provided at Peterson Loop at 6:30 pm)'
WEEKLY_RIDER_SUNDAY_KEY = 'Sunday Service '
WEEKLY_RIDER_NOTES_KEY = 'Additional Comments / Questions / Concerns'


### For parsing the responses for attending the Friday/Sunday services
PERMANENT_RIDE_THERE_KEYWORD = 'yes'
WEEKLY_RIDE_THERE_KEYWORD = 'there'
RIDE_THERE_KEYWORD = 'yes'

### For calculating assignments
MARSHALL = 'Marshall'
MUIR = 'Muir'
ERC = 'ERC'
REVELLE = 'Revelle'
SIXTH = 'Sixth'
SEVENTH = 'Seventh'
WARREN = 'Warren'
PEPPER_CANYON = 'Pepper Canyon Apts'
RITA_ATKINSON = 'Rita Atkinson'
REGENTS = 'Regents'
COSTA_VERDE = 'Costa Verde'

# Enumerating locations, consecutive numbers => neighboring locations
REVELLE_LOC = 0
MUIR_LOC = REVELLE_LOC + 1
SIXTH_LOC = MUIR_LOC + 1
MARSHALL_LOC = SIXTH_LOC + 1
ERC_LOC = MARSHALL_LOC + 1
SEVENTH_LOC = ERC_LOC + 1
WARREN_LOC = SEVENTH_LOC + 1
PEPPER_CANYON_LOC = WARREN_LOC + 1
RITA_ATKINSON_LOC = PEPPER_CANYON_LOC + 2
REGENTS_LOC = RITA_ATKINSON_LOC + 2
COSTA_VERDE_LOC = REGENTS_LOC + 1

ELSEWHERE_CODE = ~(COSTA_VERDE_LOC | (COSTA_VERDE_LOC - 1)) << 1
DEFAULT_LOCS_CODE = 0b0

DRIVER_OPENINGS_KEY = 'Open seats'
DRIVER_ROUTE_KEY = 'Locations'

# Converting enumeration to bitmap, allows to check for location intersection by bitmasking
LOC_MAP = {
    REVELLE:       0b1 << REVELLE_LOC,
    MUIR:          0b1 << MUIR_LOC,
    SIXTH:         0b1 << SIXTH_LOC,
    MARSHALL:      0b1 << MARSHALL_LOC,
    ERC:           0b1 << ERC_LOC,
    SEVENTH:       0b1 << SEVENTH_LOC,
    WARREN:        0b1 << WARREN_LOC,
    PEPPER_CANYON: 0b1 << PEPPER_CANYON_LOC,
    RITA_ATKINSON: 0b1 << RITA_ATKINSON_LOC,
    REGENTS:       0b1 << REGENTS_LOC,
    COSTA_VERDE:   0b1 << COSTA_VERDE_LOC
}