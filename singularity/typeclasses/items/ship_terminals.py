from typeclasses.items.ship_components import ShipComponent
from typeclasses.items.terminals import Terminal


class ShipTerminal(ShipComponent, Terminal):
    pass


class HelmTerminal(ShipTerminal):
    pass


class SensorsTerminal(ShipTerminal):
    pass


class EngineeringTerminal(ShipTerminal):
    pass


class WeaponsTerminal(ShipTerminal):
    pass
