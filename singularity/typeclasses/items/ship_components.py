from typeclasses.ships import ShipComponent
from evennia.utils.utils import inherits_from
from typeclasses.rooms import SimRoom
from world.content.gases import R_IDEAL_GAS_EQUATION, GASES, CO2


class PowerPlant(ShipComponent):
    pass


class Sensors(ShipComponent):
    pass


class StorageTank(ShipComponent):
    @property
    def volume(self):
        return self.db.volume

    @volume.setter
    def volume(self, value):
        self.db.volume = value

    @property
    def max_pressure(self):
        return self.db.max_pressure

    @max_pressure.setter
    def max_pressure(self, value):
        self.db.max_pressure = value

    @property
    def internal_temperature(self):
        return self.db.internal_temperature

    @internal_temperature.setter
    def internal_temperature(self, value):
        self.db.internal_temperature = value


class HeatPump(StorageTank):
    @property
    def pump_max_temperature(self):
        return self.db.pump_max_temperature

    @pump_max_temperature.setter
    def pump_max_temperature(self, value):
        self.db.pump_max_temperature = value

    @property
    def is_auto(self):
        """
        The mode setting for this heatpump. Manual or Auto. If Auto,
        attempt to automatically dump heat near max temp.
        :return: Boolean
        """
        return self.db.is_auto

    @is_auto.setter
    def is_auto(self, value):
        self.db.is_auto = value

    @property
    def desired_temperature(self):
        """
        The desired temperature for the ship. The heat pump will constantly
        strive to reach this thermostasis.
        :return: Number in Kelvin
        """
        return self.db.desired_temperature

    @desired_temperature.setter
    def desired_temperature(self, value):
        self.db.desired_temperature = value

    @property
    def heat_coefficient(self):
        """
        How efficient/how many kelvin the HeatPump can move every tick.
        :return: Presumably a number between 0.05-10 is preferred.
        """
        return self.db.heat_coefficient

    @heat_coefficient.setter
    def heat_coefficient(self, value):
        self.db.heat_coefficient = value

    def get_kelvin_moved(self, source_temp):
        internal_temperature = max(0.0000001, self.internal_temperature) # Divide by 0 protection
        base_efficiency = min(3, self.pump_max_temperature / internal_temperature) * self.get_efficiency()

        heat_possible = base_efficiency * self.heat_coefficient
        desired_moved = max(0, source_temp - self.desired_temperature)

        return min(heat_possible, desired_moved)


class Radiator(ShipComponent):
    pass


class Battery(ShipComponent):
    pass


class MainEngine(ShipComponent):
    @property
    def base_fuel_consumption(self):
        """
        How much fuel is used at WOT on this engine per tick.
        :return: Propellant in litres
        """
        return self.db.base_fuel_consumption

    @base_fuel_consumption.setter
    def base_fuel_consumption(self, value):
        self.db.base_fuel_consumption = value

    @property
    def base_energy_consumption(self):
        """
        How much electrical energy this engine consumes base
        at wide open throttle.
        :return: Number in kWh.
        """
        return self.db.base_energy_consumption

    @base_energy_consumption.setter
    def base_energy_consumption(self, value):
        self.db.base_energy_consumption = value

    @property
    def base_heat_generation(self):
        """
        How much heat this engine produces per tick
        at wide open throttle.
        :return: Heat in kelvin.
        """
        return self.db.base_heat_generation

    @base_heat_generation.setter
    def base_heat_generation(self, value):
        self.db.base_heat_generation = value

    @property
    def thrust_power(self):
        """
        The amount of power this engine is capable of producing. This
        is an imaginary number for all considered things. Consider this the
        newtons this engine can generate per ton it weighs.
        :return: Fake numbers.
        """
        return self.db.thrust_power

    @thrust_power.setter
    def thrust_power(self, value):
        self.db.thrust_power = value

    @property
    def throttle(self):
        """
        How wide open this engine is. Scales from 0-1.
        :return: 0-1 (0-100%) throttle.
        """
        return self.db.throttle

    @throttle.setter
    def throttle(self, value):
        self.db.throttle = value

    @property
    def propellant(self):
        """
        The type of propellant this engine is using.
        :return: The key of the element.
        """
        return next((g for g in GASES if g["key"] == self.db.propellant), CO2)

    @propellant.setter
    def propellant(self, value):
        self.db.propellant = value["key"]

    @property
    def boot_time(self):
        """
        How many ticks it takes the engine to warm up before being flight ready.
        :return: Ticks.
        """
        return self.db.boot_time

    @boot_time.setter
    def boot_time(self, value):
        self.db.boot_time = value

    def at_object_creation(self):
        super(MainEngine, self).at_object_creation()

        self.thrust_power = 0
        self.throttle = 0
        self.base_fuel_consumption = 0
        self.base_energy_consumption = 0
        self.base_heat_generation = 0
        self.propellant = None
        self.boot_time = 0

    def on_tick(self, parent):
        self.resource_consumption = [
            {"key": self.propellant, "amount": self.calc_fuel_consumption()},
            {"key": "energy", "amount": self.calc_energy_consumption()}
        ]

        self.resource_generation = [
            {"key": "heat", "amount": self.calc_heat_generation()}
        ]

    def calc_acceleration(self):
        """
        Gets the m/s this engine is capable of accelerating the attached ship by.
        :return: m/s
        """
        return (self.tonnage / self.used_by.gross_tonnage) \
               * self.throttle \
               * self.thrust_power \
               * (CO2["molar_mass"] / self.propellant["molar_mass"]) \
               * self.get_efficiency()

    def calc_fuel_consumption(self):
        """
        Gets the kg/tick this engine is consuming.
        :return: kg/tick propellant
        """
        ticks_per_second = 60 / 5
        return (self.tonnage / self.used_by.gross_tonnage) \
               * self.throttle \
               * self.base_fuel_consumption \
               / ticks_per_second

    def calc_energy_consumption(self):
        ticks_per_second = 60 / 5
        return (self.tonnage / self.used_by.gross_tonnage) \
               * self.base_energy_consumption \
               / ticks_per_second

    def calc_heat_generation(self):
        return 0


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

    @property
    def preferred_pressure(self):
        return self.db.preferred_pressure

    @preferred_pressure.setter
    def preferred_pressure(self, value):
        self.db.preferred_pressure = value

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

    @property
    def tank_contents(self):
        return self.db.tank_contents

    @tank_contents.setter
    def tank_contents(self, value):
        self.db.tank_contents = value

    @property
    def internal_volume(self):
        return self.db.internal_volume

    @internal_volume.setter
    def internal_volume(self, value):
        self.db.internal_volume = value

    def at_object_creation(self):
        super(LifeSupport, self).at_object_creation()

        self.preferred_pressure = 100
        self.preferred_atmosphere = [{"key": "oxygen", "amount": 0.21}, {"key": "nitrogen", "amount": 0.79}]
        self.preferred_temperature = 273.15
        self.max_siphon_flowrate = 200
        self.tank_contents = []
        self.internal_volume = 10000

        self.update_tank_contents()

    def on_tick(self, ship):
        for room in ship.rooms:
            if not inherits_from(room, SimRoom):
                continue

            # Get all rooms with a VentScrubber installed in them and
            # replace all gasses not listed in preferred_atmosphere
            # slowly over time.
            transfer_moles = min(room.total_moles, room.total_moles * self.max_siphon_flowrate / room.volume)
            room.scrub_gas(map(lambda x: x["key"], self.preferred_atmosphere), transfer_moles)
            # room.scrub_gas([], transfer_moles)

            # TODO: Adjust tank mixture dynamically so the right amount of gases are added back in.
            room.pump_gas_passive(self.tank_contents)

    def update_tank_contents(self):
        if len(self.preferred_atmosphere) == 0:
            return

        total_moles = (self.preferred_pressure*self.internal_volume)/(R_IDEAL_GAS_EQUATION * self.preferred_temperature)
        gas_mixture = {
            "volume": self.internal_volume,
            "temperature": self.preferred_temperature,
            "gases": [],
            "total_moles": total_moles
        }

        for gas_ratio in self.preferred_atmosphere:
            gas = {
                "key": gas_ratio["key"],
                "moles": total_moles * gas_ratio["amount"]
            }
            gas_mixture["gases"].append(gas)

        self.tank_contents = gas_mixture






