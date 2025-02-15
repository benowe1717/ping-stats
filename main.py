#!/usr/bin/env python3
"""
Gather statistics about all IPs in your route to a destination
"""

import concurrent.futures
import os
import sys
import yaml

from src.classes.mtr import MTR
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

    try:
        ips = config['mtr']['ips']

    except KeyError as e:
        print(e)
        return -1

    traces = []
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=len(ips)) as executor:
        future_to_ip = {
            executor.submit(
                run_mtr,
                mtr_binary,
                ip): ip for ip in ips}
        for future in concurrent.futures.as_completed(future_to_ip):
            data = future.result()
            traces.append(data)

    combined_traces = combine_traces(traces)
    averaged_traces = average_traces(combined_traces)

    result = write_prometheus_file(config, averaged_traces)
    if not result:
        return -1

    result = move_prometheus_file(config)
    if not result:
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


def run_mtr(mtr_binary: str, ip: str) -> dict:
    """
    Using the MTR() class, run a traceroute to the given IP Address using the
    given mtr binary and return the formatted trace

    :param mtr_binary: The full filepath to the mtr binary
    :type mtr_binary: str
    :param ip: The IPv4 Address to provide to the mtr binary
    :type ip: str
    :return: The trace dictionary if the trace was successful,
    an empty dictionary if the trace failed
    :rtype: dict
    """
    mtr = MTR(mtr_binary)
    mtr.ip = ip
    result = mtr.run_mtr()
    if not result:
        return {}

    result = mtr.parse_mtr_stdout()
    if not result:
        return {}

    return mtr.trace


def combine_traces(traces: list) -> dict:
    """
    Take in a list of dicts, where the list represents all traces, and each
    item in the list is a trace represented in dictionary format.
    Return a dictionary where each key represents a unique IP and
    contains all values from all traces against that IP

    :param traces: The list of traces
    :type traces: list
    :return: A dictionary containing each combined trace
    :rtype: dict
    """
    combined_traces = {}
    for trace in traces:
        for ip_addr, values in trace.items():
            if ip_addr not in combined_traces:
                combined_traces.update({ip_addr: {}})

            for key, value in values.items():
                try:
                    combined_traces[ip_addr][key].append(value)
                except KeyError:
                    combined_traces[ip_addr][key] = [value]

    return combined_traces


def average_traces(traces: dict) -> dict:
    """
    Iterate over each trace, represented by a dictionary, and average out
    all values

    :param traces: A dictionary of all traces
    :type traces: dict
    :return: A dictionary of all traces with averaged values
    :rtype: dict
    """
    for _, values in traces.items():
        for key, value in values.items():
            average = round(sum(value) / len(value), 1)
            values[key] = average
    return traces


def write_prometheus_file(config: dict, traces: dict) -> bool:
    """
    Write dicts to prometheus-formatted file for collection

    :param config: The current configuration
    :type config: dict
    :param traces: A dictionary of all traces
    :type traces: dict
    :return: True if temp file was successfully created and written to,
    False if the file could not be created or opened for writing
    :rtype: bool
    """
    promfile = PromFile(config)
    tempfile = os.path.join(promfile.temp_filepath, promfile.temp_filename)

    lines = []
    for ip_addr, objs in traces.items():
        for name, value in objs.items():
            items = [
                'ping_stats{ip_addr="', ip_addr, '", stat="', name,
                '"} ', str(value)
            ]
            lines.append(''.join(items))

    try:
        with open(tempfile, 'w', encoding='utf-8') as file:
            file.write('\n'.join(lines))
            file.write('\n')
        return True

    except PermissionError as e:
        print(e)
        return False

    except OSError as e:
        print(e)
        return False


def move_prometheus_file(config: dict) -> bool:
    """
    Move the temp prometheus file to the primary location

    :param config: The current configuration
    :type config: dict
    :return: True if the temp file was successfully moved to the main file,
    False if the temp file could not replace the main file
    :rtype: bool
    """
    promfile = PromFile(config)
    tempfile = os.path.join(promfile.temp_filepath, promfile.temp_filename)
    mainfile = os.path.join(promfile.filepath, promfile.filename)

    try:
        os.replace(tempfile, mainfile)
        return True
    except OSError as e:
        print(e)
        return False


if __name__ == '__main__':
    RESULT = main()
    if RESULT != 0:
        sys.exit(1)
    sys.exit(0)
