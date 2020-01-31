from utils.ui import progress_bar
from evennia.utils.utils import list_to_string


def start(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "files", "goto": "node_program_files"},
    ]

    for program in caller.using.programs:
        options.append({
            "key": program["key"],
            "goto": program["node"]
        })

    # options.append({"key": "exit", "goto": "exit"})

    return text, options


def node_program_notes(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"},
        {"key": "new", "goto": "node_program_notes_new"},
        {"key": "del", "goto": "node_program_notes_del"},
        {"key": "read", "goto": "node_program_notes_view"}
    ]

    return text, options


def node_program_files(caller):
    text = ""
    files = caller.using.files
    index = 0
    while index < len(files):
        file1 = files[index]
        file_index = "|w%s|n" % str(index + 1).rjust(2, '0')
        file_name = file1["key"].ljust(36)
        file_size = str(file1["size"]).rjust(5)
        text += "%s. %s [%su]\n" % (file_index, file_name, file_size)
        index += 1

    text += "\n\n"
    text += progress_bar(10, 100, width=30, display="multicolor-inverse")
    text += " 90% free space"

    options = [
        {"key": "back", "goto": "start"},
        {"key": "delete", "goto": "node_program_files_delete"},
        {"key": "run", "goto": "node_program_files_run"},
        {"key": "cd", "goto": "node_program_files_cd"},
        {"key": "next page", "goto": "node_program_files_next"},
        {"key": "prev page", "goto": "node_program_files_prev"},
        {"key": "cat", "goto": "node_program_files_cat"}
    ]

    return text, options


def node_program_network(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"},
        {"key": "disconnect", "goto": "node_program_network_disconnect"},
        {"key": "connect", "goto": "node_program_network_connect"},
        {"key": "set tag", "goto": "node_program_network_set_tag"}
    ]

    return text, options


def node_program_load_disk(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"}
    ]

    return text, options


def node_program_mail(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"},
        {"key": "new", "goto": "node_program_mail_new"},
        {"key": "del", "goto": "node_program_mail_del"},
        {"key": "read", "goto": "node_program_mail_view"}
    ]

    return text, options


def node_program_terminal(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"}
    ]

    return text, options

def node_program_helm(caller):
    text = """
    |wShip Status:|n        In Orbit
    |wLocation:|n           Atreus L2 Point
    |wNearest Body:|n       Atreus
    |wDistance:|n           130,457km
    
    |wDestination:|n        None Set
    |wTravel Est:|n         N/A
    |wMax G-Force:|n        1g
    |wFuel Est:|n           N/A
    |wRoute Calculated:|n   |rNO|n
    
    |wIFF:|n                |yWCFS-FOX|n
    |wThrusters:|n          |gONLINE|n
    |wEngine:|n             |gONLINE|n
    |wFuel Level:|n         1333.33 Litres
    """

    options = [
        {"key": "back", "goto": "start"},
        {"key": "set", "goto": "22323"},
        {"key": "begin calc", "goto": "232323"},
        {"key": "reset", "goto": "23232"},
        {"key": "iff", "goto": "23232"}
    ]
    return text, options

def node_program_reactor(caller):
    v_i = progress_bar(89,100,width=20)  + " 89%"
    c_p = progress_bar(66,100,width=20,display="multicolor-inverse")  + " ROUGH"
    c_t = progress_bar(78,100,width=20,display="multicolor-inverse")  + " 10.1 MeV"
    c_c = progress_bar(0,100,width=20)   + " 0 kWH"
    b_c = progress_bar(100,100,width=20) + " 1400 kWH"

    text = """
    |wReactor:|n            RKTR-FXY-2
    |wReactor Status:|n     |gONLINE|n
    
    |wVessel Integrity:|n   %s
    |wCore Pressure:|n      %s
    |wCore Temperature:|n   %s
    |wLas. Cap Charge:|n    %s
    
    |wBatteries:|n          %s
    
    |wFuel Total:|n         1747.73 kg He3
    |wFuel/Day:|n           24.30 kg He3
    |wPellets Total:|n      16854
    |wPellets/Day:|n        55.5
    
      |yABL_WALL|n     |xX_RAY        LAS_RDY       |gPEL_FEED|n|n
      |xCOR_PRGE     LOW_FUEL     LOW_TEMP      HIGH_TEMP|n 
    """ % (v_i, c_p, c_t, c_c, b_c)

    options = [
        {"key": "back", "goto": "start"},
        {"key": "ignite", "goto": "22222"},
        {"key": "set", "goto": "2222"},
        {"key": "purge", "goto": "22222"},
        {"key": "cycle", "goto": "22222"},
        {"key": "switch", "goto": "222222"}
    ]

    return text, options

def node_program_life_supprt(caller):
    pass

def node_program_sensors(caller):
    contacts = ["|y?-A02|n","|y?-D22|n","|y?-JJ3|n","|gWCFS-CAT|n","|gHMF-SCAD|n","|rHMS-SCUF|n","|r?-EEF|n","|y?-443|n"]
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
        {"key": "back", "goto": "start"},
        {"key": "select", "goto": "22222"}
    ]

    return text, options

def node_program_ship(caller):
    systems = [
        {"key": "RKTR_FXY_1", "integrity": 1.00},
        {"key": "RKTR_FXY_2", "integrity": 0.89},
        {"key": "SENS_MXR", "integrity": 1.00},
        {"key": "LFS_RBRD", "integrity": 1.00},
        {"key": "WPN_LASR_1", "integrity": 1.00},
        {"key": "WPN_LASR_2", "integrity": 1.00},
        {"key": "THRST_FBR", "integrity": 1.00},
        {"key": "DRVE_FBX", "integrity": 1.00},
        {"key": "COMM_FFFD", "integrity": 0.22},
        {"key": "WPN_TPDX_1", "integrity": 0.47},
        {"key": "WPN_TPDX_2", "integrity": 0.88},
        {"key": "WPN_TPDX_3", "integrity": 0.01},
        {"key": "WPN_TPDX_4", "integrity": 0.90}
    ]

    system_block = ""
    index = 0
    for system in systems:
        if index % 2 == 0:
            system_block += "\n"
        if system["integrity"] >= 0.99:
            integrity = "|cPRIST|n"
        elif system["integrity"] >= .8:
            integrity = "|gGOOD|n"
        elif system["integrity"] >= .5:
            integrity = "|yWARN|n"
        elif system["integrity"] >= .3:
            integrity = "|rCRIT|n"
        else:
            integrity = "|rFAULT|n"
        system_block += system["key"].ljust(18, ' ')
        system_block += integrity.rjust(7, ' ')
        if index % 2 == 0:
            system_block += "  "
        index += 1

    h_i = progress_bar(99,100,width=20)  + " 99%"
    text = """
    |wHull Integrity:|n     %s
    
    |wShip Systems:|n %s
    
    |xHULL_BRCH      FIRE_WARN      RAD_WARN       SYS_CORR|n    
    """ % (h_i, system_block)

    options = [
        {"key": "back", "goto": "start"},
        {"key": "select", "goto": "22222"}
    ]

    return text, options