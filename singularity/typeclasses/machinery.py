from typeclasses.objects import Object
from utils.terminal_menu import TerminalEvMenu
from menus import generic_terminal


class Machinery(Object):
    """
    Whether or not the item can be uninstalled from its room or stolen.

    If is_bolted is True, nothing can move this item except staff.
    """

    @property
    def is_bolted(self):
        return self.db.is_bolted

    @is_bolted.setter
    def is_bolted(self, value):
        self.db.is_bolted = value

    def at_object_creation(self):
        super(Machinery, self).at_object_creation()
        self.is_bolted = False

    def on_begin_use(self, character):
        pass

    def on_end_use(self, character):
        pass

    def has_part(self, part_type):
        pass

    def get_parts(self, part_type):
        pass


class Terminal(Machinery):
    @property
    def used_by(self):
        return self.db.used_by

    @used_by.setter
    def used_by(self, value):
        self.db.used_by = value

    @property
    def menu_type(self):
        return self.db.menu_type

    @menu_type.setter
    def menu_type(self, value):
        self.db.menu_type = value

    def at_object_creation(self):
        super(Terminal, self).at_object_creation()

        self.used_by = None
        self.menu_type = ''

    def on_begin_use(self, character):
        self.used_by = character
        TerminalEvMenu(self.used_by, self.menu_type, terminal=self)


class GenericTerminal(Terminal):
    @property
    def programs(self):
        return self.db.programs

    @programs.setter
    def programs(self, value):
        self.db.programs = value

    @property
    def files(self):
        return self.db.files

    @files.setter
    def files(self, value):
        self.db.files = value

    def at_object_creation(self):
        super(GenericTerminal, self).at_object_creation()
        self.files = [
            {"key": "sample_data.nff", "size": 30, "desc": "sample data example"}
        ]
        self.programs = [
            {"key": "notes", "node": "node_program_notes", "data": "menus.programs.notes"},
            {"key": "network", "node": "node_program_network", "data": "menus.programs.network"},
            {"key": "mail", "node": "node_program_mail", "data": "menus.programs.mail"},
            {"key": "load disk", "node": "node_program_load_disk", "data": "menus.programs.load_disk"},
            {"key": "terminal", "node": "node_program_terminal", "data": "menus.programs.terminal"},
            {"key": "helm", "node": "node_program_helm", "data": "menus.programs.ship_helm"},
            {"key": "reactor", "node": "node_program_reactor", "data": "menus.programs.ship_reactor"},
            {"key": "sensors", "node": "node_program_sensors", "data": "menus.programs.ship_sensors"},
            {"key": "ship_stat", "node": "node_program_ship", "data": "menus.programs.ship_stat"}
        ]
        self.menu_type = generic_terminal

    def launch_program(self, program):
        TerminalEvMenu(self.used_by, program["data"],
                       startnode=program["node"],
                       terminal=self)
