from evennia.utils.utils import rjust, ljust

def start(caller):
    text = "Make a selection from the left..."
    options = [
        {"key": "files", "goto": "node_program_files"},
    ]

    for program in caller.ndb._menutree.terminal.programs:
        options.append({
            "key": program["key"],
            "goto": program["node"]
        })

    options.append({"key": "exit", "goto": "exit"})

    return text, options


def node_program_notes(caller):
    pass


def node_program_files(caller):
    text = ""
    files = caller.ndb._menutree.terminal.files
    index = 0
    while index < len(files):
        if index % 2 == 0:
            text += "\n"
        file1 = files[index]
        file_index = rjust(index, 2, fillchar='0')
        file_name = ljust(file1["key"], 20)
        file_size = rjust(file1["size"], 3)
        text += "%s. %s [%su]" % (file_index, file_name, file_size)
        if index % 2 == 1:
            text += "  "
        index += 1

    options = [
        {"key": "back", "goto": "start"},
        {"key": "delete", "goto": "node_program_files_delete"},
        {"key": "run", "goto": "node_program_files_run"}
    ]

    return text, options


def node_program_network(caller):
    pass


def node_program_load_disk(caller):
    pass


def node_program_mail(caller):
    pass


def node_program_terminal(caller):
    pass
