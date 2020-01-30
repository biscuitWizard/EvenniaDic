from utils.ui import progress_bar


def start(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "files", "goto": "node_program_files"},
    ]

    for program in caller.using.programs:
        options.append({
            "key": program["key"],
            "goto": program["node"]
        })

    # options.append({"key": "exit", "goto": "exit"})

    return text, options


def node_program_notes(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"},
        {"key": "new", "goto": "node_program_notes_new"},
        {"key": "del", "goto": "node_program_notes_del"},
        {"key": "read", "goto": "node_program_notes_view"}
    ]

    return text, options


def node_program_files(caller):
    text = ""
    files = caller.using.files
    index = 0
    while index < len(files):
        file1 = files[index]
        file_index = "|w%s|n" % str(index + 1).rjust(2, '0')
        file_name = file1["key"].ljust(36)
        file_size = str(file1["size"]).rjust(5)
        text += "%s. %s [%su]\n" % (file_index, file_name, file_size)
        index += 1

    text += "\n\n"
    text += progress_bar(10, 100, width=30, display="multicolor-inverse")
    text += " 90% free space"

    options = [
        {"key": "back", "goto": "start"},
        {"key": "delete", "goto": "node_program_files_delete"},
        {"key": "run", "goto": "node_program_files_run"},
        {"key": "cd", "goto": "node_program_files_cd"},
        {"key": "next page", "goto": "node_program_files_next"},
        {"key": "prev page", "goto": "node_program_files_prev"},
        {"key": "cat", "goto": "node_program_files_cat"}
    ]

    return text, options


def node_program_network(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"},
        {"key": "disconnect", "goto": "node_program_network_disconnect"},
        {"key": "connect", "goto": "node_program_network_connect"},
        {"key": "set tag", "goto": "node_program_network_set_tag"}
    ]

    return text, options


def node_program_load_disk(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"}
    ]

    return text, options


def node_program_mail(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"},
        {"key": "new", "goto": "node_program_mail_new"},
        {"key": "del", "goto": "node_program_mail_del"},
        {"key": "read", "goto": "node_program_mail_view"}
    ]

    return text, options


def node_program_terminal(caller):
    text = "\n\nMake a selection from the left..."
    options = [
        {"key": "back", "goto": "start"}
    ]

    return text, options
