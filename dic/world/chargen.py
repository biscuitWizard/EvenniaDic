from world.stats import AttributeEnum, SkillEnum
import re


def start(caller):
    if not caller:
        return
    caller.ndb._menutree.points = {
        "attributes": 20,
        "skills": 20
    }
    caller.ndb._menutree.character = {
        "home_planet": None,
        "full_name": None,
        "origin": None,
        "stats": {},
        "age": 18,
        "is_psionic": False
    }

    for attribute in AttributeEnum:
        caller.ndb._menutree.character["stats"][attribute.name] = 20

    return "begin when ready", {"key": "begin", "goto": "node_attributes"}


def node_attributes(caller):
    text = ""
    for attribute in AttributeEnum:
        if attribute == AttributeEnum.Psi and not caller.ndb._menutree.character["is_psionic"]:
            continue
        text += "%s: " % attribute.name
        text += "%s\r\n" % caller.ndb._menutree.character["stats"][attribute.name]
    text += "\r\n%s points remaining.\r\n" % caller.ndb._menutree.points["attributes"]
    text += "\r\nType \"|yadd <number> to <attribute>|n\" to adjust an attribute positively."
    text += "\r\nType \"|ysub <number> from <attribute>|n\" to adjust an attribute negatively."

    options = {"key": "_default", "goto": _node_attributes}
    return text, options


def _node_attributes(caller, raw_string):
    match = re.match(r"add (\d+) to (\w+)", raw_string)
    if match:
        return adjust_attribute(caller, match, True)
    match = re.match(r"sub (\d+) from (\w+)", raw_string)
    if match:
        return adjust_attribute(caller, match, False)

    if not match:
        return "node_attributes"


def adjust_attribute(caller, match, is_add):
    attribute_token = match.group(2).lower()
    attribute = next((x for x in AttributeEnum if x.name.lower().startswith(attribute_token)), None)
    if not attribute:
        error(caller, "%s is not a valid attribute." % match.group(2))
        return "node_attributes"
    value = int(match.group(1))
    if not value or value < 0:
        error(caller, "Value to adjust must be a positive number.")
        return "node_attributes"

    attribute_value = caller.ndb._menutree.character["stats"][attribute.name]
    if not is_add and attribute_value - value < 10:
        error(caller, attribute.name + " cannot be reduced below 10.")
        return "node_attributes"

    # calculate cost..
    i_value = value
    cost = 0
    while i_value > 0:
        if is_add:
            new_value = i_value + attribute_value
        else:
            new_value = attribute_value - i_value

        if new_value <= 12:
            cost += 4
        elif new_value <= 16:
            cost += 2
        elif new_value <= 23:
            cost += 1
        elif new_value <= 26:
            cost += 2
        elif new_value <= 30:
            cost += 4
        i_value -= 1

    if not is_add:
        cost *= -1

    if cost > caller.ndb._menutree.points["attributes"]:
        deficit = (caller.ndb._menutree.points["attributes"] - cost) * -1
        error(caller, "Raising %s" % attribute.name + " costs %s total points," % cost + " %s more points than you have available." % deficit)
        return "node_attributes"

    # Succeeded the gauntlet. Change their stat.
    if is_add:
        caller.ndb._menutree.character["stats"][attribute.name] += value
    else:
        caller.ndb._menutree.character["stats"][attribute.name] -= value
    caller.ndb._menutree.points["attributes"] -= cost

    msg = "Successfully set %s " % attribute.name + "to %s" % caller.ndb._menutree.character["stats"][attribute.name]
    msg += " for %s points." % cost
    success(caller, msg)
    return "node_attributes"


def success(caller, msg):
    caller.msg("|b<|cSystem|b>|n %s" % msg)


def error(caller, msg):
    caller.msg("|y<|rError|y>|n %s" % msg)
