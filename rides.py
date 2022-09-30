import pandas as pd
from ride_assignments import RideAssignment
import rides_data as data

def main():
    #data.update_pickles()
    #data.print_pickles()
    #assignment = RideAssignment(data.riders_to_list(), data.drivers_to_list())
    #assignment.assign_riders()
    #data.write_assignments(assignment.assignments)

    riders = data.riders_to_list()
    drivers = data.drivers_to_list()
    assignment = RideAssignment(riders, drivers)
    assignment.assign_riders()
    data.write_assignments(assignment)

if __name__ == "__main__":
    main()
