from evennia import create_object
from evennia.utils.utils import inherits_from
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
        return self.obj.db.body["organs"]

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
        # check if there are organs already present and eat them if possible.
        for content in self.obj.contents:
            if not inherits_from(content, Organ):
                continue
            if not hasattr(content, 'used_by'):
                continue  # not implanted
            if content.organ_type in self.organs:
                continue  # already existing organ
            self.organs[content.organ_type] = content

        # Add some basic organs!
        for organKey in self.obj.body.species["organs"]:
            organ = next((o for o in ORGANS if o["key"] == organKey), None)
            if not organ:
                continue
            organ_obj = create_object(typeclass=organ["typeclass"],
                                      location=self.obj,
                                      key=organKey)
            organ_obj.used_by = self.obj
            self.organs[organ["type"]] = organ_obj

    def find_organ(self, organ_type):
        if len(self.organs) == 0:
            self.create_starter_organs()
        return self.organs[organ_type]
