#!/usr/bin/env python3
"""
MTR() class file
"""

import re
import subprocess


class MTR:
    """
    Execute the mtr binary, capture its output, and parse out the key details
    per IP Address into a dictionary called a trace
    """

    IP4_PATTERN = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    def __init__(self, mtr_binary: str) -> None:
        self.mtr_binary = mtr_binary
        self.mtr_stdout = ''
        self.trace = {}
        self.error = {}

    @property
    def ip(self) -> str:
        """
        ip.getter

        :return: The IPv4 Address to execute an mtr against
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip: str) -> None:
        """
        ip.setter


        :param ip: An IPv4 Address
        :type ip: str
        :raise ValueError: If the string is not in IPv4 Address format
        :return: None
        :rtype: None
        """
        if re.match(self.IP4_PATTERN, ip):
            self._ip = ip
        else:
            raise ValueError(f'{ip} is not a valid IPv4 Address!')

    def run_mtr(self) -> bool:
        """
        Execute the mtr binary and capture its output in the self.mtr_stdout
        property

        :return: True if mtr exits with exit code 0, False if mtr exits with
        a non-zero exit code
        :rtype: bool
        """
        cmd = [
            self.mtr_binary, '-4', '--no-dns', '--report', '--report-cycles',
            '4', self.ip
        ]
        try:
            output = subprocess.run(cmd, capture_output=True, check=True)
            if output.returncode == 0:
                self.mtr_stdout = output.stdout.decode('utf-8')
                return True
            self.error.update({
                'returncode': output.returncode,
                'stdout': output.stdout.decode('utf-8'),
                'stderr': output.stderr.decode('utf-8'),
                'command': output.args
            })
            return False

        except subprocess.CalledProcessError as e:
            self.error.update({
                'returncode': e.returncode,
                'stdout': e.stdout,
                'stderr': e.stderr,
                'command': e.cmd
            })
            return False

    def parse_mtr_stdout(self) -> bool:
        """
        Parse the output in self.mtr_stdout into a dictionary and store in
        self.trace

        :return: True when parsing is complete
        :rtype: bool
        """
        lines = self.mtr_stdout.split('\n')
        prematch = re.compile(self.IP4_PATTERN.split('^', maxsplit=1)[-1])
        pattern = re.compile(
            r"""^\s+\d{1,2}\.\|\-+\s+(?P<ip_addr>\d+\.\d+\.\d+\.\d+)\s+
            (?P<loss>\d+\.\d+)\%\s+(?P<sent>\d+)\s+(?P<last>\d+\.\d+)\s+
            (?P<average>\d+\.\d+)\s+(?P<best>\d+\.\d+)\s+
            (?P<worst>\d+\.\d+)\s+(?P<stdev>\d+\.\d+)$""", re.X
        )

        for line in lines:
            result = re.search(prematch, line)
            if not result:
                continue

            matches = re.match(pattern, line)
            if not matches:
                continue

            self.trace[matches['ip_addr']] = {
                'loss': float(matches['loss']),
                'sent': int(matches['sent']),
                'last': float(matches['last']),
                'average': float(matches['average']),
                'best': float(matches['best']),
                'worst': float(matches['worst']),
                'stdev': float(matches['stdev'])
            }

        return True
