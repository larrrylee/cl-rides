import string


class Rider:
    def __init__(self, name: string, phone: string, location: string):
        # TODO
        self.name = name
        self.phone = phone
        self.location = location
        self.driver = None

class Driver:
    def __init__(self, name: string, phone: string):
        #TODO
        self.name = name
        self.phone = phone
        self.riders = []
