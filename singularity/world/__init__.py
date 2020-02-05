from evennia.utils import create, logger
from django.conf import settings
from django.utils.translation import ugettext as _


START_ROOM_DESC = _(
    """
Welcome to your new |wEvennia|n-based game! Visit http://www.evennia.com if you need
help, want to contribute, report issues or just join the community.
As Account #1 you can create a demo/tutorial area with |w@batchcommand tutorial_world.build|n.
    """
)


logger.log_info("Post setup: Creating objects (New Arrivals Room) ...")
room_typeclass = settings.BASE_ROOM_TYPECLASS
start_room = create.create_object(room_typeclass, _("District 18 - New Arrivals"), nohome=True)
start_room.id = 3
start_room.db.desc = START_ROOM_DESC
start_room.save()