#!/usr/bin/env python3
"""
Unit Tests for the PromFile() class
"""

import unittest

from unittest.mock import patch

from src.classes.promfile import PromFile
from src.constants import constants


class TestPromFile(unittest.TestCase):
    """
    Unit Tests for the PromFile() class
    """

    def setUp(self) -> None:
        self.promfile = PromFile(constants.CONFIG_FILE)
        return super().setUp()

    def tearDown(self) -> None:
        del self.promfile
        return super().tearDown()

    def test_bad_file(self) -> None:
        """Test that all config values are blank when a bad file is passed"""
        file = 'fjeijwiefjaweifj;awiejf'
        with self.assertRaises(SystemExit):
            promfile = PromFile(file)
            self.assertIsNone(promfile.filepath)
            self.assertIsNone(promfile.temp_filepath)
            self.assertIsNone(promfile.filename)
            self.assertIsNone(promfile.temp_filename)

    def test_file_unreadable(self) -> None:
        """
        Test that all config values are blank when an unreadable file is
        passed
        """
        file = '/swapfile'
        with self.assertRaises(ValueError):
            promfile = PromFile(file)
            self.assertIsNone(promfile.filepath)
            self.assertIsNone(promfile.temp_filepath)
            self.assertIsNone(promfile.filename)
            self.assertIsNone(promfile.temp_filename)

    def test_file_not_yaml(self) -> None:
        """
        Test that all config values are blank when an invalid YAML file
        is passed
        """
        file = './README.md'
        with self.assertRaises(ValueError):
            promfile = PromFile(file)
            self.assertIsNone(promfile.filepath)
            self.assertIsNone(promfile.temp_filepath)
            self.assertIsNone(promfile.filename)
            self.assertIsNone(promfile.temp_filename)

    def test_filepath(self) -> None:
        """Test filepath is what we expect"""
        self.assertIsInstance(self.promfile.filepath, str)
        self.assertEqual(self.promfile.filepath, '/var/prometheus')

    def test_temp_filepath(self) -> None:
        """Test temp_filepath is what we expect"""
        self.assertIsInstance(self.promfile.temp_filepath, str)
        self.assertEqual(self.promfile.temp_filepath, '/tmp/prometheus')

    def test_filename(self) -> None:
        """Test filename is what we expect"""
        self.assertIsInstance(self.promfile.filename, str)
        self.assertEqual(self.promfile.filename, 'ping_stats.prom')

    def test_temp_filename(self) -> None:
        """Test temp_filename is what we expect"""
        self.assertIsInstance(self.promfile.temp_filename, str)
        self.assertEqual(self.promfile.temp_filename, '')

    @patch('src.classes.promfile.os.mkdir', side_effect=FileNotFoundError)
    def test_create_filepath_failed_missing_parent_directory(
            self, mock) -> None:
        """Assert failed when parent directory is missing in filepath"""
        result = self.promfile.create_filepath()
        self.assertTrue(mock.called)
        self.assertFalse(result)

    @patch('src.classes.promfile.os.mkdir', side_effect=PermissionError)
    def test_create_filepath_failed_permission_denied(
            self, mock) -> None:
        """Assert failed when user is not a privileged user"""
        result = self.promfile.create_filepath()
        self.assertTrue(mock.called)
        self.assertFalse(result)

    @patch('src.classes.promfile.os.mkdir', side_effect=FileExistsError)
    def test_create_filepath_filepath_already_exists(
            self, mock) -> None:
        """Assert true when filepath already exists"""
        result = self.promfile.create_filepath()
        self.assertTrue(mock.called)
        self.assertTrue(result)

    @patch('src.classes.promfile.os.mkdir')
    def test_create_filepath(self, mock) -> None:
        """Assert true on new creation"""
        result = self.promfile.create_filepath()
        self.assertTrue(mock.called)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
