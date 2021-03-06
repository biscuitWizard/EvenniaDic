from typeclasses.objects import SimObject
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils.utils import inherits_from
from typeclasses.items.health import Wound
from typeclasses.rooms import SimRoom
from world.enums import *
import random
import time
from utils.engineering import moles_to_pressure


class BodyPart(SimObject):
    @property
    def wounds(self):
        return self.db.wounds

    @wounds.setter
    def wounds(self, value):
        self.db.wounds = value

    @property
    def max_health(self):
        return self.db.max_health

    @max_health.setter
    def max_health(self, value):
        self.db.max_health = value

    @property
    def size(self):
        return self.db.size

    @size.setter
    def size(self, value):
        self.db.size = value

    @property
    def armor(self):
        return self.db.armor

    @armor.setter
    def armor(self, value):
        self.db.armor = value

    @property
    def internal_categories(self):
        return self.db.internal_categories

    @internal_categories.setter
    def internal_categories(self, value):
        self.db.internal_categories = value

    @property
    def is_hidden(self):
        return self.db.used_by is not None

    def at_object_creation(self):
        super(BodyPart, self).at_object_creation()
        self.locks.add("puppet:false()")
        self.db.wounds = []
        self.db.max_health = 100
        self.db.size = 0

        self.db.armor = []
        self.db.internal_categories = []

        # Set up the timer to call ticks.
        tickerhandler.add(5, self._on_tick)

    def _on_tick(self):
        if self.db.used_by is None:
            return
        if self.organ_state == OrganStateEnum.Disabled:
            return
        self.pre_tick(self.db.used_by)
        self.on_tick(self.db.used_by)

    def get_efficiency(self):
        damage = self.get_damage()
        return 1 - round(damage / self.max_health, 2)

    def get_damage(self):
        return sum(map(lambda x: x.severity, self.wounds))

    def on_death(self):
        return

    def on_revive(self):
        return

    def apply_wound(self, wound, bypass_armor=False):
        if not bypass_armor:
            # Find an armor value that matches the damage type.
            armor = next((a for a in self.armor if a.armor_type == wound.wound_type), None)
            if armor:
                # We found some armor, so continue calculating.
                if wound.severity < armor["min_threshold"]:
                    return  # The armor blocks it completely.
                elif wound.severity < armor["max_threshold"]:
                    # The armor reduces the damage to a minimum of 0.
                    wound.severity -= armor["damage_reduction"]
                    if wound.severity <= 0:
                        return  # the damage was reduced completely.

        existing = next(wound for wound in self.wounds if wound.wound_type == wound.wound_type)
        if not existing:
            self.wounds.append(wound)
            if self.get_damage() >= self.max_health:
                self.on_death()  # check for death
            return

        if wound.wound_type == DamageTypeEnum.Hypoxia:
            existing.severity += wound.severity
            if self.get_damage() >= self.max_health:
                self.on_death()  # check for death
            return

        # Check to see if we just worsen an existing wound.
        worsen_chance = existing.severity + 20
        if random.randint(1, 100) <= worsen_chance:
            existing.severity += wound.severity
            if self.get_damage() >= self.max_health:
                self.on_death()  # check for death
            return

        # It's a new wound! Yuck!
        self.wounds.append(wound)
        if self.get_damage() >= self.max_health:
            self.on_death()  # check for death


class Organ(BodyPart):
    @property
    def organ_type(self):
        return self.db.organ_type

    @organ_type.setter
    def organ_type(self, value):
        self.db.organ_type = value

    @property
    def organ_state(self):
        return self.db.organ_state

    @organ_state.setter
    def organ_state(self, value):
        self.db.organ_state = value

    def at_object_creation(self):
        super(Organ, self).at_object_creation()
        self.locks.add("puppet:false();organ:true()")
        self.db.organ_state = OrganStateEnum.Active
        self.db.organ_type = None

    def on_death(self):
        self.db.organ_state = OrganStateEnum.Disabled

    def on_revive(self):
        self.db.organ_state = OrganStateEnum.Active


class Heart(Organ):
    @property
    def heartrate(self):
        return self.db.heartrate

    @heartrate.setter
    def heartrate(self, value):
        self.db.heartrate = value

    @property
    def base_stoke_volume(self):
        return self.db.base_stoke_volume

    @base_stoke_volume.setter
    def base_stoke_volume(self, value):
        self.db.base_stoke_volume = value

    @property
    def base_resting_heartrate(self):
        return self.db.base_resting_heartrate

    @base_resting_heartrate.setter
    def base_resting_heartrate(self, value):
        self.db.base_resting_heartrate = value

    @property
    def critical_heartrate(self):
        return self.db.critical_heartrate

    @critical_heartrate.setter
    def critical_heartrate(self, value):
        self.db.critical_heartrate = value

    def at_object_creation(self):
        super(Heart, self).at_object_creation()
        self.locks.add("puppet:false();organ:true()")
        self.db.heartrate = 60
        self.db.resource_consumption = [
            {"key": "oxygen", "amount": 4.02}
        ]
        self.db.organ_type = OrganType.Heart
        self.db.base_stoke_volume = 70
        self.db.base_resting_heartrate = 75
        self.db.critical_heartrate = 200

    def on_tick(self, character):
        if self.organ_state == OrganStateEnum.Disabled:
            return

        target_heartrate = self.get_target_heartrate(character)
        heartrate = self.get_heartrate()

        t = .35  # Rate of heartrate change.
        self.heartrate = round((1 - t) * heartrate + t * target_heartrate)

        cardiac_failure_chance = max(0.0,
                                     self.heartrate
                                     - self.db.critical_heartrate
                                     - (character.stats.get_attribute(AttributeEnum.Endurance) / 8))
        if random.randint(1, 100) < cardiac_failure_chance:
            character.msg("Your heart stops! Oh no!")
            self.organ_state = OrganStateEnum.Disabled

    def get_heartrate(self):
        return self.db.heartrate

    def get_target_heartrate(self, character):
        exertion = character.body.get_exertion()
        resting = self.get_resting_heartrate(character)
        oxygen_deficit = (1 - character.body.get_oxygenation()) * 450.0
        return round(resting * (1 + (3 * exertion))) + oxygen_deficit + random.randint(-2, 2)

    def get_resting_heartrate(self, character):
        stamina = character.stats.get_attribute(AttributeEnum.Endurance)

        return round(self.db.base_resting_heartrate - (((stamina - 50) / 100) * (self.db.base_resting_heartrate / 2)))

    def get_flow(self, character):
        # protection from species not set or divide by 0 errors.
        if character.body.max_blood_amount < 1:
            return 0

        stroke_volume = self.db.base_stoke_volume * \
                        (character.body.current_blood_amount / character.body.max_blood_amount)
        return self.get_heartrate() * stroke_volume


class Lungs(Organ):
    @property
    def base_exchange_generation(self):
        return self.db.base_exchange_generation

    @base_exchange_generation.setter
    def base_exchange_generation(self, value):
        self.db.base_exchange_generation = value

    @property
    def exchange_gas(self):
        return self.db.exchange_gas

    @exchange_gas.setter
    def exchange_gas(self, value):
        self.db.exchange_gas = value

    @property
    def inhale_volume_per_tick(self):
        return self.db.inhale_volume_per_tick

    @inhale_volume_per_tick.setter
    def inhale_volume_per_tick(self, value):
        self.db.inhale_volume_per_tick = value

    @property
    def exchange_gas_efficiency(self):
        return self.db.exchange_gas_efficiency

    @exchange_gas_efficiency.setter
    def exchange_gas_efficiency(self, value):
        self.db.exchange_gas_efficiency = value

    @property
    def exhale_gas(self):
        return self.db.exhale_gas

    @exhale_gas.setter
    def exhale_gas(self, value):
        self.db.exhale_gas = value

    @property
    def min_breath_pressure(self):
        return self.db.min_breath_pressure

    @min_breath_pressure.setter
    def min_breath_pressure(self, value):
        self.db.min_breath_pressure = value

    @property
    def last_gasp(self):
        return self.db.last_gasp

    @last_gasp.setter
    def last_gasp(self, value):
        self.db.last_gasp = value

    def at_object_creation(self):
        super(Lungs, self).at_object_creation()

        self.exchange_gas = "oxygen"
        self.base_exchange_generation = 28
        self.exhale_gas = "co2"
        self.exchange_gas_efficiency = 0
        self.inhale_volume_per_tick = 0
        self.db.last_gasp = 0

        self.resource_generation = [
            {"key": self.exchange_gas, "amount": self.base_exchange_generation}
        ]

    def on_tick(self, character):
        average_flow = 5000  # Maybe make max blood ML?

        # Get our pumping-organ thingy. If we have one. If we don't..
        # Well that's rough buddy.
        heart = character.body.organs.find_organ(OrganType.Heart)
        if not heart or heart.organ_state == OrganStateEnum.Disabled:
            return  # No oxygen for you...

        # How efficiently are our lungs working?
        # If they're damaged or the air is thin, this can be compensated for by a faster
        # heart rate.
        efficiency = self.get_efficiency()
        heart_overdrive = (heart.get_flow(character) - average_flow) / 1000
        efficiency = min(1.1, efficiency + heart_overdrive)
        # Add the oxygen_input (base lung efficiency) to our blood.
        gas = round(self.base_exchange_generation * efficiency, 2)

        resource = next((r for r in self.db.resource_generation if r["key"] == self.exchange_gas), None)
        if not resource:
            return

        # Check for the environment for the gas we want!
        location = self.used_by.location
        if inherits_from(location, SimRoom):
            breath = self.get_breath()
            inhale_gas = next((b for b in breath["gases"] if b["key"] == self.exchange_gas), None)
            inhale_moles = 0
            if inhale_gas:
                inhale_moles = inhale_gas["moles"]

            breath_pressure = moles_to_pressure(breath["total_moles"], breath["temperature"], breath["volume"])

            inhale_efficiency = min(round(((inhale_moles / breath["total_moles"]) * breath_pressure)
                                          / self.min_breath_pressure, 3), 3)

            if inhale_efficiency < 1:
                # Not enough to breathe...
                if inhale_efficiency >= 0.8:
                    # Just enough to draw in a shitty breath.
                    gas = gas * inhale_efficiency
                else:
                    gas = 0
                    if time.time() - self.last_gasp > 30:
                        self.last_gasp = time.time()
                        self.used_by.msg("You gasp for breath.")
                        self.used_by.msg("inhale moles: %s" % inhale_moles)
                        self.used_by.msg("total breath moles: %s" % breath["total_moles"])
                        self.used_by.msg("breath pressure: %s" % breath_pressure)
                        self.used_by.msg("inhale efficiency: %s" % inhale_efficiency)

            # Now to deal with adding the exhale back in.
            if inhale_gas:
                exchanged_moles = inhale_gas["moles"] * self.exchange_gas_efficiency * inhale_efficiency
                if inhale_efficiency < 0.8:
                    exchanged_moles = 0
                inhale_gas["moles"] = inhale_gas["moles"] - exchanged_moles
                exhale_gas = next((g for g in breath["gases"] if g["key"] == self.exhale_gas), None)
                if exchanged_moles > 0:
                    if exhale_gas is None:
                        exhale_gas = {
                            "key": self.exhale_gas
                        }
                        breath["gases"].append(exhale_gas)
                    exhale_gas["moles"] = exchanged_moles
                location.add_gas(breath)
        # Update the amount generated
        resource["amount"] = gas

    def get_breath(self):
        if self.inhale_volume_per_tick <= 0:
            return
        location = self.used_by.location
        breath = location.remove_volume(self.inhale_volume_per_tick)
        #  TODO: Maybe some fancy way to handle masks or internal tanks?
        return breath


class Brain(Organ):
    conciousness = ConsciousnessState.Alert
    organ_type = OrganType.NervousSystem

    def at_object_creation(self):
        super(Brain, self).at_object_creation()
        self.locks.add("puppet:false();organ:true()")
        self.db.conciousness = self.conciousness
        self.db.resource_consumption = [
            {"key": "oxygen", "amount": 17.5}
        ]

    def on_tick(self, character):
        oxygenation = character.body.get_oxygenation()
        if oxygenation < 0.92:
            damage_rate = 1 - (0.92 / oxygenation)
            damage = 1.2 * damage_rate
            self.apply_wound(Wound(DamageTypeEnum.Hypoxia, damage))

        # TODO: Check for neurotoxins and apply additional damage.

        # Conciousness check to see if we start blacking out from
        # brain damage or hypoxia.
        if self.conciousness == ConsciousnessState.Alert:
            # Should only start to lose consciousness after about 40% damage.
            blackout_chance = 100 * (.60 - self.get_efficiency())
            if random.randint(1, 100) <= blackout_chance:
                self.conciousness = ConsciousnessState.Blackout
        elif self.conciousness == ConsciousnessState.Blackout:
            wakeup_chance = character.stats.get_attribute(AttributeEnum.Endurance) + (30 * self.get_efficiency())
            if random.randint(1, 100) <= wakeup_chance:
                self.conciousness = ConsciousnessState.Alert


class Liver(Organ):
    speed = 0.5
    organ_type = OrganType.Filtration

    def at_object_creation(self):
        super(Liver, self).at_object_creation()
        self.locks.add("puppet:false();organ:true()")
        self.db.speed = self.speed
        self.db.resource_consumption = [
            {"key": "oxygen", "amount": 1.5}
        ]

    def on_tick(self, character):
        return  # debug
        reagents = character.body.resources
        efficiency = self.get_efficiency()

        for reagent in reagents:
            metabolizability = reagent.metabolizability
            if not metabolizability:  # Guard Check
                continue

            # TODO: Add a check for reagents that damage the liver.

            # Remove an amount of millilitres from the body corresponding
            # to the capability, damage, and metabolizability of the compound.

            metabolized = efficiency * metabolizability * self.speed
            reagent.amountMilliliters -= metabolized
            # TODO: Add mechanics that apply a reagent's mechanical effects /w ratio to amount metabolized

            if reagent.amountMilliliters <= 0:
                pass  # Need some code here to REMOVE the compound from the blood.


class Stomach(Organ):
    contents = []
    oxygen_consumption = 1
    organ_type = OrganType.Digestive

    def at_object_creation(self):
        super(Stomach, self).at_object_creation()
        self.locks.add("puppet:false();organ:true()")
        self.db.contents = self.contents
        self.db.resource_consumption = [
            {"key": "oxygen", "amount": 1}
        ]

    def on_tick(self, character):
        for food in self.contents:
            pass  # TODO: Process food into reagents in the blood, or to increase body energy.
