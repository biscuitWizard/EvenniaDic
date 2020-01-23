from typeclasses.items.organs import Organ, OrganType


class Cybernetic(Organ):
    @property
    def is_passive(self):
        return self.db.is_passive

    @is_passive.setter
    def is_passive(self, value):
        self.db.is_passive = value

    @property
    def power_consumption(self):
        return self.db.power_consumption

    @power_consumption.setter
    def power_consumption(self, value):
        self.db.power_consumption = value

    def on_activate(self, character):
        pass

    def on_deactivate(self, character):
        pass

    def on_use(self, character):
        pass


class CyberBattery(Cybernetic):
    """Provides power for other implants."""
    pass


class BioReactor(Cybernetic):
    """Converts a portion of calories into power."""
    pass
