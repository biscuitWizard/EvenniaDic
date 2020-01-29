"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from evennia.utils import lazy_property, utils
from world.stats import StatsHandler
from world.body import BodyHandler
from world.memory import MemoryHandler
from world.enums import *
import re
from commands.admin.character_commands import AdminCharacterCmdSet
from world.content.species import SPECIES_HUMAN
from commands.character_general import CharacterGameCmdSet
from evennia.commands.default.cmdset_character import CharacterCmdSet


_GENDER_PRONOUN_MAP = {
    "male": {"s": "he", "o": "him", "p": "his", "a": "his"},
    "female": {"s": "she", "o": "her", "p": "her", "a": "hers"},
    "neutral": {"s": "it", "o": "it", "p": "its", "a": "its"},
    "ambiguous": {"s": "they", "o": "them", "p": "their", "a": "theirs"},
}
_RE_GENDER_PRONOUN = re.compile(r"(?<!\|)\|(?!\|)[sSoOpPaA]")


class GenderCharacter(DefaultCharacter):
    """
    This is a Character class aware of gender.
    """

    def at_object_creation(self):
        """
        Called once when the object is created.
        """
        super().at_object_creation()
        self.db.gender = "ambiguous"

    def _get_pronoun(self, regex_match):
        """
        Get pronoun from the pronoun marker in the text. This is used as
        the callable for the re.sub function.
        Args:
            regex_match (MatchObject): the regular expression match.
        Notes:
            - `|s`, `|S`: Subjective form: he, she, it, He, She, It, They
            - `|o`, `|O`: Objective form: him, her, it, Him, Her, It, Them
            - `|p`, `|P`: Possessive form: his, her, its, His, Her, Its, Their
            - `|a`, `|A`: Absolute Possessive form: his, hers, its, His, Hers, Its, Theirs
        """
        typ = regex_match.group()[1]  # "s", "O" etc
        gender = self.attributes.get("gender", default="ambiguous")
        gender = gender if gender in ("male", "female", "neutral") else "ambiguous"
        pronoun = _GENDER_PRONOUN_MAP[gender][typ.lower()]
        return pronoun.capitalize() if typ.isupper() else pronoun

    def msg(self, text, from_obj=None, session=None, **kwargs):
        """
        Emits something to a session attached to the object.
        Overloads the default msg() implementation to include
        gender-aware markers in output.
        Args:
            text (str, optional): The message to send
            from_obj (obj, optional): object that is sending. If
                given, at_msg_send will be called
            session (Session or list, optional): session or list of
                sessions to relay to, if any. If set, will
                force send regardless of MULTISESSION_MODE.
        Notes:
            `at_msg_receive` will be called on this Object.
            All extra kwargs will be passed on to the protocol.
        """
        # pre-process the text before continuing
        try:
            text = _RE_GENDER_PRONOUN.sub(self._get_pronoun, text)
        except TypeError:
            pass
        super().msg(text, from_obj=from_obj, session=session, **kwargs)


class Character(GenderCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    @lazy_property
    def stats(self):
        return StatsHandler(self)

    @lazy_property
    def body(self):
        return BodyHandler(self)

    @lazy_property
    def memories(self):
        return MemoryHandler(self)

    """Base character typeclass for DIC.
    This base Character typeclass should only contain things that would be
    common to NPCs, Mobs, Accounts, or anything else built off of it. Flags
    like "Aggro" would go further downstream.
    """
    def at_object_creation(self):
        super(Character, self).at_object_creation()

        # Core holds information about circulatory systems,
        # pain, etc. It can be considered the "core limb" or body
        # of a creature, and everything requires a body.
        self.db.body = dict()
        self.db.memories = []

        self.db.position = 'STANDING'

        self.db.pose = self.db.pose or self.db.pose_default
        self.db.pose_death = 'lies dead.'

        self.cmdset.add(AdminCharacterCmdSet, permanent=True)
        # self.cmdset.add("commands.chargen.ChargenCmdSet", permanent=True)

        # override default command sets.
        self.cmdset.remove(CharacterCmdSet)
        self.cmdset.add(CharacterGameCmdSet, permanent=True)

        self.reset_stats()
        self.apply_species(SPECIES_HUMAN)

    def can_act(self):
        return True

    def can_move(self):
        return True

    def reset_stats(self):
        self.db.stats = {}

        for attribute in AttributeEnum:
            self.db.stats[attribute.name] = 20
        for skill in SkillEnum:
            self.db.stats[skill.name] = 0

    def apply_species(self, species):
        # if species == self.body.species:
        #     return  # Nothing to do. Already this species.

        # Destroy current body.
        self.body.destroy()

        # Apply a new species to body.
        self.body.species = species

        # Initialize new species
        self.body.organs.create_starter_organs()

        # Apply starter resources.
        species = self.body.species
        self.body.current_blood_amount = self.body.max_blood_amount
        if "blood" in species and "starting_resources" in species["blood"]:
            for resource in species["blood"]["starting_resources"]:
                self.msg("adding %s" % resource["amount"] + " %s to blood" % resource["key"])
                self.body.adjust_resources(resource["key"], resource["amount"])
