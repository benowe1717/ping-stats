#!/usr/bin/env python3
"""Wrapper for the argparse library"""
import argparse
import re

from src.constants import constants


class ParseArgs():
    NAME = constants.ARGPARSE_PROGRAM_NAME
    DESC = constants.ARGPARSE_PROGRAM_DESCRIPTION
    VERSION = constants.ARGPARSE_VERSION
    AUTHOR = constants.ARGPARSE_AUTHOR
    REPO = constants.ARGPARSE_REPO

    def __init__(self, args) -> None:
        self.args = args
        self.parser = argparse.ArgumentParser(
            prog=self.NAME, description=self.DESC)
        self.ips = []

        self.parser.add_argument(
            '-v',
            '--version',
            action='store_true',
            required=False,
            help='Show this program\'s current version')

        self.parser.add_argument(
            '-i',
            '--ips',
            nargs='+',
            required=False,
            help='The IP Addresses you want to monitor')

        self.parse_args = self.parser.parse_args()

        if len(self.args) == 1:
            self.parser.print_help()
            self.parser.exit()

        if self.parse_args.version:
            self._print_version()
            self.parser.exit()

        if self.parse_args.ips:
            self.ips = self._sanitize_ips()

    def _print_version(self) -> None:
        print(f'{self.NAME} v{self.VERSION}')
        print(
            'This is free software:',
            'you are free to change and redistribute it.')
        print('There is NO WARARNTY, to the extent permitted by law.')
        print(f'Written by {self.AUTHOR}; see below for original code')
        print(f'<{self.REPO}')

    def _sanitize_ips(self) -> list:
        """
        Sanitizes the user's input into a normalized list
        ['1.1.1.1,1.0.0.1,8.8.8.8']
        ['1.1.1.1,', '1.0.0.1,', '8.8.8.8']
        ['1.1.1.1', '1.0.0.1', '8.8.8.8']

        All inputs will be normalized into
        ['1.1.1.1', '1.0.0.1', '8.8.8.8']
        """
        normalized = []
        inputs = []
        for i in self.parse_args.ips:
            splits = i.split(',')
            inputs.append(splits)

        pattern = r'^\d+\.\d+\.\d+\.\d+$'
        findall_pattern = r'\d+\.\d+\.\d+\.\d+'
        for i in inputs:
            for ii in i:
                if ii != '':
                    if not re.match(pattern, ii):
                        matches = re.findall(findall_pattern, ii)
                        for match in matches:
                            normalized.append(match.strip())
                    else:
                        normalized.append(ii.strip())
        return normalized
