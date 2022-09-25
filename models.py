from operator import truediv
import string


class Rider:
    def __init__(self, name: string, phone: string, location: string):
        # TODO
        self.name = name
        self.phone = phone
        self.location = location
        self.driver = None

class Driver:
    def __init__(self, name: string, phone: string, capacity: int):
        #TODO
        self.name = name
        self.phone = phone
        self.capacity = capacity
        self.riders = []
    

    def add_rider(self, rider: Rider) -> bool:
        if len(self.riders) < self.capacity and self.riders.count(rider) == 0:
            rider.driver = self
            self.riders.append(rider)
            self.capacity += 1
            return True
        return False