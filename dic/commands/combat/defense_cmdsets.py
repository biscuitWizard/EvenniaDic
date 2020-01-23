from evennia import CmdSet
from commands.combat.defense import *
from commands.combat.ship_defense import *
from commands.combat.vehicle_defense import *


class GroundMeleeDefenseCmdSet(CmdSet):
    key = "ground_melee_defense_cmdset"
    priority = 0

    def at_cmdset_creation(self):
        """Populate CmdSet"""
        self.add(CmdPass())
        self.add(CmdBlock())
        self.add(CmdDodge())
        self.add(CmdParry())


class GroundRangedDefenseCmdSet(CmdSet):
    key = "ground_ranged_defense_cmdset"
    priority = 0

    def at_cmdset_creation(self):
        """Populate CmdSet"""
        self.add(CmdPass())
        self.add(CmdBlock())
        self.add(CmdDodge())
        self.add(CmdQuickshot())


class VehicleToGroundDefenseCmdSet(CmdSet):
    key = "vehicle_to_ground_defense_cmdset"
    priority = 0

    def at_cmdset_creation(self):
        """Populate CmdSet"""
        self.add(CmdPass())
        self.add(CmdDodge())


class VehicleToVehicleDefenseCmdSet(CmdSet):
    key = "vehicle_to_vehicle_defense_cmdset"
    priority = 0

    def at_cmdset_creation(self):
        """Populate CmdSet"""
        self.add(CmdVehiclePass())
        self.add(CmdVehicleEvade())


class ShipToShipDefenseCmdSet(CmdSet):
    key = "ship_to_ship_defense_cmdset"
    priority = 0

    def at_cmdset_creation(self):
        """Populate CmdSet"""
        self.add(CmdShipPass())
        self.add(CmdShipEvade())
