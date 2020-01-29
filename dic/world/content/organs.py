from world.enums import *

"""
Humans
"""
HEART_HUMAN = {
    "key": "a human heart",
    "typeclass": "typeclasses.items.organs.Heart",
    "organ_type": OrganType.Heart,
    "max_health": 100,
    "heartrate": 75,
    "base_stroke_volume": 70,
    "base_resting_heartrate": 75,
    "critical_heartrate": 200,
    "resource_consumption": [
        {"key": "oxygen", "amount": 4.02}
    ]
}

LUNGS_HUMAN = {
    "key": "human lungs",
    "typeclass": "typeclasses.items.organs.Lungs",
    "organ_type": OrganType.Lungs,
    "max_health": 75,
    "base_exchange_generation": 28,
    "inhale_volume_per_tick": 0.62,  # Volume in litres of breathed in gas
    "exchange_gas_efficiency": 0.05,  # How much of exchange_gas is processed
    "exhale_gas": "co2",  # Key of gas that's exhaled.
    "min_breath_pressure": 50,  # In KPA.
    "resource_generation": [
        {"key": "oxygen", "amount": 28}
    ]
}

BRAIN_HUMAN = {
    "key": "a human brain",
    "typeclass": "typeclasses.items.organs.Brain",
    "organ_type": OrganType.NervousSystem,
    "max_health": 100,
    "resource_consumption": [
        {"key": "oxygen", "amount": 17.5}
    ]
}

STOMACH_HUMAN = {
    "key": "a human stomach",
    "typeclass": "typeclasses.items.organs.Stomach",
    "organ_type": OrganType.Digestive,
    "speed": 0.5,
    "resource_consumption": [
        {"key": "oxygen", "amount": 1.5}
    ]
}

LIVER_HUMAN = {
    "key": "a human liver",
    "typeclass": "typeclasses.items.organs.Liver",
    "organ_type": OrganType.Filtration,
    "resource_consumption": [
        {"key": "oxygen", "amount": 1}
    ]
}

"""
Androids
"""
BRAIN_ANDROID = {
    "key": "a positronic brain",
    "organ_type": OrganType.NervousSystem
}

LUNGS_ANDROID = {
    "key": "a mechanical heat-exchanger",
    "organ_type": OrganType.Lungs
}

BATTERY_ANDROID = {
    "key": "an android power-cell",
    "organ_type": OrganType.Heart
}

"""
CERATA
"""
HEART_CERATA = {
    "key": "a ceratan heart",
    "typeclass": "typeclasses.items.organs.Heart",
    "organ_type": OrganType.Heart
}

BRAIN_CERATA = {
    "key": "a ceratan nerve cluster",
    "typeclass": "typeclasses.items.organs.Brain",
    "organ_type": OrganType.NervousSystem
}

LUNGS_CERATA = {
    "key": "a ceratan respiratory tracheae",
    "typeclass": "typeclasses.items.organs.Lungs",
    "organ_type": OrganType.Lungs
}

STOMACH_CERATA = {
    "key": "a ceratan stomach",
    "typeclass": "typeclasses.items.organs.Stomach",
    "organ_type": OrganType.Digestive
}

LIVER_CERATA = {
    "key": "a ceratan enzyme bladder",
    "typeclass": "typeclasses.items.organs.Liver",
    "organ_type": OrganType.Filtration
}

ORGANS = [
    HEART_HUMAN, BRAIN_HUMAN, LIVER_HUMAN, LUNGS_HUMAN, STOMACH_HUMAN,
    BATTERY_ANDROID, BRAIN_ANDROID, LUNGS_ANDROID,
    BRAIN_CERATA, HEART_CERATA, LIVER_CERATA, LUNGS_CERATA, STOMACH_CERATA
]
