def _start(caller):
    caller.ndb._menutree.terminal.on_begin_use(caller)


def node_program_reactor(caller):
    v_i = progress_bar(89, 100, width=20) + " 89%"
    c_p = progress_bar(66, 100, width=20, display="multicolor-inverse") + " ROUGH"
    c_t = progress_bar(78, 100, width=20, display="multicolor-inverse") + " 10.1 MeV"
    c_c = progress_bar(0, 100, width=20) + " 0 kWH"
    b_c = progress_bar(100, 100, width=20) + " 1400 kWH"

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
        {"key": "return", "goto": _start},
        {"key": "ignite", "goto": "22222"},
        {"key": "set", "goto": "2222"},
        {"key": "purge", "goto": "22222"},
        {"key": "cycle", "goto": "22222"},
        {"key": "switch", "goto": "222222"}
    ]

    return text, options
