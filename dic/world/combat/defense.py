from evennia import DefaultScript


class Defense(DefaultScript):
    key = "defense_script"
    interval = 300  # 5 min repeat

    def at_repeat(self):
        "called every self.interval seconds."
        pass


class GroundMeleeDefense(Defense):
    def at_start(self):
        self.obj.cmdset.add("commands.combat.defense_cmdsets.GroundMeleeDefenseCmdSet")

    def at_stop(self):
        self.obj.cmdset.remove("commands.combat.defense_cmdsets.GroundMeleeDefenseCmdSet")


class GroundRangedDefense(Defense):
    def at_start(self):
        self.obj.cmdset.add("commands.combat.defense_cmdsets.GroundRangedDefenseCmdSet")

    def at_stop(self):
        self.obj.cmdset.remove("commands.combat.defense_cmdsets.GroundRangedDefenseCmdSet")


class VehicleToGroundDefense(Defense):
    def at_start(self):
        self.obj.cmdset.add("commands.combat.defense_cmdsets.VehicleToGroundDefenseCmdSet")

    def at_stop(self):
        self.obj.cmdset.remove("commands.combat.defense_cmdsets.VehicleToGroundDefenseCmdSet")


class VehicleToVehicleDefense(Defense):
    def at_start(self):
        self.obj.cmdset.add("commands.combat.defense_cmdsets.VehicleToVehicleDefenseCmdSet")

    def at_stop(self):
        self.obj.cmdset.remove("commands.combat.defense_cmdsets.VehicleToVehicleDefenseCmdSet")


class ShipToShipDefense(Defense):
    def at_start(self):
        self.obj.cmdset.add("commands.combat.defense_cmdsets.ShipToShipDefenseCmdSet")

    def at_stop(self):
        self.obj.cmdset.remove("commands.combat.defense_cmdsets.ShipToShipDefenseCmdSet")
