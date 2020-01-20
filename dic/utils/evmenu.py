from evennia.utils.evmenu import EvMenu


class DICEvMenu(EvMenu):
    def node_formatter(self, nodetext, optionstext):
        header = """|c
    __                                                 ____________________
 __/  \_______________________________________________/                    \__
/  \__/
\__/|n
        """

        footer = """|c
 __                                                                    __
/  \__________________________________________________________________/  \__
\__/                                                                  \__/  \\
                                                                         \__/                                                          
        |n"""
        return header + "\r\n" + nodetext + "\r\n" + optionstext + "\r\n" + footer
