from evennia import DefaultObject, default_cmds, CmdSet


class HealthAdminCmdSet(CmdSet):
    key = "admin_health_cmdset"
    priority = 0

    def at_cmdset_creation(self):
        """Populate CmdSet"""
        self.add(CmdSetExertion())


class CmdSetExertion(default_cmds.MuxCommand):
    key = "health set exertion"

    def func(self):
        args = self.args.split(' ')
        target = self.caller.search(args[0])
        if not target:
            # we didn't find anyone, but search has already let the
            # caller know. We'll just return, since we're done
            return
        target.db.body.exertion = float(args[1])
        self.caller.msg('You set exertion to %s' % target.db.body.exertion)
