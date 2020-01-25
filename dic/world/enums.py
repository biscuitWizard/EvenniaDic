from enum import Enum


class DamageTypeEnum(Enum):
    Blunt = 1
    Velocity = 2
    Burn = 3
    Cut = 4

    # Special Damage Types
    Hypoxia = 10


class OrganStateEnum(Enum):
    Active = 1
    Disabled = 2


class ConsciousnessState(Enum):
    Alert = 1,
    Blackout = 2,
    Dead = 3


class OrganType(Enum):
    Heart = 1,
    NervousSystem = 2,
    Lungs = 3,
    Digestive = 4,
    Filtration = 5


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
