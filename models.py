from operator import truediv
import string


class Rider:
    def __init__(self, name: string, phone: string, location: string):
        # TODO
        self.name = name
        self.phone = phone
        self.location = location
        self.driver = None
    

    def __str__(self) -> str:
        return f'Rider: {self.name}, {self.phone}, {self.location}'
    

    def __repr__(self) -> str:
        return str(self)


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
    
    
    def __str__(self) -> str:
        return f'Driver: {self.name}, {self.phone}, {self.capacity}'
    

    def __repr__(self) -> str:
        return str(self)