from world.content.astronomy import *
import math


def _start(caller):
    caller.ndb._menutree.terminal.on_begin_use(caller)


def node_program_helm(caller):
    destination = PLANET_2
    current = PLANET_1
    x = math.pow(destination["x"] - current["x"], 2)
    y = math.pow(destination["y"] - current["y"], 2)
    raw_distance = round(math.sqrt(abs(x + y)), 4)
    distance = "%s AU (%s mKM)" % (raw_distance, round(raw_distance / 0.0066, 1))

    text = """
    |wShip Status:|n        In Orbit
    |wLocation:|n           Atreus L2 Point
    |wNearest Body:|n       Atreus
    |wDistance:|n           130,457km

    |wDestination:|n        %s
    |wTravel Est:|n         %s
    |wMax G-Force:|n        1g
    |wMax Speed:|n          3400 / 3400 km/s
    |wFuel Est:|n           N/A
    |wRoute Calculated:|n   |rNO|n

    |wIFF:|n                |yWCFS-FOX|n
    |wThrusters:|n          |gONLINE|n
    |wEngine:|n             |gONLINE|n
    |wFuel Level:|n         1333.33 Litres
    """ % (destination["name"], distance)

    options = [
        {"key": "_default", "goto": "node_program_helm_parse"},
        {"key": "return", "goto": _start},
        {"key": "set", "goto": "22323"},
        {"key": "begin calc", "goto": "232323"},
        {"key": "reset", "goto": "23232"},
        {"key": "iff", "goto": "23232"}
    ]
    return text, options


def node_program_helm_parse(caller, raw_string):
    pass