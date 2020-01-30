from evennia import default_cmds


class CmdDefense(default_cmds.MuxCommand):
    def func(self):
        pass


class CmdPass(CmdDefense):
    pass


class CmdDodge(CmdDefense):
    pass


class CmdParry(CmdDefense):
    pass


class CmdBlock(CmdDefense):
    pass


class CmdQuickshot(CmdDefense):
    pass
