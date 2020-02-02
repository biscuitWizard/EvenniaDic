class NavigationHandler(object):
    @property
    def current_orbit(self):
        return None

    @property
    def destination(self):
        return None

    @property
    def max_speed(self):
        return None

    @property
    def max_g_force(self):
        return None

    @property
    def route_calculation(self):
        return 0.00

    @property
    def deviation(self):
        return 0.00

    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

    def is_calculating_route(self):
        return False

