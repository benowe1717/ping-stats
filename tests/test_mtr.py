#!/usr/bin/env python3
"""
Unit Tests for the MTR() class
"""

from subprocess import CalledProcessError, CompletedProcess
import unittest

from unittest.mock import patch

from src.classes.mtr import MTR


class TestMTR(unittest.TestCase):
    """
    Unit Tests for the MTR() class
    """

    ips = ['1.1.1.1']

    def setUp(self) -> None:
        self.mtr = MTR(self.ips)
        return super().setUp()

    def tearDown(self) -> None:
        del self.mtr
        return super().tearDown()

    def test_validate_ips_failed_ipv6(self):
        """Ensure an IPv6 string doesn't work"""
        ipv6 = 'fe80::a4f2:7f33:f8cd:6a0b'
        self.assertFalse(self.mtr.validate_ips(ipv6))

    def test_validate_ips_failed_typo_ipv4(self):
        """Ensure a typo'd IPv4 string doesn't work"""
        ipv4 = '1.1.11'
        self.assertFalse(self.mtr.validate_ips(ipv4))

    def test_validate_ips(self):
        """Ensure a properly formatted IPv4 string works"""
        ipv4 = '74.125.138.138'
        self.assertTrue(self.mtr.validate_ips(ipv4))

    @patch('src.classes.mtr.subprocess.run', side_effect=CalledProcessError(
        **{
            'returncode': 1,
            'cmd': '/usr/bin/mtr --reprt --report-cyles 4 1.1.1.1',
            'stderr': '/usr/bin/mtr: unrecognized option',
        }
    ))
    def test_run_mtr_failed_raised_error(self, mock):
        """Mock a subprocess.run call that raises the CalledProcessError"""
        result = self.mtr.run_mtr(self.ips[0])
        self.assertTrue(mock.called)
        self.assertFalse(result)
        self.assertRaises(CalledProcessError)
        self.assertEqual(self.mtr.error, {
            'returncode': 1,
            'command': '/usr/bin/mtr --reprt --report-cyles 4 1.1.1.1',
            'stdout': None,
            'stderr': '/usr/bin/mtr: unrecognized option',
        })

    @patch('src.classes.mtr.subprocess.run')
    def test_run_mtr(self, mock):
        """Mock a subprocess.run call that is successful"""
        mock.return_value = CompletedProcess(**{
            'returncode': 0,
            'args': '/usr/bin/mtr --report --report-cycles 4 1.1.1.1',
            'stdout': b'Start\n',
            'stderr': None,
        })
        result = self.mtr.run_mtr(self.ips[0])
        self.assertTrue(mock.called)
        self.assertTrue(result)
        self.assertEqual(self.mtr.raw_output, 'Start\n')

    def test_parse_output_no_matching_lines(self):
        """If no regex matches, ensure we get an empty result"""
        output = 'This does not work\n'
        self.mtr.raw_output = output
        self.assertEqual(self.mtr.parse_output(), [])

    def test_parse_output_one_matching_line(self):
        """When only one line is matching in a list of multiple
        ensure only that line is present in the results"""
        output = 'Start: 2025-01-23T16:48:05-0500\n'
        output += """
HOST: benjaminz-thinkpad          Loss%   Snt   Last   Avg  Best  Wrst StDev\n
        """
        output += """
  1.|-- 10.10.28.1                 0.0%     4    5.8  11.9   5.8  16.8   5.6\n
        """
        self.mtr.raw_output = output
        self.assertEqual(self.mtr.parse_output(), [{
            'ip_addr': '10.10.28.1',
            'loss': 0.0,
            'sent': 4,
            'last': 5.8,
            'average': 11.9,
            'best': 5.8,
            'worst': 16.8,
            'stdev': 5.6
        }])

    def test_parse_output(self):
        """Get a consistently parsed output"""
        output = 'Start: 2025-01-23T16:48:05-0500\n'
        output += """
HOST: benjaminz-thinkpad          Loss%   Snt   Last   Avg  Best  Wrst StDev\n
        """
        output += """
  1.|-- 10.10.28.1                 0.0%     4    5.8  11.9   5.8  16.8   5.6\n
        """
        output += """
  2.|-- 192.168.1.254              0.0%     4    8.5  10.9   8.5  14.4   2.6\n
        """
        self.mtr.raw_output = output
        self.assertEqual(self.mtr.parse_output(), [
            {
                'ip_addr': '10.10.28.1',
                'loss': 0.0,
                'sent': 4,
                'last': 5.8,
                'average': 11.9,
                'best': 5.8,
                'worst': 16.8,
                'stdev': 5.6
            },
            {
                'ip_addr': '192.168.1.254',
                'loss': 0.0,
                'sent': 4,
                'last': 8.5,
                'average': 10.9,
                'best': 8.5,
                'worst': 14.4,
                'stdev': 2.6
            },
        ])


if __name__ == '__main__':
    unittest.main()
