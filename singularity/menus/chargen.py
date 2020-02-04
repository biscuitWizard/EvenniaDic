from world.enums import *
from world.content.chargen import *
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
        "age": 16,
        "is_psionic": False,
        "current_term": 0,
        "species": "human"
    }
    caller.ndb._menutree.terms = []

    for attribute in AttributeEnum:
        caller.ndb._menutree.character["stats"][attribute.name] = 20

    text = """
    Welcome to Singularity's Character Generator!
    
    Have a paragraph about WTF is going on and some info about our game. Also here are some warnings
    that you *definitely* shouldn't make multiple characters. And also here's some commands to
    help get you more info! TBD!!!
    
    |yPlease do not make multiple characters to game chargen.|n
    
    When you're ready, go ahead and like.. type |ybegin|n to start CharGen.
    """

    return text, ({"key": "begin", "goto": "node_menu"})


def node_menu(caller):
    name = caller.ndb._menutree.character["full_name"]
    if not name:
        name = "Not Set"
    species = caller.ndb._menutree.character["species"]
    origin = caller.ndb._menutree.character["origin"]
    if not origin:
        origin = "Not Set"

    d_b = "|gOk|n" if _is_basics_done(caller)[0] else "|rNo|n"
    d_a = "|gOk|n" if _is_attributes_done(caller)[0] else "|rNo|n"
    d_s = "|gOk|n" if _is_skills_done(caller)[0] else "|rNo|n"
    d_l = "|gOk|n" if _is_life_done(caller)[0] else "|rNo|n"

    text = """
    Below are the general details of your character. Use the below commands
    to navigate through chargen steps. Some steps may appear after others are completed.
    
    |wFull Name:|n       %s
    |wSpecies:|n         %s
    |wOrigin:|n          %s
    
    Completed:
    |wBasics:|n          %s
    |wAttributes:|n      %s
    |wStarting Skills:|n %s
    |wLife path:|n       %s    
    """ % (name, species, origin, d_b, d_a, d_s, d_l)

    options = (
        {"key": "basics", "goto": "node_basics"},
        {"key": "attributes", "goto": "node_attributes"},
        {"key": "skills", "goto": "node_skills"}
    )

    return text, options


def node_basics(caller):
    character = caller.ndb._menutree.character
    name = character["full_name"]
    if not name:
        name = "Not Set"
    species = character["species"]
    origin = character["origin"]
    if not origin:
        origin = "Not Set"
    age = character["age"]
    text = """
    |wFull Name:|n       %s
    |wAdolescent Age:|n  %s
    |wSpecies:|n         %s
    |wOrigin:|n          %s
    
    Type |yhelp <command>|n to get info on available choices.
    """ % (name, age, species, origin)

    options = (
        {"key": "return", "goto": "node_menu"},
        {"key": "full_name", "goto": ""},
        {"key": "age", "goto": ""},
        {"key": "species", "goto": ""},
        {"key": "origin", "goto": ""}
    )

    return text, options


def _is_attributes_done(caller):
    if caller.ndb._menutree.points["attributes"] != 0:
        return False, "All attribute points must be allocated."
    return True, ""


def _is_basics_done(caller):
    character = caller.ndb._menutree.character
    name = character["full_name"]
    if not name or len(name) < 3:
        return False, "Full name must have a value and be longer than 3 characters."
    origin = character["origin"]
    if not origin:
        return False, "Must select an origin."
    species_stats = next(s for s in CHARGEN["species"] if s["key"] == character["species"])
    age = character["age"]
    if age < species_stats["min_start_age"]:
        return False, "Age must be equal to or more than %s." % species_stats["min_start_age"]
    if age > species_stats["max_start_age"]:
        return False, "Age must be equal to or less than %s." % species_stats["max_start_age"]
    return True, ""


def _is_skills_done(caller):
    return False, ""


def _is_life_done(caller):
    return False, ""


def node_skills(caller):
    text = """
    """

    index = 0
    stats = caller.ndb._menutree.character["stats"]
    for skill in SkillEnum:
        if index % 2 == 0:
            text += "\n"

        text += ("%s:" % skill.name).ljust(28)
        value = stats.get(skill.name, 0)
        text += str(value).rjust(9)
        if index % 2 == 0:
            text += "  "
        index += 1

    options = (
        {"key": "return", "goto": "node_menu"},
        {"key": "set", "goto": ""}
    )

    return text, options


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

    # options = {"key": "_default", "goto": _node_attributes}
    # if caller.ndb._menutree.points["attributes"] == 0:
    options = ({"key": "_default", "goto": _node_attributes},
               {"key": "return", "goto": "node_menu"})
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


def node_terms(caller):
    text = ""
    term_count = 1
    for term in caller.ndb._menutree.terms:
        text += "\r\n* Term %s:" % term_count + " %s" % term.title
        term_count += 1

    age = caller.ndb._menutree.character["age"] + (4 * caller.ndb._menutree.character["current_term"])
    text += "\r\nCurrent Character Age: %s" % age
    text += "\r\n\r\nType \"|ychoose <term>|n\" to begin a term."

    options = ({"key": "_default", "goto": _node_terms},
               {"key": "list choices", "goto": _list_term_choices},
               {"key": "finish", "goto": "node_finish"})
    return text, options


def _node_terms(caller, raw_string):
    match = re.match(r"choose (\w+)", raw_string)
    if not match:
        error(caller, "I didn't understand that.")
        return "node_terms"

    term_token = match.group(1).lower()
    term = next((x for x in TERMS if x["title"].lower().startswith(term_token)), None)
    if not term:
        error(caller, "%s is not a valid term. Type \"|ylist choices|n\" to get a list of all available careers.")
        return "node_terms"

    caller.ndb._menutree.terms.append({
        "term": term["title"]
    })
    return "node_term"


def _list_term_choices(caller):
    text = ""
    for term in TERMS:
        text += "\r\n* %s" % term["title"]
        for assignment in term["assignments"]:
            text += "\r\n\t- %s: " % assignment["title"]
            text += "sample description text"

    caller.msg(text)
    return "node_terms"


def node_term(caller):
    term_title = caller.ndb._menutree.terms[len(caller.ndb._menutree.terms) - 1]["term"]
    # term = next((x for x in TERMS if x["title"] == term_title), None)
    text = "Career: %s" % term_title
    text += "\r\nAssignment: Not Set"
    text += "\r\nPersonal Advancement: Not Set"
    text += "\r\nYears: %s" % caller.ndb._menutree.character["age"]
    text += "-%s" % (caller.ndb._menutree.character["age"] + 4)
    text += "\r\n\r\nLife Event: |y1 Available|n"

    text += "\r\n\r\nType \"|yset Assignment to <assignment>|n\" to choose an assignment."
    text += "\r\nType \"|yset Advancement to <option>|n\" to choose a personal advancement."
    text += "\r\n\r\nRolling for a life event is optional and may yield positive or negative results. "
    text += "Once you've chosen to roll a life event, the result cannot be rerolled or changed except through mulligan."

    options = ({"key": "show assignments", "goto": _list_term_assignments},
               {"key": "show advancements", "goto": _list_term_advancements},
               {"key": "roll life event", "goto": _do_life_event})
    return text, options


def _list_term_advancements(caller):
    return "node_term"


def _list_term_assignments(caller):
    return "node_term"


def _do_life_event(caller):
    return "node_term"


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
