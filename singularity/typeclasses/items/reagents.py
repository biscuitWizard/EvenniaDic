from typeclasses.objects import Object


class Reagent(Object):
    """
        A ratio from 0-1 describing how fast this compound
        can be processed through an organic body.

        Highly metabolic compounds (1) will filter out of the
        blood at a much higher rate than medium metabolic compounds (0.5)

        Metabolic compounds with a 0 will never leave the body without
        filtration from an external source.
    """
    metabolizability = 0
    amountMilliliters = 0

    def at_object_creation(self):
        super(Reagent, self).at_object_creation()
        self.locks.add("puppet:false();reagent:true()")
        self.db.metabolizability = self.metabolizability
        self.db.amountMilliliters = self.amountMilliliters
