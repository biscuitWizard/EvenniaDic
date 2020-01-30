import random
from world.enums import *


SKILL_MAP = [
    {
        "skill": SkillEnum.Brawl,
        "attributes": [
            {"key": AttributeEnum.Strength, "ratio": 0.2},
            {"key": AttributeEnum.Reaction, "ratio": 0.4},
            {"key": AttributeEnum.Perception, "ratio": 0.2}
        ]
    },
    {
        "skill": SkillEnum.Dodge,
        "attributes": [
            {"key": AttributeEnum.Perception, "ratio": 0.5},
            {"key": AttributeEnum.Reaction, "ratio": 0.5}
        ]
    }
]


def prob(chance):
    return random.randint(1, 100) <= chance


def stat_test(character, stat_enum, modifiers=None):
    roll = random.randint(1, 100)
    if roll <= 5:
        return False
    if roll >= 95:
        return True

    if isinstance(stat_enum, AttributeEnum):
        return roll <= character.stats.get_attribute(stat_enum) + modifiers
    elif isinstance(stat_enum, SkillEnum):
        # Skill check!
        attribute_value = 0
        skill_map = next(m for m in SKILL_MAP if m["skill"] == stat_enum)
        for attribute_map in skill_map["attributes"]:
            ratio = 2.0 * attribute_map["ratio"]
            attribute_value += character.stats.get_attribute(attribute_map["key"] * ratio)
        skill_value = character.stats.get_skill(stat_enum) / 2.0

        difficulty = ((attribute_value + skill_value) / 2.5) + modifiers
        return roll <= difficulty
    return False
