from typeclasses.objects import Object


class Limb(Object):
    wounds = []

    def at_object_creation(self):
        super(Limb, self).at_object_creation()
        self.locks.add("puppet:false();limb:true()")
        self.db.wounds = self.wounds
        self.db.used_by = None
