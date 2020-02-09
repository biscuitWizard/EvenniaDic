from evennia import DefaultObject, default_cmds, CmdSet
from evennia.utils.evmenu import EvMenu
from menus import chargen
from utils.evmenu import MyEvMenu


class ChargenCmdSet(CmdSet):
    key = "chargen_cmdset"
    priority = 0

    def at_cmdset_creation(self):
        """Populate CmdSet"""
        self.add(BeginChargen())


class BeginChargen(default_cmds.MuxCommand):
    key = "chargen"

    def func(self):
        MyEvMenu(self.caller, chargen, startnode="start")
