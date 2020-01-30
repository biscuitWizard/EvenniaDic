import time
from evennia.utils import utils
from django.conf import settings

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)


class MemoryHandler(object):
    @property
    def memories(self):
        return self.obj.db.memories

    def __init__(self, obj):
        # save the parent typeclass
        self.obj = obj

        if not hasattr(self.obj.db, 'memories'):
            raise Exception('`MemoryHandler` requires `db.memories` attribute on `{}`.'.format(obj))

    def add_memory(self, content, is_hidden=False):
        if not content or content == '':
            return
        existing_memory = next((m for m in self.memories if m["content"] == content.lower()), None)
        if existing_memory:
            return

        self.memories.append({
            "content": content,
            "added_on": time.time(),
            "is_hidden": is_hidden
        })


class MemorizeCmd(COMMAND_DEFAULT_CLASS):
    key = "memorize"
    locks = "cmd:all()"

    def func(self):
        if not self.args or self.args == '':
            self.caller.msg("Please enter something to memorize.")
            return

        def memorize_callback():
            self.caller.msg("You successfully memorize it.")
            self.caller.memories.add_memory(self.args)

        self.caller.msg("You begin repeating '%s' back to yourself repeatedly." % self.args)
        utils.delay(2, memorize_callback)


class MemoriesCmd(COMMAND_DEFAULT_CLASS):
    key = "memory"
    locks = "cmd:all()"

    def func(self):
        memories = self.caller.memories.memories
        if len(memories) == 0:
            self.caller.msg("You don't remember anything.")
            return

        self.caller.msg("You recall:")
        for memory in self.caller.memories.memories:
            self.caller.msg("\t%s" % memory["content"])

