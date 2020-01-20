from world.organs import OrganType
from world.stats import AttributeEnum
from typeclasses.objects import Object
from evennia import TICKER_HANDLER as tickerhandler
from typeclasses.items.health import WoundTypeEnum, Wound
from enum import Enum
import random


class OrganStateEnum(Enum):
    Active = 1
    Disabled = 2


class Organ(Object):
    wounds = []
    max_health = 100
    organ_type = None
    oxygen_consumption = 0
    organ_state = OrganStateEnum.Active

    def at_object_creation(self):
        super(Organ, self).at_object_creation()
        self.locks.add("puppet:false();organ:true()")
        self.db.wounds = self.wounds
        self.db.used_by = None
        self.db.organ_state = self.organ_state
        self.db.oxygen_consumption = self.oxygen_consumption

        # Set up the timer to call ticks.
        tickerhandler.add(5, self._on_tick)

    def at_implant(self, character):
        self.db.used_by = character

    def at_remove(self, character):
        self.db.used_by = None

    def _on_tick(self):
        if not self.db.used_by:
            return
        if self.organ_state == OrganStateEnum.Disabled:
            return
        self.pre_tick(self.db.used_by)
        self.on_tick(self.db.used_by)

    def pre_tick(self, character):
        if self.oxygen_consumption > 0:
            character.vitals.adjust_blood_oxygen(self.oxygen_consumption * -1)

    def on_tick(self, character):
        pass

    def get_efficiency(self):
        health = sum(map(lambda x: x.severity, self.wounds))
        return 1 - round(health / self.max_health, 2)

    def apply_wound(self, wound):
        existing = next(wound for wound in self.wounds if wound.wound_type == wound.wound_type)
        if not existing:
            self.wounds.append(wound)

        if wound.wound_type == WoundTypeEnum.Hypoxia:
            existing.severity += wound.severity
            return


class Heart(Organ):
    @property
    def heartrate(self):
        return self.db.heartrate
    @heartrate.setter
    def heartrate(self, value):
        self.db.heartrate = value

    def at_object_creation(self):
        super(Heart, self).at_object_creation()
        self.locks.add("puppet:false();organ:true()")
        self.db.heartrate = 60
        self.db.oxygen_consumption = 4.02
        self.db.organ_type = OrganType.Heart

    def on_tick(self, character):
        if self.organ_state == OrganStateEnum.Disabled:
            return

        target_heartrate = self.get_target_heartrate(character)
        heartrate = self.get_heartrate()

        t = .35  # Rate of heartrate change.
        self.heartrate = round((1 - t) * heartrate + t * target_heartrate)

        cardiac_failure_chance = max(0.0,
                                     self.heartrate
                                     - 200.0
                                     - (character.stats.get_attribute(AttributeEnum.Endurance) / 8))
        if random.randint(1, 100) < cardiac_failure_chance:
            character.msg("Your heart stops! Oh no!")
            self.organ_state = OrganStateEnum.Disabled

    def get_heartrate(self):
        return self.db.heartrate

    def get_target_heartrate(self, character):
        exertion = character.vitals.get_exertion()
        resting = self.get_resting_heartrate(character)
        oxygen_deficit = (1 - character.vitals.get_oxygenation()) * 450.0
        return round(resting * (1 + (3 * exertion))) + oxygen_deficit + random.randint(-2, 2)

    def get_resting_heartrate(self, character):
        stamina = character.stats.get_attribute(AttributeEnum.Endurance)

        return round(75 - (((stamina - 50) / 100) * 30))

    def get_flow(self, character):
        stroke_volume = 70 * (character.db.body.cur_blood / character.db.body.max_blood)
        return self.get_heartrate() * stroke_volume


class Lungs(Organ):
    oxygen_input = 28

    def on_tick(self, character):
        average_flow = 5000  # Maybe make max blood ML?

        # Get our pumping-organ thingy. If we have one. If we don't..
        # Well that's rough buddy.
        heart = character.organs.find_organ(OrganType.Heart)
        if not heart or heart.organ_state == OrganStateEnum.Disabled:
            return  # No oxygen for you...

        # How efficiently are our lungs working?
        # If they're damaged or the air is thin, this can be compensated for by a faster
        # heart rate.
        efficiency = self.get_efficiency()
        heart_overdrive = (heart.get_flow(character) - average_flow) / 1000
        efficiency = min(1.1, efficiency + heart_overdrive)
        # Add the oxygen_input (base lung efficiency) to our blood.
        oxygen = round(self.oxygen_input * efficiency, 2)
        character.vitals.adjust_blood_oxygen(oxygen)


class ConsciousnessState(Enum):
    Alert = 1,
    Blackout = 2,
    Dead = 3


class Brain(Organ):
    conciousness = ConsciousnessState.Alert
    organ_type = OrganType.NervousSystem
    oxygen_consumption = 17.5

    def at_object_creation(self):
        super(Brain, self).at_object_creation()
        self.locks.add("puppet:false();organ:true()")
        self.db.conciousness = self.conciousness

    def on_tick(self, character):
        oxygenation = character.vitals.get_oxygenation()
        if oxygenation < 0.92:
            damage_rate = 1 - (0.92 / oxygenation)
            damage = 1.2 * damage_rate
            self.apply_wound(Wound(WoundTypeEnum.Hypoxia, damage))

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
    oxygen_consumption = 1.5
    organ_type = OrganType.Filtration

    def at_object_creation(self):
        super(Liver, self).at_object_creation()
        self.locks.add("puppet:false();organ:true()")
        self.db.speed = self.speed

    def on_tick(self, character):
        reagents = character.vitals.get_blood_contents()
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

    def on_tick(self, character):
        for food in self.contents:
            pass  # TODO: Process food into reagents in the blood, or to increase body energy.
