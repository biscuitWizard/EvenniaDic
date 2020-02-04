def _start(caller):
    caller.ndb._menutree.terminal.on_begin_use(caller)


def node_program_terminal(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "return", "goto": _start},
    ]

    return text, options
