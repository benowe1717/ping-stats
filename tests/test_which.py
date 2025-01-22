#!/usr/bin/env python3
"""
Unit Tests for the Which() class
"""

import unittest

from src.classes.which import Which


class TestWhich(unittest.TestCase):
    """
    Unit Tests for the Which() class
    """

    def test_find_command(self):
        """Ensure a command is found with a standard binary."""
        which = Which()
        self.assertTrue(which.find_command('ls'))

    def test_find_command_failed(self):
        """Ensure the method returns False when given gibberish
        or non-existing commands."""
        which = Which()
        self.assertFalse(which.find_command('abcdefg'))


if __name__ == '__main__':
    unittest.main()
