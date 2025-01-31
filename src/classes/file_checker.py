#!/usr/bin/env python3
"""
Helper methods to determine if a file is preset, readable, writable, or any
other properties associated with files and folder
"""
import json
import os
import sys

import yaml


class FileChecker():
    """
    Helper methods to determine if a file is preset, readable, writable, or any
    other properties associated with files and folder
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
        Determine if the given object is a file
        """
        if os.path.isfile(self.file):
            return True
        return False

    def is_dir(self) -> bool:
        """
        Determine if the given object is a folder
        """
        if os.path.isdir(self.file):
            return True
        return False

    def is_readable(self) -> bool:
        """
        Determine if the given object is readable by the user executing the
        script
        """
        if os.access(self.file, os.R_OK):
            return True
        return False

    def is_writable(self) -> bool:
        """
        Determine if the given object is writable by the user executing the
        script
        """
        if os.access(self.file, os.W_OK):
            return True
        return False

    def is_yaml(self) -> bool:
        """
        Determine if the given object is a valid YAML object
        Sets the self.yaml property if true
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
        Determine if the given object is a valid JSON object
        Sets the self.json property if true
        """
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                self.json = json.load(f)
            return True
        except json.JSONDecodeError:
            return False
