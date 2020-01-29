from typeclasses.objects import Object
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils.utils import inherits_from
from typeclasses.ships import ShipRoom


class ShipComponent(Object):
    @property
    def armor(self):
        return self.db.armor

    @armor.setter
    def armor(self, value):
        self.db.armor = value

    @property
    def resource_consumption(self):
        return self.db.resource_consumption

    @resource_consumption.setter
    def resource_consumption(self, value):
        self.db.resource_consumption = value

    @property
    def resource_generation(self):
        return self.db.resource_generation

    @resource_generation.setter
    def resource_generation(self, value):
        self.db.resource_generation = value

    @property
    def resource_storage(self):
        return self.db.resource_storage

    @resource_storage.setter
    def resource_storage(self, value):
        self.db.resource_storage = value

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
    def used_by(self):
        return self.db.used_by

    @used_by.setter
    def used_by(self, value):
        self.db.used_by = value

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
        self.used_by = None
        self.is_disabled = False

        self.resource_consumption = []
        self.resource_generation = []
        self.resource_storage = []

        self.armor = []

        # Set up the timer to call ticks.
        tickerhandler.add(5, self._on_tick)

    def at_install(self, ship):
        self.db.used_by = ship

    def at_remove(self, ship):
        self.db.used_by = None

    def _on_tick(self):
        if self.db.used_by is None or self.is_disabled:
            return
        self.pre_tick(self.db.used_by)
        self.on_tick(self.db.used_by)

    def pre_tick(self, ship):
        for resource in self.resource_consumption:
            amount = resource["amount"]
            ship.adjust_resources(resource["key"], amount * -1)

        for resource in self.resource_generation:
            amount = resource["amount"] * self.get_efficiency()
            ship.adjust_resources(resource["key"], amount)

    def on_tick(self, ship):
        pass


class PowerPlant(ShipComponent):
    pass


class Sensors(ShipComponent):
    pass


class FuelTank(ShipComponent):
    pass


class Radiator(ShipComponent):
    pass


class Battery(ShipComponent):
    pass


class MainEngine(ShipComponent):
    pass


class Thruster(ShipComponent):
    pass


class LifeSupport(ShipComponent):
    @property
    def preferred_atmosphere(self):
        return self.db.preferred_atmosphere

    @preferred_atmosphere.setter
    def preferred_atmosphere(self, value):
        self.db.preferred_atmosphere = value

    @property
    def preferred_temperature(self):
        return self.db.preferred_temperature

    @preferred_temperature.setter
    def preferred_temperature(self, value):
        self.db.preferred_temperature = value

    """
    L/s 
    
    This can be used to balance how fast a room is siphoned.
    """
    @property
    def max_siphon_flowrate(self):
        return self.db.max_siphon_flowrate

    @max_siphon_flowrate.setter
    def max_siphon_flowrate(self, value):
        self.db.max_siphon_flowrate = value

    def at_object_creation(self):
        super(LifeSupport, self).at_object_creation()

        self.preferred_atmosphere = []
        self.preferred_temperature = 30
        self.max_siphon_flowrate = 200

    def on_tick(self, ship):
        for room in ship.rooms:
            if not inherits_from(room, ShipRoom):
                continue

            # Get all rooms with a VentScrubber installed in them and
            # replace all gasses not listed in preferred_atmosphere
            # slowly over time.
            transfer_moles = min(room.total_moles, room.total_moles * self.max_siphon_flowrate / room.size)
            room.scrub_gas(self.preferred_atmosphere.map(lambda x: x["key"]), transfer_moles)






