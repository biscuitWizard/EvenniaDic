from evennia.utils.evmenu import EvMenu, EvMenuError

from evennia.utils.ansi import strip_ansi
from evennia.utils.utils import mod_import, make_iter, pad, to_str, m_len, is_iter, dedent, crop

# i18n
from django.utils.translation import ugettext as _


_HELP_FULL = _("Commands: <menu option>, help, quit")
_HELP_NO_OPTIONS = _("Commands: help, quit")
_HELP_NO_QUIT = _("Commands: <menu option>, help")
_HELP_NO_OPTIONS_NO_QUIT = _("Commands: help")


class MyEvMenu(EvMenu):
    last_nodename = ''
    cached_string = ''
    cached_options = []

    def goto(self, nodename, raw_string, **kwargs):
        """
        Run a node by name, optionally dynamically generating that name first.
        Args:
            nodename (str or callable): Name of node or a callable
                to be called as `function(caller, raw_string, **kwargs)` or
                `function(caller, **kwargs)` to return the actual goto string or
                a ("nodename", kwargs) tuple.
            raw_string (str): The raw default string entered on the
                previous node (only used if the node accepts it as an
                argument)
        Kwargs:
            any: Extra arguments to goto callables.
        """
        self.cached_string = raw_string

        if callable(nodename):
            # run the "goto" callable, if possible
            inp_nodename = nodename
            nodename = self._safe_call(nodename, raw_string, **kwargs)
            if isinstance(nodename, (tuple, list)):
                if not len(nodename) > 1 or not isinstance(nodename[1], dict):
                    raise EvMenuError(
                        "{}: goto callable must return str or (str, dict)".format(inp_nodename)
                    )
                nodename, kwargs = nodename[:2]
            if not nodename:
                # no nodename return. Re-run current node
                nodename = self.nodename
        try:
            # execute the found node, make use of the returns.
            nodetext, options = self._execute_node(nodename, raw_string, **kwargs)
        except EvMenuError:
            return

        if self._persistent:
            self.caller.attributes.add(
                "_menutree_saved_startnode", (nodename, (raw_string, kwargs))
            )

            # validation of the node return values
        helptext = ""
        if is_iter(nodetext):
            if len(nodetext) > 1:
                nodetext, helptext = nodetext[:2]
            else:
                nodetext = nodetext[0]
        nodetext = "" if nodetext is None else str(nodetext)
        options = [options] if isinstance(options, dict) else options

        # this will be displayed in the given order
        display_options = []
        # this is used for lookup
        self.options = {}
        self.default = None
        if options:
            for inum, dic in enumerate(options):
                # fix up the option dicts
                keys = make_iter(dic.get("key"))
                desc = dic.get("desc", dic.get("text", None))
                if "_default" in keys:
                    keys = [key for key in keys if key != "_default"]
                    goto, goto_kwargs, execute, exec_kwargs = self.extract_goto_exec(nodename, dic)
                    self.default = (goto, goto_kwargs, execute, exec_kwargs)
                else:
                    # use the key (only) if set, otherwise use the running number
                    keys = list(make_iter(dic.get("key", str(inum + 1).strip())))
                    goto, goto_kwargs, execute, exec_kwargs = self.extract_goto_exec(nodename, dic)
                if keys:
                    display_options.append((keys[0], desc))
                    for key in keys:
                        if goto or execute:
                            self.options[strip_ansi(key).strip().lower()] = (
                                goto,
                                goto_kwargs,
                                execute,
                                exec_kwargs,
                            )
        self.cached_options = display_options
        self.nodetext = self._format_node(nodetext, display_options)
        self.node_kwargs = kwargs
        self.nodename = nodename

        # handle the helptext
        if helptext:
            self.helptext = self.helptext_formatter(helptext)
        elif options:
            self.helptext = _HELP_FULL if self.auto_quit else _HELP_NO_QUIT
        else:
            self.helptext = _HELP_NO_OPTIONS if self.auto_quit else _HELP_NO_OPTIONS_NO_QUIT

        if self.nodename != self.last_nodename:
            self.last_nodename = nodename
            self.display_nodetext()
        if not options:
            self.close_menu()

    def display_nodetext(self):
        if self.last_nodename:
            nodename = self.last_nodename
            raw_string = self.cached_string
            kwargs = self.node_kwargs

            if callable(nodename):
                # run the "goto" callable, if possible
                inp_nodename = nodename
                nodename = self._safe_call(nodename, raw_string, **kwargs)
                if isinstance(nodename, (tuple, list)):
                    if not len(nodename) > 1 or not isinstance(nodename[1], dict):
                        raise EvMenuError(
                            "{}: goto callable must return str or (str, dict)".format(inp_nodename)
                        )
                    nodename, kwargs = nodename[:2]
                if not nodename:
                    # no nodename return. Re-run current node
                    nodename = self.nodename
            try:
                # execute the found node, make use of the returns.
                nodetext, options = self._execute_node(nodename, raw_string, **kwargs)
            except EvMenuError:
                return

            self.nodetext = self._format_node(nodetext, self.cached_options)

        super().display_nodetext()


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
