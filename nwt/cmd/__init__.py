# -*- coding: utf-8 -*-
"""
Module for interaction with command input
"""

import sys
from prompt_toolkit import PromptSession

from nwt.cmd.inputparser import InputParser
from nwt.cmd.outputparser import OutputParser


class Interactive(object):
    """
    Interactive command session
    """

    def __init__(self):
        self.leftprompt = ' nwt > '
        self.prompt_session = PromptSession()

    def prompter(self):
        """
        Function to replace default 'input' -> 'prompt'
        """

        try:
            result = self.prompt_session.prompt(self.leftprompt)
            return result
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

    def inject(self, query):
        parsed = InputParser(query)
        out = OutputParser(parsed)
        print(out)

    def run(self):
        while True:
            self.inject(self.prompter().lower())
