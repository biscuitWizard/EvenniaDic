from enum import Enum


class AttributeEnum(Enum):
    Strength = 1
    Perception = 2
    Endurance = 3
    Savvy = 4
    Intelligence = 5
    Reaction = 6
    Luck = 7
    Psi = 8


class SkillEnum(Enum):
    Brawl = 1
    Deceive = 2
    Dodge = 3
    Drive = 4
    ExoticWeapons = 5
    Explosives = 6
    EVA = 24
    Firearms = 7
    FirstAid = 8
    Forensics = 9
    Gunnery = 10
    Hardware = 11
    HeavyWeapons = 12
    Mechanics = 13
    Medicine = 14
    NonLethalWeapons = 15
    Parkour = 16
    Pilot = 17
    Research = 18
    Salvage = 19
    Software = 20
    Stealth = 21
    Surgery = 22
    Tailoring = 23


class StatsHandler(object):
    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

    """ Attributes are 0-100, with 30 being average. """
    def get_attribute(self, attributeEnum):
        return 30

    pass
