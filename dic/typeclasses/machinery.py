from typeclasses.objects import Object
from evennia.utils.evmenu import EvMenu


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
        EvMenu(character, self.menu_type,
               startnode="start",
               cmdset_mergetype="Replace", cmdset_priority=1,
               auto_quit=True, auto_look=True, auto_help=True,
               cmd_on_exit="look",
               persistent=False,
               startnode_input="",
               session=None,
               debug=False,
               terminal=self)


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
        self.files = []
        self.programs = [
            {"key": "notes", "node": "node_program_notes"},
            {"key": "network", "node": "node_program_network"},
            {"key": "mail", "node": "node_program_mail"},
            {"key": "load disk", "node": "node_program_load_disk"},
            {"key": "terminal", "node": "node_program_terminal"}
        ]
        self.menu_type = "menus.generic_terminal"

