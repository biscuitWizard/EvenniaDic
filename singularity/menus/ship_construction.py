def start(caller, ship):
    if not caller:
        return

    text = "Vessel Name: %s" % ship.name
    text += "\nRegistration ID: %s" % ship.registration_id
    text += "\nRegistered To: %s" % ship.registered_to.name
    text += "\nTrade Value: 55.6mCr"
    text += "\n\nTonnage: %s" % ship.tonnage
    text += "\nRooms: %s" % len(ship.rooms)
    text += "\nInsurance: None"
    text += "\n\nPayment Remaining: 25.2mCr"
    text += "\nWeekly Payment: 4432.22Cr"
    text += "\nNext Due: 3 days, 4 hours"

    options = (
        {"key": "rename vessel", "goto": "node_rename_vessel"},
        {"key": "transfer registration", "goto": "node_transfer_vessel"},
        {"key": "shipyard", "goto": "node_shipyard"},
        {"key": "exit", "goto": "exit"}
    )
    return text, options


def node_rename_vessel(caller):
    pass


def node_transfer_vessel(caller):
    pass


def node_shipyard(caller, ship):
    pass
