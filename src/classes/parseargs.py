#!/usr/bin/env python3
"""
ParseArgs() class file
"""
import argparse

from src.classes.file_checker import FileChecker
from src.constants import constants


class ParseArgs():
    """
    Accept and validate command line parameters
    """
    NAME = constants.ARGPARSE_PROGRAM_NAME
    DESC = constants.ARGPARSE_PROGRAM_DESCRIPTION
    VERSION = constants.ARGPARSE_VERSION
    AUTHOR = constants.ARGPARSE_AUTHOR
    REPO = constants.ARGPARSE_REPO

    def __init__(self, args) -> None:
        self.args = args
        self.parser = argparse.ArgumentParser(
            prog=self.NAME, description=self.DESC)
        self.config_file = ''

        self.parser.add_argument(
            '-v',
            '--version',
            action='store_true',
            required=False,
            help='Show this program\'s current version')

        self.parser.add_argument(
            '-c',
            '--config-file',
            nargs=1,
            required=False,
            help='Optionally specify the full path to a custom config file'
        )

        self.parse_args = self.parser.parse_args()

        if self.parse_args.version:
            self._print_version()
            self.parser.exit()

        if self.parse_args.config_file:
            config_file = self.parse_args.config_file[0]
            fc = FileChecker(config_file)
            if not fc.is_file():
                self.parser.error(f'{fc.file} is not a valid file!')

            if not fc.is_readable():
                self.parser.error(f'{fc.file} is not readable!')

            if not fc.is_yaml():
                self.parser.error(f'{fc.file} is not a valid YAML file!')

            self.config_file = fc.file

    def _print_version(self) -> None:
        """
        Print out the warranty and version number of the program.

        :return: None
        :rtype: None
        """
        print(f'{self.NAME} v{self.VERSION}')
        print(
            'This is free software:',
            'you are free to change and redistribute it.')
        print('There is NO WARARNTY, to the extent permitted by law.')
        print(f'Written by {self.AUTHOR}; see below for original code')
        print(f'<{self.REPO}')
