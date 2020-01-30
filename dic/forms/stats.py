from evennia import EvForm, EvTable
from world.enums import *
from evennia.utils.utils import pad


FORMCHAR = "x"
TABLECHAR = "c"

FORM = """
.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1xxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
|                                                              |
| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  xxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| xxxxxxxxxxxxxxx2xxxxxxxxxxxxxx  xxxxxxxxxxxxxx3xxxxxxxxxxxxx |
| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  xxxxxxxxxxxxxxxxxxxxxxxxxxxx |
|                                                              |
 >------------------------------------------------------------<
| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  xxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  xxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  xxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| xxxxxxxxxxxxxxx4xxxxxxxxxxxxxx  xxxxxxxxxxxxx5xxxxxxxxxxxxxx |
| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  xxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  xxxxxxxxxxxxxxxxxxxxxxxxxxxx |
 >------------------------------------------------------------<
"""


def show(character):
    # create a new form from the template
    form = EvForm("forms/stats.py")

    # add data to each tagged form cell
    tableA = "|wHeight:|n %s\n|wBuild:|n %s\n|wEye Color:|n %s" % ("1.74m", "Thin (45kg)", "Blue")
    tableB = "|wSpecies:|n %s\n|wOrigin:|n %s" % (character.body.species["key"], "Spacer")
    tableC = ""
    tableD = ""

    index = 0
    for attribute in AttributeEnum:
        attribute_name = pad("\n|w%s:|n" % attribute.name, width=18, align="l")
        attribute_value = get_attribute_wordlevel(character.stats.get_attribute(attribute))
        if index % 2:
            tableD += attribute_name + " " + attribute_value
        else:
            tableC += attribute_name + " " + attribute_value
        index += 1

    character_name = pad("[ " + character.name + " ]", width=62, fillchar='-')

    form.map(cells={1: character_name, 2: tableA, 3: tableB, 4: tableC, 5: tableD})
    # create the EvTables

    return str(form)