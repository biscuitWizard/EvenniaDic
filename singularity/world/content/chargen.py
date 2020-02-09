from world.enums import *


TERM_UNIVERSITY = {
    "title": "University"
}


TERM_AGENT = {
    "title": "Agent",
    "advancements": [SkillEnum.Firearms, SkillEnum.Drive, SkillEnum.Brawl,
                     AttributeEnum.Reaction, AttributeEnum.Endurance, AttributeEnum.Intelligence],
    "assignments": [
        {
            "title": "Law Enforcement",
            "advancements": [SkillEnum.Forensics, SkillEnum.Stealth, SkillEnum.Brawl, SkillEnum.NonLethalWeapons],
            "ranks": [
                    {"title": "Rookie", "bonus": None},
                    {"title": "Corporal", "bonus": SkillEnum.Stealth},
                    {"title": "Sergeant", "bonus": None},
                    {"title": "Detective", "bonus": None},
                    {"title": "Lieutenant", "bonus": SkillEnum.Forensics},
                    {"title": "Chief", "bonus": SkillEnum.Deceive},
                    {"title": "Commissioner", "bonus": AttributeEnum.Savvy},
            ],
            "description": "You are a detective, or police officer."
        },
        {
            "title": "Intelligence",
            "advancements": [SkillEnum.Forensics, SkillEnum.Deceive, SkillEnum.Stealth, SkillEnum.Software],
            "ranks": [
                {"title": "Rookie", "bonus": None},
                {"title": "Agent", "bonus": SkillEnum.Deceive},
                {"title": "Field Agent", "bonus": SkillEnum.Forensics},
                {"title": "Field Agent II", "bonus": None},
                {"title": "Special Agent", "bonus": SkillEnum.Firearms},
                {"title": "Assistant Director", "bonus": None},
                {"title": "Director", "bonus": None},
            ],
            "description": ""
        },
        {
            "title": "Corporate",
            "advancements": [SkillEnum.Forensics, SkillEnum.Hardware, SkillEnum.Stealth, SkillEnum.Deceive],
            "ranks": [
                {"title": "Rookie", "bonus": None},
                {"title": "Agent", "bonus": SkillEnum.Deceive},
                {"title": "Field Agent", "bonus": SkillEnum.Forensics},
                {"title": "Field Agent II", "bonus": None},
                {"title": "Special Agent", "bonus": SkillEnum.Firearms},
                {"title": "Assistant Director", "bonus": None},
                {"title": "Director", "bonus": None},
            ],
            "description": ""
        }
    ]
}

TERM_CITIZEN = {
    "title": "Citizen",
    "assignments": [
        {
            "title": "Corporate"
        },
        {
            "title": "Worker"
        },
        {
            "title": "Colonist"
        }
    ]
}

TERM_DRIFTER = {
    "title": "Drifter",
    "assignments": [
        {
            "title": "Belter"
        },
        {
            "title": "Wanderer"
        },
        {
            "title": "Scavenger"
        }
    ]
}

TERM_ENTERTAINER = {
    "title": "Entertainer",
    "assignments": [
        {
            "title": "Artist"
        },
        {
            "title": "Journalist"
        },
        {
            "title": "Performer"
        }
    ]
}

TERM_MERCHANT = {
    "title": "Merchant",
    "assignments": [
        {
            "title": "Merchant Marine"
        },
        {
            "title": "Free Trader"
        },
        {
            "title": "Broker"
        }
    ]
}

TERM_CRIMINAL = {
    "title": "Criminal",
    "assignments": [
        {
            "title": "Thief"
        },
        {
            "title": "Enforcer"
        },
        {
            "title": "Pirate"
        }
    ]
}

TERM_ELITE = {
    "title": "Elite",
    "assignments": [
        {
            "title": "Administrator"
        },
        {
            "title": "Diplomat"
        },
        {
            "title": "Dilettante"
        }
    ]
}

TERM_SCIENTIST = {
    "title": "STEM",
    "assignments": [
        {
            "title": "Mechanic"
        },
        {
            "title": "Scientist"
        },
        {
            "title": "Physician"
        }
    ]
}

TERMS = [
    TERM_AGENT,
    TERM_CITIZEN,
    TERM_CRIMINAL,
    TERM_DRIFTER,
    TERM_ELITE,
    TERM_ENTERTAINER,
    TERM_MERCHANT,
    TERM_SCIENTIST
]


ORIGIN_NOBLE = {
    "title": "Noble",
    "description": "",
    "species_restrictions": ["human"]
}


ORIGIN_EPSILON_CHILD = {
    "title": "Epsilon Child",
    "description": "",
    "species_restrictions": ["human"]
}


ORIGIN_MILITARY_BRAT = {
    "title": "Military Brat",
    "description": "",
    "species_restrictions": ["human"]
}


ORIGIN_BEAT_WITH_UGLY_STICK = {
    "title": "Beat with an Ugly-Stick",
    "description": "",
    "species_restrictions": ["human"]
}


ORIGIN_BOOKWORM = {
    "title": "Bookworm",
    "description": "",
    "species_restrictions": ["human"]
}


ORIGIN_FERAL_CHILD = {
    "title": "Feral Child",
    "description": "",
    "species_restrictions": ["human"]
}


ORIGIN_BELTER = {
    "title": "Belter",
    "description": "",
    "species_restrictions": ["human", "android"]
}


ORIGIN_SICKLY = {
    "title": "Sickly",
    "description": "",
    "species_restrictions": ["human"]
}


ORIGIN_SAVANT = {
    "title": "Savant",
    "description": "",
    "species_restrictions": ["human"]
}


ORIGIN_DRIFTER = {
    "title": "Drifter",
    "description": "",
    "species_restrictions": ["human", "android"]
}


ORIGIN_THUG = {
    "title": "Thug",
    "description": "",
    "species_restrictions": ["human", "android"]
}


ORIGIN_INHERITANCE = {
    "title": "Inheritance",
    "description": "",
    "species_restrictions": ["human"]
}


ORIGIN_NEW_MODEL = {
    "title": "New Model",
    "description": "",
    "species_restrictions": ["android"]
}


ORIGIN_PROTOTYPE = {
    "title": "Prototype",
    "description": "",
    "species_restrictions": ["android"]
}


ORIGIN_FACTORY_MODEL = {
    "title": "Factory Model",
    "description": "",
    "species_restrictions": ["android"]
}


ORIGIN_EVE = {
    "title": "Eve",
    "description": "",
    "species_restrictions": ["android"]
}


ORIGINS = [
    ORIGIN_BEAT_WITH_UGLY_STICK,
    ORIGIN_BELTER,
    ORIGIN_BOOKWORM,
    ORIGIN_DRIFTER,
    ORIGIN_EPSILON_CHILD,
    ORIGIN_FERAL_CHILD,
    ORIGIN_INHERITANCE,
    ORIGIN_MILITARY_BRAT,
    ORIGIN_NOBLE,
    ORIGIN_SAVANT,
    ORIGIN_SICKLY,
    ORIGIN_THUG,

    ORIGIN_PROTOTYPE,
    ORIGIN_FACTORY_MODEL,
    ORIGIN_NEW_MODEL,
    ORIGIN_EVE
]


CHARGEN = {
    "species": [
        {
            "key": "human",
            "min_start_age": 16,
            "max_start_age": 20,
            "min_age": 18,
            "max_terms": 13
        },
        {
            "key": "android",
            "min_start_age": 1,
            "max_start_age": 5,
            "min_age": 3,
            "max_terms": 4
        }
    ],
    "terms": TERMS,
    "origins": ORIGINS
}