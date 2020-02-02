def start(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "files", "goto": "node_program_files"},
    ]

    for program in caller.using.programs:
        options.append({
            "key": program["key"],
            "goto": (_launch_program, {"program": program})
        })

    # options.append({"key": "exit", "goto": "exit"})

    return text, options


def _launch_program(caller, **kwargs):
    caller.ndb._menutree.terminal.launch_program(kwargs.get("program"))

