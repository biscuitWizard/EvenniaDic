from world.stats import AttributeEnum
from evennia import create_object
from enum import Enum


class OrganType(Enum):
    Heart = 1,
    NervousSystem = 2,
    Lungs = 3,
    Digestive = 4,
    Filtration = 5


class OrganException(Exception):
    """Base exception class for OrganHandler."""
    def __init__(self, msg):
        self.msg = msg


class OrganHandler(object):
    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

        #  if not self.obj.db.organ_slots:
        #      raise OrganException('`OrganHandler` requires `db.organ_slots` attribute on `{}`.'.format(obj))

        if len(obj.db.organ_slots) == 0:
            self.create_starter_organs()
        self.organs = obj.db.organ_slots

    def create_starter_organs(self):
        # check if there are organs already present and eat them if possible.
        for content in self.obj.contents:
            if not content.organ_type:
                continue  # not an organ
            if not content.used_by:
                continue  # not implanted
            if self.obj.db.organ_slots[content.organ_type]:
                continue  # already existing organ
            self.obj.db.organ_slots[content.organ_type] = content

        # Add some basic organs!
        # Heart? Check.
        if not self.obj.db.organ_slots[OrganType.Heart]:
            heart = create_object(typeclass='typeclasses.items.organs.Heart',
                                  location=self.obj,
                                  key='Heart')
            heart.db.used_by = self.obj
            self.obj.db.organ_slots[OrganType.Heart] = heart
        # Lungs? Check.
        if not self.obj.db.organ_slots[OrganType.Lungs]:
            lungs = create_object(typeclass='typeclasses.items.organs.Lungs',
                                  location=self.obj,
                                  key='Lungs')
            lungs.db.used_by = self.obj
            self.obj.db.organ_slots[OrganType.Lungs] = lungs
        # Brain? Check.
        if not self.obj.db.organ_slots[OrganType.NervousSystem]:
            brain = create_object(typeclass='typeclasses.items.organs.Brain',
                                  location=self.obj,
                                  key='Brain')
            brain.db.used_by = self.obj
            self.obj.db.organ_slots[OrganType.NervousSystem] = brain
        # Liver? Check.
        if not self.obj.db.organ_slots[OrganType.Filtration]:
            liver = create_object(typeclass='typeclasses.items.organs.Liver',
                                  location=self.obj,
                                  key='Liver')
            liver.db.used_by = self.obj
            self.obj.db.organ_slots[OrganType.Filtration] = liver

        self.organs = self.obj.db.organ_slots

    def find_organ(self, organ_type):
        if len(self.obj.db.organ_slots) == 0:
            self.create_starter_organs()
        return self.organs[organ_type]
