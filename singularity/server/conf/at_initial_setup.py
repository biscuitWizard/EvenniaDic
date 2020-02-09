"""
At_initial_setup module template

Custom at_initial_setup method. This allows you to hook special
modifications to the initial server startup process. Note that this
will only be run once - when the server starts up for the very first
time! It is called last in the startup process and can thus be used to
overload things that happened before it.

The module must contain a global function at_initial_setup().  This
will be called without arguments. Note that tracebacks in this module
will be QUIETLY ignored, so make sure to check it well to make sure it
does what you expect it to.

"""
from evennia.utils import create, logger
from django.conf import settings
from django.utils.translation import ugettext as _
from commands.chargen import ChargenCmdSet


START_ROOM_DESC = _(
    """
Fancy room description.

Type |ychargen|n to begin character generation.
    """
)


def at_initial_setup():
    logger.log_info("Post setup: Creating objects (New Arrivals Room) ...")
    room_typeclass = settings.BASE_ROOM_TYPECLASS
    start_room = create.create_object(room_typeclass, _("District 18 - New Arrivals"), nohome=True)
    start_room.save()
    start_room.db.desc = START_ROOM_DESC
    start_room.cmdset.add(ChargenCmdSet, permanent=True)
    start_room.save()







