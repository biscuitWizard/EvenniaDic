from evennia import create_object
from evennia.utils.utils import inherits_from
from evennia.prototypes.spawner import spawn
from typeclasses.items.organs import Organ
from world.enums import *
from world.content.organs import ORGANS


class OrganException(Exception):
    """Base exception class for OrganHandler."""

    def __init__(self, msg):
        self.msg = msg


class OrganHandler(object):
    @property
    def organs(self):
        return self.obj.db.body.get("organs", None)

    @organs.setter
    def organs(self, value):
        self.obj.db.body["organs"] = value

    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

        if "organs" not in self.obj.db.body:
            self.organs = dict()

        if len(self.organs) == 0:
            self.create_starter_organs()

    def create_starter_organs(self):
        if "organs" not in self.obj.db.body:
            self.organs = dict()

        # check if there are organs already present and eat them if possible.
        for content in self.obj.contents:
            if not inherits_from(content, Organ):
                continue
            if content.used_by is None:
                continue  # not implanted
            if content.organ_type in self.organs:
                continue  # already existing organ
            self.organs[content.organ_type] = content

        # Add some basic organs!
        for organ_key in self.obj.body.species["organs"]:
            organ = next((o for o in ORGANS if o["key"] == organ_key), None)
            if not organ:
                continue
            if organ["organ_type"] in self.organs:
                continue  # We already have an organ of this type.

            organ["location"] = self.obj
            organ["used_by"] = self.obj
            organ_obj = spawn(organ)[0]

            self.organs[organ_obj.organ_type] = organ_obj

    def find_organ(self, organ_type):
        if len(self.organs) == 0:
            self.create_starter_organs()
        return self.organs[organ_type]
