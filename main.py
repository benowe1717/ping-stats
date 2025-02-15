#!/usr/bin/env python3
"""
Gather statistics about all IPs in your route to a destination
"""

import sys
import yaml

from src.classes.parseargs import ParseArgs
from src.classes.promfile import PromFile
from src.classes.which import Which
from src.constants import constants


def main() -> int:
    """Main program loop"""
    args = sys.argv
    parseargs = ParseArgs(args)
    config_file = get_config_file(parseargs)
    config = read_config_file(config_file)
    result = prometheus_setup(config)
    if not result:
        return -1

    mtr_binary = find_mtr()
    if not mtr_binary:
        return -1

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


def prometheus_setup(config: dict) -> bool:
    """
    Ensure all required Prometheus directories are present and create them
    if they are not present

    :param config: A dictionary containing the current configuration
    :type config: dict
    :return: True if all Prometheus directories are present,
    False if directories are not present
    :rtype: bool
    """
    try:
        promfile = PromFile(config)

        result = promfile.create_filepath()
        if not result:
            return False

        result = promfile.create_temp_filepath()
        if not result:
            return False

        return True

    except KeyError as e:
        print(e)
        return False

    except ValueError as e:
        print(e)
        return False


def find_mtr() -> str:
    """
    Attempt to locate the full filepath to the mtr binary

    :return: The full filepath to the mtr binary, or empty if the binary
    cannot be located
    :rtype: str
    """
    which = Which()
    result = which.find_command('mtr')
    if not result:
        return ''
    return which.command


if __name__ == '__main__':
    RESULT = main()
    if RESULT != 0:
        sys.exit(1)
    sys.exit(0)
