from evennia.utils.utils import list_to_string


def _start(caller):
    caller.ndb._menutree.terminal.on_begin_use(caller)


def node_program_sensors(caller):
    contacts = ["|y?-A02|n", "|y?-D22|n", "|y?-JJ3|n", "|gWCFS-CAT|n", "|gHMF-SCAD|n", "|rHMS-SCUF|n", "|r?-EEF|n",
                "|y?-443|n"]
    target = "?-A02"
    text = """
    |wContacts:|n %s

    |wTarget:|n         %s
    |wName:|n           Unknown
    |wClass:|n          Unknown
    |wTonnage:|n        Unknown
    |wDistance:|n       14,432 mKm
    |wTemperature:|n    455K






    |yIFF     |n     |xREAC         THRUST         |gDRIVE   |n|n
    |xWEAPONS     TARGET       INTRCEPT      LIFE_SIGN|n 
    """ % (list_to_string(contacts), target)

    options = [
        {"key": "return", "goto": _start},
        {"key": "select", "goto": "22222"}
    ]

    return text, options
