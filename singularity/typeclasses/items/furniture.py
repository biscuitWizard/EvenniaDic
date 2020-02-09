from typeclasses.objects import InstallationObject

class FurnitureObject(InstallationObject):
    pass


class ShopFurnitureObject(FurnitureObject):
    @property
    def shop_inventory(self):
        return self.db.shop_inventory

    @shop_inventory.setter
    def shop_inventory(self, value):
        self.db.shop_inventory = value

    def at_object_creation(self):
        super(FurnitureObject, self).at_object_creation()
        self.shop_inventory = {}