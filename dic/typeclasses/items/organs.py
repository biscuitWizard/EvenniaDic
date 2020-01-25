from typeclasses.objects import Object
from evennia import TICKER_HANDLER as tickerhandler
from typeclasses.items.health import Wound
from world.enums import *
import random


class BodyPart(Object):
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
    def used_by(self):
        return self.db.used_by

    @used_by.setter
    def used_by(self, value):
        self.db.used_by = value

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

    def at_object_creation(self):
        super(BodyPart, self).at_object_creation()
        self.locks.add("puppet:false()")
        self.db.wounds = []
        self.db.used_by = None
        self.db.max_health = 100
        self.db.size = 0

        self.db.resource_consumption = []
        self.db.resource_generation = []
        self.db.resource_storage = []

        self.db.armor = []
        self.db.internal_categories = []

        # Set up the timer to call ticks.
        tickerhandler.add(5, self._on_tick)

    def at_implant(self, character):
        self.db.used_by = character

    def at_remove(self, character):
        self.db.used_by = None

    def _on_tick(self):
        if self.db.used_by is None:
            return
        if self.organ_state == OrganStateEnum.Disabled:
            return
        self.pre_tick(self.db.used_by)
        self.on_tick(self.db.used_by)

    def pre_tick(self, character):
        for resource in self.resource_consumption:
            amount = resource["amount"]
            character.body.adjust_resources(resource["key"], amount * -1)

        for resource in self.resource_generation:
            amount = resource["amount"] * self.get_efficiency()
            character.body.adjust_resources(resource["key"], amount)

    def on_tick(self, character):
        pass

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

    def at_object_creation(self):
        super(Lungs, self).at_object_creation()

        if not self.exchange_gas:
            self.exchange_gas = "oxygen"
        if not self.base_exchange_generation:
            self.base_exchange_generation = 28

        self.db.resource_generation = [
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
        # Update the amount generated
        resource["amount"] = gas


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
