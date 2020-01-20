from world.stats import AttributeEnum, SkillEnum


TERM_AGENT = {
    "title": "Agent",
    "assignments": [
        {
            "title": "Law Enforcement",
            "skills": [SkillEnum.Forensics, SkillEnum.Stealth, SkillEnum.Brawl, SkillEnum.NonLethalWeapons],
            "ranks": [
                    {"title": "Rookie", "bonus": None},
                    {"title": "Corporal", "bonus": SkillEnum.Stealth},
                    {"title": "Sergeant", "bonus": None},
                    {"title": "Detective", "bonus": None},
                    {"title": "Lieutenant", "bonus": SkillEnum.Forensics},
                    {"title": "Chief", "bonus": SkillEnum.Deceive},
                    {"title": "Commissioner", "bonus": AttributeEnum.Savvy},
            ]
        },
        {
            "title": "Intelligence",
            "skills": [SkillEnum.Forensics, SkillEnum.Deceive, SkillEnum.Stealth, SkillEnum.Software],
            "ranks": [
                {"title": "Rookie", "bonus": None},
                {"title": "Agent", "bonus": SkillEnum.Deceive},
                {"title": "Field Agent", "bonus": SkillEnum.Forensics},
                {"title": "Field Agent II", "bonus": None},
                {"title": "Special Agent", "bonus": SkillEnum.Firearms},
                {"title": "Assistant Director", "bonus": None},
                {"title": "Director", "bonus": None},
            ]
        },
        {
            "title": "Corporate",
            "skills": [SkillEnum.Forensics, SkillEnum.Hardware, SkillEnum.Stealth, SkillEnum.Deceive],
            "ranks": [
                {"title": "Rookie", "bonus": None},
                {"title": "Agent", "bonus": SkillEnum.Deceive},
                {"title": "Field Agent", "bonus": SkillEnum.Forensics},
                {"title": "Field Agent II", "bonus": None},
                {"title": "Special Agent", "bonus": SkillEnum.Firearms},
                {"title": "Assistant Director", "bonus": None},
                {"title": "Director", "bonus": None},
            ]
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