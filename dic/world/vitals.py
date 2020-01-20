from world.organs import OrganType
from typeclasses.items.organs import ConsciousnessState


class VitalsHandler(object):
    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

    def is_alive(self):
        nervous_system = self.obj.organs.find_organ(OrganType.NervousSystem)
        if not nervous_system:
            return False
        return nervous_system.conciousness != ConsciousnessState.Dead

    def has_heartbeat(self):
        heart = self.obj.organs.find_organ(OrganType.Heart)
        if not heart:
            return False
        return heart.get_heartrate() > 0

    def get_bpm(self):
        if not self.has_heartbeat():
            return 0
        heart = self.obj.organs.find_organ(OrganType.Heart)
        return heart.get_heartrate()

    def has_blood(self):
        return self.obj.db.body.cur_blood > 0

    """ 
    Outputs a value 0-1 range of the oxygenation of the *current blood* in the body.
    
    If there's a lot of blood loss, this value will still be high.
    """
    def get_oxygenation(self):
        max_oxygen = (self.obj.db.body.cur_blood / 10.0) * 20.1
        self.obj.db.body.blood_oxygen = min(self.obj.db.body.blood_oxygen, max_oxygen)

        return round(self.obj.db.body.blood_oxygen / max_oxygen, 2)

    def get_pain(self):
        return 0

    """0-1 value for human ranges. If above 1, can cause cardiac arrest. """
    def get_exertion(self):
        return self.obj.db.body.exertion

    def get_brain_activity(self):
        nervous_system = self.obj.organs.find_organ(OrganType.NervousSystem)
        if not nervous_system:
            return 0
        return nervous_system.get_efficiency()

    """In millilitres"""
    def get_blood_amount(self):
        return self.obj.db.body.cur_blood

    """ Array of reagents. """
    def get_blood_contents(self):
        return self.obj.db.body.blood_contents

    """In celsius"""
    def get_body_temp(self):
        return self.obj.db.body.temperature

    """ Positive amounts to add oxygen, negative amounts to remove oxygen."""
    def adjust_blood_oxygen(self, amount):
        max_oxygen = (self.obj.db.body.cur_blood / 10.0) * 20.1
        new_oxygen = round(self.obj.db.body.blood_oxygen + amount, 2)
        self.obj.db.body.blood_oxygen = max(min(new_oxygen, max_oxygen), 0)


