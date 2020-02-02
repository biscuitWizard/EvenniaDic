def _start(caller):
    caller.ndb._menutree.terminal.on_begin_use(caller)


def node_program_mail(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "return", "goto": _start},
        {"key": "new", "goto": "node_program_mail_new"},
        {"key": "del", "goto": "node_program_mail_del"},
        {"key": "read", "goto": "node_program_mail_view"}
    ]

    return text, options
