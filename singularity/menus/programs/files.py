from utils.ui import progress_bar


def _start(caller):
    caller.ndb._menutree.terminal.on_begin_use(caller)


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
        {"key": "return", "goto": _start},
        {"key": "delete", "goto": "node_program_files_delete"},
        {"key": "run", "goto": "node_program_files_run"},
        {"key": "cd", "goto": "node_program_files_cd"},
        {"key": "next page", "goto": "node_program_files_next"},
        {"key": "prev page", "goto": "node_program_files_prev"},
        {"key": "cat", "goto": "node_program_files_cat"}
    ]

    return text, options
