import time
from enum import Enum


class WoundTypeEnum(Enum):
    Blunt = 1
    Velocity = 2
    Burn = 3
    Cut = 4
    # Special Damage Types
    Hypoxia = 10


class Wound:
    severity = 0
    created_on = 0
    wound_type = None

    def __init__(self, wound_type, severity):
        self.created_on = time.time()
        self.wound_type = wound_type
        self.severity = severity


class Body:
    blood_oxygen = 9999
    wounds = []
    max_blood = 5000
    cur_blood = 5000
    blood_contents = []
    temperature = 37.2
    exertion = 0
