from typeclasses.objects import Object, SimObject
from typeclasses.rooms import SimRoom
from evennia import create_object
from evennia.utils.utils import inherits_from

from typeclasses.items.ship_components import LifeSupport


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
        ls = create_object(LifeSupport, key="Nemesis Life Support", location=self)
        ls.used_by = self

    def initialize_cockpit(self):
        for room in self.rooms:
            room.destroy()
        self.rooms = []
        cockpit = create_object(ShipRoom, key="Cockpit")
        self.rooms.append(cockpit)

    def adjust_resources(self, key, amount):
        pass

    def can_fly(self):
        return False

    def can_leave_atmosphere(self):
        return False

    def can_leave_orbit(self):
        return False

    def get_ship_components(self):
        return filter(lambda x: inherits_from(x, ShipComponent) and x.used_by == self, self.contents)

    def fly_to(self, exit):
        pass


class ShipRoom(SimRoom):
    @property
    def ship_parent(self):
        return self.db.ship_parent

    @ship_parent.setter
    def ship_parent(self, value):
        self.db.ship_parent = value

    def at_object_creation(self):
        super(ShipRoom, self).at_object_creation()
        self.atmosphere = [
            {"key": "oxygen", "moles": 0.43997},
            {"key": "nitrogen", "moles": 1.36565}
        ]
        self.ship_parent = None


class ShipComponent(SimObject):
    @property
    def armor(self):
        return self.db.armor

    @armor.setter
    def armor(self, value):
        self.db.armor = value

    @property
    def tonnage(self):
        return self.db.tonnage

    @tonnage.setter
    def tonnage(self, value):
        self.db.tonnage = value

    @property
    def is_disabled(self):
        return self.db.is_disabled

    @is_disabled.setter
    def is_disabled(self, value):
        self.db.is_disabled = value

    @property
    def temperature(self):
        return self.db.temperature

    @temperature.setter
    def temperature(self, value):
        self.db.temperature = value

    """
    Emission strength in dbW
    """
    @property
    def emission_strength(self):
        return self.db.emission_strength

    @emission_strength.setter
    def emission_strength(self, value):
        self.db.emission_strength = value

    """
    Emission frequency in Hz.
    """
    @property
    def emission_frequency(self):
        return self.db.emission_frequency

    @emission_frequency.setter
    def emission_frequency(self, value):
        self.db.emission_frequency = value

    def at_object_creation(self):
        super(ShipComponent, self).at_object_creation()
        self.locks.add("puppet:false()")
        self.tonnage = 0
        self.emission_frequency = 0
        self.emission_strength = 0
        self.is_disabled = False

        self.armor = []
