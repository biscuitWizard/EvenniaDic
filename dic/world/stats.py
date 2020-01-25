# from world.enums import AttributeEnum


class StatsHandler(object):
    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

    """ Attributes are 0-100, with 30 being average. """
    def get_attribute(self, attributeEnum):
        return 30

    pass
