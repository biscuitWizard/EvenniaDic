# from world.enums import AttributeEnum


class StatsHandler(object):
    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

    """ Attributes are 0-100, with 30 being average. """
    def get_attribute(self, attribute_enum):
        raw_attribute = self.get_raw_attribute(attribute_enum)
        body_attribute = self.obj.body.get_attribute(attribute_enum)

        return min(raw_attribute, body_attribute)

    def get_raw_attribute(self, attribute_enum):
        return self.obj.stats.get(attribute_enum, 0)

    def get_skill(self, skill_enum):
        return self.get_raw_skill(skill_enum)

    def get_raw_skill(self, skill_enum):
        return self.obj.stats.get(skill_enum, 0)
