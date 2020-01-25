from world.enums import *

"""
Humans
"""
HEART_HUMAN = {
    "key": "a human heart",
    "typeclass": "typeclasses.items.organs.Heart",
    "type": OrganType.Heart
}

LUNGS_HUMAN = {
    "key": "human lungs",
    "typeclass": "typeclasses.items.organs.Lungs",
    "type": OrganType.Lungs
}

BRAIN_HUMAN = {
    "key": "a human brain",
    "typeclass": "typeclasses.items.organs.Brain",
    "type": OrganType.NervousSystem
}

STOMACH_HUMAN = {
    "key": "a human stomach",
    "typeclass": "typeclasses.items.organs.Stomach",
    "type": OrganType.Digestive
}

LIVER_HUMAN = {
    "key": "a human liver",
    "typeclass": "typeclasses.items.organs.Liver",
    "type": OrganType.Filtration
}

"""
Androids
"""
BRAIN_ANDROID = {
    "key": "a positronic brain",
    "type": OrganType.NervousSystem
}

LUNGS_ANDROID = {
    "key": "a mechanical heat-exchanger",
    "type": OrganType.Lungs
}

BATTERY_ANDROID = {
    "key": "an android power-cell",
    "type": OrganType.Heart
}

"""
CERATA
"""
HEART_CERATA = {
    "key": "a ceratan heart",
    "typeclass": "typeclasses.items.organs.Heart",
    "type": OrganType.Heart
}

BRAIN_CERATA = {
    "key": "a ceratan nerve cluster",
    "typeclass": "typeclasses.items.organs.Brain",
    "type": OrganType.NervousSystem
}

LUNGS_CERATA = {
    "key": "a ceratan respiratory tracheae",
    "typeclass": "typeclasses.items.organs.Lungs",
    "type": OrganType.Lungs
}

STOMACH_CERATA = {
    "key": "a ceratan stomach",
    "typeclass": "typeclasses.items.organs.Stomach",
    "type": OrganType.Digestive
}

LIVER_CERATA = {
    "key": "a ceratan enzyme bladder",
    "typeclass": "typeclasses.items.organs.Liver",
    "type": OrganType.Filtration
}

ORGANS = [
    HEART_HUMAN, BRAIN_HUMAN, LIVER_HUMAN, LUNGS_HUMAN, STOMACH_HUMAN,
    BATTERY_ANDROID, BRAIN_ANDROID, LUNGS_ANDROID,
    BRAIN_CERATA, HEART_CERATA, LIVER_CERATA, LUNGS_CERATA, STOMACH_CERATA
]
