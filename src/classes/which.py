#!/usr/bin/env python3
"""
Emulate the which command in Python
"""

import os
import sys


class Which:
    """
    Emulate the which command in Python
    """

    paths = []
    command = None

    def __init__(self) -> None:
        self.path = os.getenv('PATH')
        if self.path is None:
            print('ERROR: Unable to get the $PATH environment variable!')
            sys.exit(1)

        self.get_paths()

    def get_paths(self) -> None:
        """
        Split the output of the $PATH variable into a list of paths
        """
        if self.path is not None:
            self.paths = self.path.split(':')

    def find_command(self, command: str) -> bool:
        """
        Search all paths from $PATH for the given binary.
        Return True if found, False if not.
        Set the command attribute appropriately.
        """
        for path in self.paths:
            command_path = os.path.join(path, command)
            if os.path.exists(command_path):
                self.command = command_path
                return True
        return False
