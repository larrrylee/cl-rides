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

DRIVER_OPENINGS_KEY = 'Open seats'
DRIVER_ROUTE_KEY = 'Locations'

DEFAULT_LOCS_CODE = 0b0
elsewhere_code = 0b0

loc_map = {
    REVELLE:       0b0,
    MUIR:          0b0,
    SIXTH:         0b0,
    MARSHALL:      0b0,
    ERC:           0b0,
    SEVENTH:       0b0,
    WARREN:        0b0,
    PEPPER_CANYON: 0b0,
    RITA_ATKINSON: 0b0,
    REGENTS:       0b0,
    COSTA_VERDE:   0b0
}
