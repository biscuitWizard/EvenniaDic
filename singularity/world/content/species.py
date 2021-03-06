
SPECIES_HUMAN = {
    "key": "human",
    "title": "Human",
    "is_machine": False,
    "taxonomy": "Homo sapiens",
    "blood": {
        "type": "human blood",
        "subtypes": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        "color": "red",
        "quantity": 5000,
        "transport": "oxygenation",
        "exchange": "oxygen",
        "exchange_efficiency": 20.1,
        "starting_resources": [
            {"key": "oxygen", "amount": 10000}
        ]
    },
    "armor": [],  # Any natural armors
    "hypothermic": 34.7,  # Temperature in C before suffering hypothermia.
    "hyperthermic": 40,  # Temperature in C before suffering hyperthermia.
    "body_size": 36,  # This is the percentile out of a hundred to hit the body relative to limbs.
    "organs": ["a human heart", "human lungs", "a human stomach", "a human liver"],
    "limbs": ["a human arm", "a human arm", "a human leg", "a human leg", "a human head"]
}

SPECIES_ANDROID = {
    "key": "android",
    "title": "Android",
    "is_machine": True,
    "taxonomy": "Silica sapiens",
    "body_size": 36,  # This is the percentile out of a hundred the body is
    "organs": ["a positronic brain", "a mechanical heat-exchanger", "an android power-cell"]
}

SPECIES_CERATA = {
    "key": "cerata",
    "title": "Ceratan",
    "is_machine": False,
    "taxonomy": "Ceratarctos scyphephalus",
    "blood_quantity": 7000,
    "summary": """
        The cerata use siloxane backbones (alternating silicon-oxygen chains), as siloxanes can form a wide variety of 
        polymers. They respire fluorine gas. As such, the cerata are prone 
        to exploding on contact with an Earth-like atmosphere.
        
        Features four stalk-like digitigrade legs ending in three opposed silica-based talons each, and two arms
        ending in hands with segmented palms, three fingers, and two thumb-like appendages. They are capable of 
        communicating with nearby cerata using high-bandwidth gamma-ray wavelength color-pulse signaling.
        
        Their ships commonly do not use any cooling at all, and most cerata find peak comfort at about 150C.
        At about 50C, cerata enter a type of hibernation state where after a few hours they will die
        from hypothermia.
        
        Ceratans can molt to a needed gender. Nymphs hatch from eggs are determinedly
        male or sexless from a gyne. Nymphs are basic workers and often not very independent or far from a gyne.
        Eventually a nymph can molt to either an alate (a male with wings), or a gyne (reproductive female).
        
        It is not unheard of to see an alate alone, but gynes will always have a swarm of alates, or nymphs nearby.
        Gynes do not operate in similar territories, being very proud and very territorial. There will almost never
        be more than one gyne on a ceratan ship. This reproductive strategy has made ceratan prolific in space.
        
        Ceratans are on par technologically with humans despite having achieved space-flight earlier. All cerata
        seen off world or on human stations will be wearing an exo-suit that keeps them warm and not-exploded.
        
        Ceratan fluids and organs are highly organofluoridic.
        
        Atmosphere:
        22% Helium
        62% Argon
        16% Fluorine
    """,
    "organs": ["a ceratan heart", "a ceratan nerve cluster", "a ceratan respiratory tracheae",
               "a ceratan stomach", "a ceratan enzyme bladder"]
}

SPECIES = [SPECIES_HUMAN, SPECIES_ANDROID, SPECIES_CERATA]

