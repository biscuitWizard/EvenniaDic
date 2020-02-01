from evennia.commands.cmdset import CmdSet
from evennia.commands.default import general, help, admin, system
from evennia.commands.default import building
from evennia.commands.default import batchprocess
from world.memory import MemoriesCmd, MemorizeCmd
from typeclasses.exits import FlightExit

from django.conf import settings
from evennia.utils import utils
from evennia.utils.utils import inherits_from

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)


class CharacterGameCmdSet(CmdSet):
    """
       Implements the default command set.
       """

    key = "Character"
    priority = 0

    def at_cmdset_creation(self):
        "Populates the cmdset"

        # The general commands
        self.add(general.CmdLook())
        # self.add(general.CmdHome())
        # self.add(general.CmdInventory())
        self.add(CmdGameInventory())
        self.add(general.CmdPose())
        # self.add(general.CmdNick())
        # self.add(general.CmdSetDesc())
        self.add(general.CmdGet())
        self.add(general.CmdDrop())
        self.add(general.CmdGive())
        self.add(general.CmdSay())
        # self.add(general.CmdWhisper())
        self.add(general.CmdAccess())

        # The help system
        self.add(help.CmdHelp())
        self.add(help.CmdSetHelp())

        # System commands
        self.add(system.CmdPy())
        self.add(system.CmdScripts())
        self.add(system.CmdObjects())
        self.add(system.CmdAccounts())
        self.add(system.CmdService())
        self.add(system.CmdAbout())
        self.add(system.CmdTime())
        self.add(system.CmdServerLoad())
        # self.add(system.CmdPs())
        self.add(system.CmdTickers())

        # Admin commands
        self.add(admin.CmdBoot())
        self.add(admin.CmdBan())
        self.add(admin.CmdUnban())
        self.add(admin.CmdEmit())
        self.add(admin.CmdPerm())
        self.add(admin.CmdWall())
        self.add(admin.CmdForce())

        # Building and world manipulation
        self.add(building.CmdTeleport())
        self.add(building.CmdSetObjAlias())
        self.add(building.CmdListCmdSets())
        self.add(building.CmdWipe())
        self.add(building.CmdSetAttribute())
        self.add(building.CmdName())
        self.add(building.CmdDesc())
        self.add(building.CmdCpAttr())
        self.add(building.CmdMvAttr())
        self.add(building.CmdCopy())
        self.add(building.CmdFind())
        self.add(building.CmdOpen())
        self.add(building.CmdLink())
        self.add(building.CmdUnLink())
        self.add(building.CmdCreate())
        self.add(building.CmdDig())
        self.add(building.CmdTunnel())
        self.add(building.CmdDestroy())
        self.add(building.CmdExamine())
        self.add(building.CmdTypeclass())
        self.add(building.CmdLock())
        self.add(building.CmdScript())
        self.add(building.CmdSetHome())
        self.add(building.CmdTag())
        self.add(building.CmdSpawn())

        # Batchprocessor commands
        self.add(batchprocess.CmdBatchCommands())
        self.add(batchprocess.CmdBatchCode())

        # Debug Commands
        self.add(CmdAtmoCheck())
        self.add(CmdEMScan())
        self.add(CmdStats())
        self.add(CmdUse())

        # memories commands
        self.add(MemoriesCmd())
        self.add(MemorizeCmd())
        self.add(CmdFly())


class CmdFly(COMMAND_DEFAULT_CLASS):
    key = "fly"

    def func(self):
        ship = self.caller.location.ship_parent
        target = ship.search(self.args)
        if not inherits_from(target, FlightExit):
            self.caller.msg("That is not a valid direction to fly.")
        ship.move_to(target.destination)
        self.caller.msg("|cFrom outside the view-screen you see:|n %s" % target.destination.return_appearance(ship))


class CmdEMScan(COMMAND_DEFAULT_CLASS):
    key = "scan em"

    def func(self):
        frequencies = ["10hz", "100hz", "200hz", "400hz", "800hz", "1200hz", "1600hz", "2000hz"]
        values = [10, 35, 20, 1, 44, 55, 66, 22]
        # rows = 16
        # current_row = rows
        text = ""

        for frequency in frequencies:
            index = frequencies.index(frequency)
            value = values[index]
            text += "[%s] " % frequency
            text += "%sdbW\r\n" % value

        # while current_row > 0:
        #     text += "      |"
        #     for frequency in frequencies:
        #         index = frequencies.index(frequency)
        #         value = values[index]
        #         row_value = (value / 100) * rows
        #         if row_value >= current_row:
        #             text += ".."
        #         else:
        #             text += "  "
        #     text += "\r\n"
        #     current_row -= 1
        #
        # text += "      |------------------------\r\n"
        #
        # rows = 6
        # current_row = rows
        # index = 0
        # while current_row > 0:
        #     text += "       "
        #     for frequency in frequencies:
        #         if index + 1 > len(frequency):
        #             text += "  "
        #             continue
        #         text += "%s " % frequency[index]
        #
        #     text += "\r\n"
        #     index += 1
        #     current_row -= 1
        self.caller.msg(text)


class CmdAtmoCheck(COMMAND_DEFAULT_CLASS):
    key = "scan atmo"
    locks = "cmd:all()"

    def func(self):
        room = self.caller.location
        total_moles = room.total_moles

        text = "======= Atmospheric Composition ======="
        text += "\r\nTemperature: %sK" % room.temperature
        text += "\r\nVolume: %s litres" % room.volume_litres
        text += "\r\nMax Occupancy: %s people" % room.size
        text += "\r\nPressure: %skPA" % room.pressure
        text += "\r\nGasses:"
        for atmo_gas in room.atmosphere:
            gas_percent = round(atmo_gas["moles"] * 100 / total_moles, 2)
            text += "\r\n\t[%s] " % atmo_gas["key"].upper() + " %s%%" % gas_percent
        self.caller.msg(text)


class CmdGameInventory(COMMAND_DEFAULT_CLASS):
    """
    view inventory
    Usage:
      inventory
      inv
    Shows your inventory.
    """

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        items = []
        for item in self.caller.contents:
            if hasattr(item, 'is_hidden') and item.is_hidden:
                continue
            items.append(item)

        if not items:
            string = "You are not carrying anything."
        else:
            table = self.styled_table(border="header")
            for item in items:
                table.add_row("|C%s|n" % item.name, item.db.desc or "")
            string = "|wYou are carrying:\n%s" % table
        self.caller.msg(string)


from forms import stats
class CmdStats(COMMAND_DEFAULT_CLASS):
    key = "+stats"

    def func(self):
        self.caller.msg(stats.show(self.caller))


class CmdUse(COMMAND_DEFAULT_CLASS):
    key = "use"

    def func(self):
        target = self.caller.search(self.args)
        if not target:
            # we didn't find anyone, but search has already let the
            # caller know. We'll just return, since we're done
            return

        target.used_by = self.caller
        self.caller.using = target

        self.caller.msg("You begin operating %s." % target.name)

        target.on_begin_use(self.caller)
