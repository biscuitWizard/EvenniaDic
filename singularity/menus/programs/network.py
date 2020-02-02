def _start(caller):
    caller.ndb._menutree.terminal.on_begin_use(caller)


def node_program_network(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "return", "goto": _start},
        {"key": "disconnect", "goto": "node_program_network_disconnect"},
        {"key": "connect", "goto": "node_program_network_connect"},
        {"key": "set tag", "goto": "node_program_network_set_tag"}
    ]

    return text, options
