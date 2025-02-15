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

    def setUp(self) -> None:
        self.ip = '1.1.1.1'
        self.mtr_binary = '/usr/bin/mtr'
        self.mtr = MTR(self.mtr_binary)
        return super().setUp()

    def tearDown(self) -> None:
        del self.mtr
        del self.mtr_binary
        del self.ip
        return super().tearDown()

    def test_set_ip_to_ipv6_fails(self) -> None:
        """
        Assert raises ValueError when IPv6 is used
        """
        ipv6 = 'fe80::a4f2:7f33:f8cd:6a0b'
        with self.assertRaises(ValueError):
            self.mtr.ip = ipv6

    def test_set_ip_to_random_string_fails(self) -> None:
        """
        Assert raises ValueError when random string is used
        """
        ip = 'some random ip goes here'
        with self.assertRaises(ValueError):
            self.mtr.ip = ip

    def test_set_ip_to_typod_ipv4_fails(self) -> None:
        """
        Assert raises ValueError when typod ipv4 address is used
        """
        ipv4 = '1.1.11'
        with self.assertRaises(ValueError):
            self.mtr.ip = ipv4

    def test_set_ip(self) -> None:
        """
        Assert setting ip to ipv4 address works
        """
        self.mtr.ip = self.ip
        self.assertEqual(self.mtr.ip, self.ip)

    @patch('src.classes.mtr.subprocess.run', side_effect=CalledProcessError(
        **{
            'returncode': 1,
            'cmd': '/usr/bin/mtr --reprt --report-cyles 4 1.1.1.1',
            'stderr': '/usr/bin/mtr: unrecognized option',
        }
    ))
    def test_run_mtr_failed_raised_error(self, mock):
        """Mock a subprocess.run call that raises the CalledProcessError"""
        self.mtr.ip = self.ip
        result = self.mtr.run_mtr()
        self.assertTrue(mock.called)
        self.assertFalse(result)
        self.assertRaises(CalledProcessError)
        self.assertEqual(self.mtr.mtr_stdout, '')
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
        self.mtr.ip = self.ip
        result = self.mtr.run_mtr()
        self.assertTrue(mock.called)
        self.assertTrue(result)
        self.assertEqual(self.mtr.mtr_stdout, 'Start\n')

    def test_parse_output_no_matching_lines(self):
        """If no regex matches, ensure we get an empty result"""
        output = 'This does not work\n'
        self.mtr.mtr_stdout = output
        self.assertEqual(self.mtr.trace, {})

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
        self.mtr.mtr_stdout = output
        self.mtr.parse_mtr_stdout()
        self.assertEqual(self.mtr.trace, {
            '10.10.28.1': {
                'loss': 0.0,
                'sent': 4,
                'last': 5.8,
                'average': 11.9,
                'best': 5.8,
                'worst': 16.8,
                'stdev': 5.6
            }
        })

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
        self.mtr.mtr_stdout = output
        self.mtr.parse_mtr_stdout()
        self.assertEqual(self.mtr.trace, {
            '10.10.28.1': {
                'loss': 0.0,
                'sent': 4,
                'last': 5.8,
                'average': 11.9,
                'best': 5.8,
                'worst': 16.8,
                'stdev': 5.6
            }, '192.168.1.254': {
                'loss': 0.0,
                'sent': 4,
                'last': 8.5,
                'average': 10.9,
                'best': 8.5,
                'worst': 14.4,
                'stdev': 2.6
            }
        })


if __name__ == '__main__':
    unittest.main()
