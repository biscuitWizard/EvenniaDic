from evennia import DefaultObject, default_cmds, CmdSet
from world.organs import OrganType


class DefaultCmdSet(CmdSet):
    """
    The default cmdset always sits
    on the button object and whereas other
    command sets may be added/merge onto it
    and hide it, removing them will always
    bring it back. It's added to the object
    using obj.cmdset.add_default().
    """

    key = "RedButtonDefault"
    mergetype = "Union"  # this is default, we don't really need to put it here.

    def at_cmdset_creation(self):
        "Init the cmdset"
        self.add(CmdScan())

class CmdScan(default_cmds.MuxCommand):
    """
    Scans someone.

    Usage: scan <target>
    """
    key = "scan"

    def func(self):
        """Executes poke command"""
        target = self.caller.search(self.args)
        if not target:
            # we didn't find anyone, but search has already let the
            # caller know. We'll just return, since we're done
            return
        # we found a target! we'll do stuff to them.
        response = "=== %s Vitals ===" % target
        response += "\r\nHeart-rate: %s bpm" % target.body.get_bpm()
        response += "\r\nOxygenation: %s%%" % (target.body.get_oxygenation() * 100)
        response += "\r\nBrain Activity: %s%%" % (target.body.get_brain_activity() * 100)
        response += "\r\nBlood: %s" % target.body.current_blood_amount
        response += "/%s mL" % target.body.max_blood_amount
        heart = target.body.organs.find_organ(OrganType.Heart)
        response += "\r\nBlood Flow: %s mL/min" % heart.get_flow(target)
        response += "\r\nBody Temperature: %sc" % target.body.temperature
        self.caller.msg(response)
        # target.msg("You have been poked by %s." % self.caller)
        # self.caller.msg("You have poked %s." % target)

class MedicalScanner(DefaultObject):
    def at_object_creation(self):
        """
        This function is called when object is created. Use this
        instead of e.g. __init__.
        """
        # store desc (default, you can change this at creation time)
        desc = "A medical scanner device for showing vitals."
        self.db.desc = desc

        self.cmdset.add_default(DefaultCmdSet, permanent=True)

        # since the cmdsets relevant to the button are added 'on the fly',
        # we need to setup custom scripts to do this for us (also, these scripts
        # check so they are valid (i.e. the lid is actually still closed)).
        # The AddClosedCmdSet script makes sure to add the Closed-cmdset.
        # self.scripts.add(scriptexamples.ClosedLidState)
        # the script EventBlinkButton makes the button blink regularly.
        # self.scripts.add(scriptexamples.BlinkButtonEvent)
