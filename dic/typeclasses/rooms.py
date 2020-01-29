"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from evennia import TICKER_HANDLER as tickerhandler
from world.content.gases import specific_entropy_gas, MINIMUM_TRANSFER_MOLES, R_IDEAL_GAS_EQUATION
from utils.engineering import moles_to_pressure


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    pass


class SimRoom(Room):
    @property
    def atmosphere(self):
        return self.db.atmosphere

    @atmosphere.setter
    def atmosphere(self, value):
        self.db.atmosphere = value

    @property
    def total_moles(self):
        moles = 0
        for atmo_gas in self.atmosphere:
            moles += atmo_gas["moles"]
        return moles

    """
    Size variable determines how many occupants can fit in this room.
    
    A size of 1 means only 1 character object can fit in the room.
    
    A size of 20 means 20 character objects can fit in the room.
    """
    @property
    def size(self):
        return self.db.size

    @size.setter
    def size(self, value):
        self.db.size = value

    """
    Rough volume calculations for a space. This is presented as cubic metres.
    """
    @property
    def volume(self):
        return self.size * 2

    """
    Rough volume calculations for a space. This is presented as litres.
    """
    @property
    def volume_litres(self):
        return self.volume * 1000

    """
    Pressure in kPA for room.
    """
    @property
    def pressure(self):
        return moles_to_pressure(self.total_moles, self.temperature, self.volume_litres)

    """
    Temperature in Kelvin.
    """
    @property
    def temperature(self):
        return self.db.temperature

    @temperature.setter
    def temperature(self, value):
        self.db.temperature = value

    @property
    def is_outside(self):
        return self.db.is_outside

    @is_outside.setter
    def is_outside(self, value):
        self.db.is_outside = value

    def at_object_creation(self):
        super(SimRoom, self).at_object_creation()

        self.atmosphere = []
        self.size = 1
        self.is_outside = False
        self.temperature = 273.15

        tickerhandler.add(5, self._on_tick)

    def _on_tick(self):
        #  TODO: For each open exit, equalize gas with adjoined room.
        pass

    """
    Generalized scrubber def that 'scrubs/removes' gasses not listed
    in filtered_gasses.
    
    Returns power in watts required to move the gas.
    """
    def scrub_gas(self, filtered_gases, total_transfer_moles):
        if self.total_moles < MINIMUM_TRANSFER_MOLES:
            return -1  # Don't bother below the armstrong limit.
        total_filterable_moles = 0   # How much gas there actually is to filter.
        total_power = 0
        for atmo_gas in self.atmosphere:
            if atmo_gas["key"] in filtered_gases or atmo_gas["moles"] < MINIMUM_TRANSFER_MOLES:
                continue

            total_filterable_moles += atmo_gas["moles"]
            specific_entropy = specific_entropy_gas(atmo_gas["key"], self.temperature, atmo_gas["moles"], self.volume)
            specific_power = 0  # W/mol
            if specific_entropy > 0:
                specific_power = -specific_entropy * self.temperature

            total_power += specific_power

        if total_filterable_moles < MINIMUM_TRANSFER_MOLES:
            return -1

        total_filterable_moles = min(total_transfer_moles, total_filterable_moles)

        for atmo_gas in self.atmosphere:
            if atmo_gas["key"] in filtered_gases or atmo_gas["moles"] < MINIMUM_TRANSFER_MOLES:
                continue
            transfer_moles = atmo_gas["moles"]
            transfer_moles = min(transfer_moles, total_transfer_moles * (atmo_gas["moles"] / total_filterable_moles))
            self.adjust_gas(atmo_gas["key"], -transfer_moles)

        return total_power

    def adjust_gas(self, key, amount):
        atmo_gas = next((g for g in self.atmosphere if g["key"] == key), None)
        if amount <= 0 and atmo_gas is None:
            return

        atmo_gas["moles"] = max(0, atmo_gas["moles"] + amount)
        if atmo_gas["moles"] == 0:
            self.atmosphere.remove(atmo_gas)

    def equalize_gas_with(self, sink_room):
        pass

    """
    Removes a volume (in litres) of gas from the room. Returns an object with
    info about the contents of that gas.
    """
    def remove_volume(self, volume):
        result = {
            "gases": [],
            "temperature": self.temperature,
            "volume": volume,
            "total_moles": 0
        }

        ratio = volume / self.volume_litres
        for atmo_gas in self.atmosphere:
            gas = {
                "key": atmo_gas["key"],
                "moles": atmo_gas["moles"] * ratio
            }
            atmo_gas["moles"] -= gas["moles"]
            result["total_moles"] += gas["moles"]
            result["gases"].append(gas)

        return result

    def add_gas(self, gas_mixture):
        for gas in gas_mixture["gases"]:
            atmo_gas = next((g for g in self.atmosphere if g["key"] == gas["key"]), None)
            if atmo_gas is None:
                atmo_gas = {
                    "key": gas["key"],
                    "moles": 0
                }
                self.atmosphere.append(atmo_gas)
            atmo_gas["moles"] += gas["moles"]



