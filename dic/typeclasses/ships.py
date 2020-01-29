from typeclasses.objects import Object
from typeclasses.rooms import SimRoom
from evennia import create_object


class Ship(Object):
    @property
    def is_landed(self):
        return self.db.is_landed

    @is_landed.setter
    def is_landed(self, value):
        self.db.is_landed = value

    @property
    def tonnage(self):
        return self.db.tonnage

    @tonnage.setter
    def tonnage(self, value):
        self.db.tonnage = value

    @property
    def registered_to(self):
        return self.db.registered_to

    @registered_to.setter
    def registered_to(self, value):
        self.db.registered_to = value

    @property
    def hull_temperature(self):
        return self.db.hull_temperature

    @hull_temperature.setter
    def hull_temperature(self, value):
        self.db.hull_temperature = value

    @property
    def rooms(self):
        return self.db.rooms

    @rooms.setter
    def rooms(self, value):
        self.db.rooms = value

    def at_object_creation(self):
        super(Ship, self).at_object_creation()

        self.is_landed = True
        self.tonnage = 100
        self.registered_to = None
        self.hull_temperature = 30
        self.rooms = []
        self.is_item = False

        self.initialize_cockpit()

    def initialize_cockpit(self):
        for room in self.rooms:
            room.destroy()
        self.rooms = []
        cockpit = create_object(ShipRoom, key="Cockpit")
        self.rooms.append(cockpit)

    def adjust_resources(self, key, amount):
        pass


class ShipRoom(SimRoom):
    def at_object_creation(self):
        super(ShipRoom, self).at_object_creation()
        self.atmosphere = [
            {"key": "oxygen", "moles": 0.43997},
            {"key": "nitrogen", "moles": 1.36565}
        ]
