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
from world.enums import *
from commands.health_commands import HealthAdminCmdSet
from world.content.species import SPECIES_HUMAN

class Character(DefaultCharacter):
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
    """Base character typeclass for DIC.
    This base Character typeclass should only contain things that would be
    common to NPCs, Mobs, Accounts, or anything else built off of it. Flags
    like "Aggro" would go further downstream.
    """
    def at_object_creation(self):
        super(Character, self).at_object_creation()
        self.db.race = None

        # Core holds information about circulatory systems,
        # pain, etc. It can be considered the "core limb" or body
        # of a creature, and everything requires a body.
        self.db.body = {}

        self.db.position = 'STANDING'

        self.db.pose = self.db.pose or self.db.pose_default
        self.db.pose_death = 'lies dead.'

        self.cmdset.add(HealthAdminCmdSet, permanent=True)
        self.cmdset.add("commands.chargen.ChargenCmdSet", permanent=True)

        self.reset_stats()
        self.apply_species(SPECIES_HUMAN)

    def reset_stats(self):
        self.db.stats = {}

        for attribute in AttributeEnum:
            self.db.stats[attribute.name] = 20
        for skill in SkillEnum:
            self.db.stats[skill.name] = 0

    def apply_species(self, species):
        # Destroy current body.
        self.body.destroy()

        # Apply a new species to body.
        self.body.species = species

        # Initialize new species
        self.body.organs.create_starter_organs()

    @lazy_property
    def stats(self):
        return StatsHandler(self)

    @lazy_property
    def body(self):
        return BodyHandler(self)
