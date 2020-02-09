from evennia.typeclasses import DefaultScript

class CorporationScript(DefaultScript):
    @property
    def corporations(self):
        return self.db.corporations

    def at_script_creation(self):
        self.key = "global corporations"
        self.desc = "Manages global corporation simulation and storage."
        self.interval = 60
        self.persistent = True

        self.db.corporations = []

    def get_or_create_corporation(self, key):
        corporation = next((c for c in self.corporations if c["key"] == key), None)
        if not corporation:
            corporation = {}
        if "buildings" not in corporation:
            corporation["buildings"] = []
        if "workforce" not in corporation:
            corporation["workforce"] = []

        return corporation

    def at_repeat(self):
        pass