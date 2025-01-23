#!/usr/bin/env python3
"""
MTR wrapper in Python
"""

import re
import subprocess
import sys

from src.classes.which import Which


class MTR:
    """
    MTR wrapper in Python
    """

    mtr = None
    raw_output = []
    error = {}
    ips = []
    traces = {}

    def __init__(self, ips: list) -> None:
        which = Which()
        result = which.find_command('mtr')
        if not result:
            sys.exit(1)
        self.mtr = which.command
        self.ips = ips
        for ip in self.ips:
            if not self.validate_ips(ip):
                print(f'ERROR: {ip} is not a valid IPv4 Address!')
                print(f'{ip} has been removed from the list!')
                index = self.ips.index(ip)
                self.ips.pop(index)

    def validate_ips(self, ip: str) -> bool:
        """
        Validate that the given string is a valid IPv4 Address.
        """
        pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        if re.match(pattern, ip):
            return True
        return False

    def run_mtr(self, ip: str) -> bool:
        """
        Execute the mtr binary and capture its output
        """
        cmd = [
            self.mtr, '-4', '--no-dns', '--report', '--report-cycles', '4',
            ip
        ]
        try:
            output = subprocess.run(cmd, capture_output=True, check=True)
            if output.returncode == 0:
                self.raw_output = output.stdout.decode('utf-8')
                return True
            return False
        except subprocess.CalledProcessError as e:
            self.error.update(
                {
                    'returncode': e.returncode,
                    'stdout': e.stdout,
                    'stderr': e.stderr,
                    'command': e.cmd
                }
            )
            return False

    def parse_output(self) -> list:
        """
        Parse the output from run_mtr() method
        """
        traces = []
        lines = self.raw_output.split('\n')  # type: ignore
        prematch = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        pattern = re.compile(r"""^\s+\d{1,2}\.\|\-\-\s+
        (?P<ip_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+
        (?P<loss>\d{1,3}\.\d+)\%\s+(?P<packets>\d)\s+(?P<last>\d+\.\d+)\s+
        (?P<average>\d+\.\d+)\s+(?P<best>\d+\.\d+)\s+(?P<worst>\d+\.\d+)\s+
        (?P<stdev>\d+\.\d+)$""", re.X)

        for line in lines:
            trace = {}
            result = re.search(prematch, line)
            if not result:
                continue

            matches = re.match(pattern, line)
            if not matches:
                continue

            trace.update({
                'ip_addr': matches['ip_addr'],
                'loss': float(matches['loss']),
                'sent': int(matches['packets']),
                'last': float(matches['last']),
                'average': float(matches['average']),
                'best': float(matches['best']),
                'worst': float(matches['worst']),
                'stdev': float(matches['stdev']),
            })
            traces.append(trace)

        return traces
