from typeclasses.objects import Object


class Terminal(Object):
    @property
    def used_by(self):
        return self.db.used_by

    @used_by.setter
    def used_by(self, value):
        self.db.used_by = value

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
        super(Terminal, self).at_object_creation()

        self.used_by = None
        self.is_bolted = False

    def on_begin_use(self, character):
        pass

    def on_end_use(self, character):
        pass
