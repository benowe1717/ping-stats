#!/usr/bin/env python3
"""
FileChecker() class file
"""
import json
import os
import sys

import yaml


class FileChecker():
    """
    Determine and obtain several attributes associated with files and
    directories.
    """

    def __init__(self, file: str) -> None:
        try:
            if '~' in file:
                file = os.path.expanduser(file)

            self.file = os.path.realpath(file, strict=True)
            self.yaml = {}
            self.json = {}
        except FileNotFoundError:
            print(f'Unable to locate {file}')
            sys.exit(1)

    def is_file(self) -> bool:
        """
        Determine if self.file is a file

        :return: True if is file, False if not file
        :rtype: bool
        """
        if os.path.isfile(self.file):
            return True
        return False

    def is_dir(self) -> bool:
        """
        Determine if self.file is a folder

        :return: True if is directory, False if not directory
        :rtype: bool
        """
        if os.path.isdir(self.file):
            return True
        return False

    def is_readable(self) -> bool:
        """
        Determine if self.file is readable by the user executing the program

        :return: True if readable, False if not readable
        :rtype: bool
        """
        if os.access(self.file, os.R_OK):
            return True
        return False

    def is_writable(self) -> bool:
        """
        Determine if self.file is writable by the user executing the program

        :return: True if writable, False if not writable
        :rtype: bool
        """
        if os.access(self.file, os.W_OK):
            return True
        return False

    def is_yaml(self) -> bool:
        """
        Determine if self.file contains valid YAML data
        If True, read contents of self.file into self.yaml property

        :return: True if valid YAML, False if not valid YAML
        :rtype: bool
        """
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if isinstance(data, dict):
                self.yaml = data
                return True
            return False
        except yaml.YAMLError:
            return False

    def is_json(self) -> bool:
        """
        Determine if self.file contains valid JSON data
        If True, read contents of self.file into self.json property

        :return: True if valid JSON, False if not valid JSON
        :rtype: bool
        """
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                self.json = json.load(f)
            return True
        except json.JSONDecodeError:
            return False
