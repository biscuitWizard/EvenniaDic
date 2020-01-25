from world.organs import OrganHandler
from world.limbs import LimbHandler
from evennia.utils import lazy_property
from world.content.species import SPECIES, SPECIES_HUMAN
from world.enums import *


class BodyHandler(object):
    @property
    def resources(self):
        return self.obj.db.body["resources"]

    @resources.setter
    def resources(self, value):
        self.obj.db.body["resources"] = value

    @property
    def wounds(self):
        return self.obj.db.body["wounds"]

    @wounds.setter
    def wounds(self, value):
        self.obj.db.body["wounds"] = value

    @property
    def current_blood_amount(self):
        return self.obj.db.body["current_blood_amount"]

    @current_blood_amount.setter
    def current_blood_amount(self, value):
        self.obj.db.body["current_blood_amount"] = value

    @property
    def max_blood_amount(self):
        species = self.species
        if "blood" not in species:
            return 0
        if "quantity" not in species:
            return 0

        return species["blood"]["quantity"]

    @property
    def temperature(self):
        return self.obj.db.body["temperature"]

    @temperature.setter
    def temperature(self, value):
        self.obj.db.body["temperature"] = value

    @property
    def species(self):
        species_key = self.obj.db.body["species"]
        return next((s for s in SPECIES if s.key == species_key), SPECIES_HUMAN)

    @species.setter
    def species(self, value):
        self.obj.db.body["species"] = value.key

    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

        if not self.obj.db.body:
            raise Exception('`BodyHandler` requires `db.body` attribute on `{}`.'.format(obj))

    # exertion = 0

    @lazy_property
    def limbs(self):
        """LimbHandler manages limbs and appendages connected to this Character."""
        return LimbHandler(self.obj)

    @lazy_property
    def organs(self):
        """OrganHandler manages vital organs inside this Character."""
        return OrganHandler(self.obj)

    def get_resource(self, key):
        existing = 0
        if key in self.resources:
            existing = self.resources[key]
        return existing

    def adjust_resources(self, key, amount):
        # get existing amount..
        existing = self.get_resource(key)

        # calculate the new value
        new_value = max(0, existing + amount)
        new_value = min(self.get_resource_capacity(key), new_value)

        self.resources[key] = new_value

    def get_resource_capacity(self, key):
        capacity = 0

        if "blood" in self.species and "exchange" in self.species["blood"]:
            if key == self.species["blood"]["exchange"]:
                efficiency = self.species["blood"]["exchange_efficiency"]
                capacity += efficiency * (self.current_blood_amount / 10.0)

        for content in self.obj.contents:
            if not hasattr(content, 'resource_storage'):
                continue  # not a body part
            if not hasattr(content, 'used_by'):
                continue  # not implanted
            capacity += self._get_resource_capacity(key, content)

        return capacity

    def _get_resource_capacity(self, key, body_part):
        capacity = 0
        if key in body_part.resource_storage:
            capacity = body_part.resource_storage[key]

        for content in body_part.contents:
            if not hasattr(content, 'resource_storage'):
                continue  # not a body part
            if not hasattr(content, 'used_by'):
                continue  # not implanted
            capacity += self._get_resource_capacity(key, content)

        return capacity

    def is_alive(self):
        nervous_system = self.obj.organs.find_organ(OrganType.NervousSystem)
        if not nervous_system:
            return False
        return nervous_system.conciousness != ConsciousnessState.Dead

    def has_heartbeat(self):
        heart = self.obj.organs.find_organ(OrganType.Heart)
        if not heart:
            return False
        return heart.get_heartrate() > 0

    def get_bpm(self):
        if not self.has_heartbeat():
            return 0
        heart = self.obj.organs.find_organ(OrganType.Heart)
        return heart.get_heartrate()

    def has_blood(self):
        return self.obj.db.body.cur_blood > 0

    def get_brain_activity(self):
        nervous_system = self.obj.organs.find_organ(OrganType.NervousSystem)
        if not nervous_system:
            return 0
        return nervous_system.get_efficiency()

    """ Destroy this current body. """
    def destroy(self):
        for content in self.obj.contents:
            if not (hasattr(content, 'organ_type') or hasattr(content, 'size_capacity')):
                continue  # not an organ or limb
            if not hasattr(content, 'used_by'):
                continue  # not implanted
            content.delete()

        self.obj.db.body = {}
