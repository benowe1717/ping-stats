#!/usr/bin/env python3
"""
Gather statistics about all IPs in your route to a destination
"""

import sys
import yaml

from src.classes.parseargs import ParseArgs
from src.constants import constants


def main() -> int:
    """Main program loop"""
    args = sys.argv
    parseargs = ParseArgs(args)
    config_file = get_config_file(parseargs)

    return 0


def get_config_file(parseargs: ParseArgs) -> str:
    """
    Find the config_file and set it

    :param parseargs: The reference to the current ParseArgs class
    :type parseargs: ParseArgs
    :return: The full filepath to the config file if given by the user or
    the default config file
    :rtype: str
    """
    if parseargs.config_file:
        return parseargs.config_file
    return constants.CONFIG_FILE


def read_config_file(config_file: str) -> dict:
    """
    Read the YAML config file and return a dictionary

    :param config_file: The full filepath and filename to a YAML config file
    :type config_file: str
    :return: A dictionary containing the data from the YAML file
    :rtype: dict
    """
    with open(config_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return data


if __name__ == '__main__':
    RESULT = main()
    if RESULT != 0:
        sys.exit(1)
    sys.exit(0)
