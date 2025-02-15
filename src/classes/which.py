#!/usr/bin/env python3
"""
Which() class file
"""

import os
import sys


class Which:
    """
    Attempt to locate and return the full path to a given binary on the given
    user's $PATH. This functionality closely mimics the `which` binary on
    Linux systems.
    """

    def __init__(self) -> None:
        self.paths = []
        self.command = ''
        self.path = os.getenv('PATH')
        if self.path is None:
            msg = 'ERROR: Unable to read contents of $PATH environment '
            msg += 'variable!'
            print(msg)
            sys.exit(1)

        self.get_paths()

    def get_paths(self) -> None:
        """
        Split the output of the os.getenv() call in __init__ if not empty.
        """
        if self.path is not None:
            self.paths = self.path.split(':')

    def find_command(self, command: str) -> bool:
        """
        Search all paths from self.path for the given binary.

        :param command: The name of the binary to search for
        :type command: str
        :return: True if found, False if not found
        :rtype: bool
        """
        for path in self.paths:
            command_path = os.path.join(path, command)
            if os.path.exists(command_path):
                self.command = command_path
                return True
        return False
