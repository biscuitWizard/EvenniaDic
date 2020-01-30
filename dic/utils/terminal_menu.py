from evennia.utils.evmenu import EvMenu
from evennia.utils.ansi import strip_ansi
from forms import terminal


class TerminalEvMenu(EvMenu):
    def node_formatter(self, nodetext, optionstext):
        return terminal.show("TEST", optionstext, nodetext)

    def options_formatter(self, optionlist):
        """
        Formats the option block.
        Args:
            optionlist (list): List of (key, description) tuples for every
                option related to this node.
            caller (Object, Account or None, optional): The caller of the node.
        Returns:
            options (str): The formatted option display.
        """
        if not optionlist:
            return ""

        text = ""
        for key, desc in optionlist:
            raw_key = strip_ansi(key)
            text += "|w[%s]|n\n" % raw_key.upper()

        return text
