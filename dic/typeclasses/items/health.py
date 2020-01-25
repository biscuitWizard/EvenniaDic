import time


class Wound:
    severity = 0
    created_on = 0
    wound_type = None

    def __init__(self, wound_type, severity):
        self.created_on = time.time()
        self.wound_type = wound_type
        self.severity = severity

