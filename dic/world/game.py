import random
from world.enums import *


def prob(chance):
    return random.randint(1, 100) <= chance


def stat_test(character, stat_enum, modifiers=None):
    if isinstance(stat_enum, AttributeEnum):
        return random.randint(1, 100) <= 30 + modifiers
    elif isinstance(stat_enum, SkillEnum):
        return random.randint(1, 100) <= 30 + modifiers
    return False
