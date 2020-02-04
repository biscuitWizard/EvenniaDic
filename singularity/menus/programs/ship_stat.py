from utils.ui import progress_bar


def _start(caller):
    caller.ndb._menutree.terminal.on_begin_use(caller)


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

    h_i = progress_bar(99, 100, width=20) + " 99%"
    text = """
    |wHull Integrity:|n     %s

    |wShip Systems:|n %s

    |xHULL_BRCH      FIRE_WARN      RAD_WARN       SYS_CORR|n    
    """ % (h_i, system_block)

    options = [
        {"key": "return", "goto": _start},
        {"key": "select", "goto": "22222"}
    ]

    return text, options
