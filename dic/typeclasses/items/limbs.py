from typeclasses.items.organs import BodyPart


class Limb(BodyPart):
    @property
    def size_capacity(self):
        return self.db.size_capacity

    @size_capacity.setter
    def size_capacity(self, value):
        self.db.size_capacity = value

    def at_object_creation(self):
        super(Limb, self).at_object_creation()
        self.locks.add("puppet:false();limb:true()")
        self.db.used_by = None
