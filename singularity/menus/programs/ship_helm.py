from world.content.astronomy import *
import math
import re


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
        {"key": "_default", "goto": node_program_helm_parse},
        {"key": "return", "goto": _start},
        {"key": "set", "goto": "22323"},
        {"key": "begin calc", "goto": _begin_calc},
        {"key": "reset", "goto": _reset_nav},
        {"key": "iff", "goto": _toggle_iff}
    ]
    return text, options


def node_program_helm_parse(caller, raw_string):
    set_cmd = re.match(r'set (\w+) to (\w+|\d+)', raw_string)
    if set_cmd:
        arg = set_cmd.group(1).lower()
        if "destination".startswith(arg):
            _set_destination(set_cmd.group(2))
        elif "g-force".startswith(arg):
            _set_g_force(set_cmd.group(2))
        elif "speed".startswith(arg):
            _set_speed(set_cmd.group(2))
        else:
            caller.msg("Invalid argument specified. Valid arguments: |wdestination, g-force, speed.|n")
        return "node_program_helm"


def _set_destination(arg):
    pass


def _set_g_force(arg):
    pass


def _set_speed(arg):
    pass


def _toggle_iff(caller):
    caller.msg("You toggle IFF %s." % "|gON|n")
    return "node_program_helm"


def _reset_nav(caller):
    return "node_program_helm"


def _begin_calc(caller):
    return "node_program_helm"
