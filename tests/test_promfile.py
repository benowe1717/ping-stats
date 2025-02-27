#!/usr/bin/env python3
"""
Unit Tests for the PromFile() class
"""

import os
import unittest

from unittest.mock import patch

from src.classes.promfile import PromFile


class TestPromFile(unittest.TestCase):
    """
    Unit Tests for the PromFile() class
    """

    def setUp(self) -> None:
        self.config = {
            'prometheus': {
                'filepath': './data/var/prometheus',
                'temp_filepath': 'data/tmp/prometheus',
                'filename': 'ping-stats.prom'
            }
        }
        self.promfile = PromFile(self.config)
        return super().setUp()

    def tearDown(self) -> None:
        del self.config
        del self.promfile
        return super().tearDown()

    def test_missing_config_section(self) -> None:
        """
        Assert raise KeyError when 'prometheus' key is missing in config
        dict
        """
        config = {
            'mtr': {
                'ips': [
                    '1.1.1.1'
                ]
            }
        }
        with self.assertRaises(KeyError):
            PromFile(config)

    def test_missing_config_key(self) -> None:
        """
        Assert raise ValueError when one of any required keys is missing
        in config dict
        """
        config = {
            'prometheus': {
                'filepath': './data/var/prometheus'
            }
        }
        with self.assertRaises(ValueError):
            PromFile(config)

    def test_invalid_key_in_config(self) -> None:
        """
        Assert raise ValueError when an unknown key exists in config dict
        """
        self.config['prometheus'].update({'invalid': 'something'})
        with self.assertRaises(ValueError):
            PromFile(self.config)

    def test_valid_config_no_temp_filename(self) -> None:
        """
        Assert config is valid when all required keys are passed
        """
        self.assertEqual(
            self.promfile.filepath,
            os.path.realpath(self.config['prometheus']['filepath'])
        )
        self.assertEqual(
            self.promfile.filename,
            self.config['prometheus']['filename']
        )
        self.assertEqual(
            self.promfile.temp_filepath,
            os.path.realpath(self.config['prometheus']['temp_filepath'])
        )
        self.assertEqual(
            self.promfile.temp_filename,
            self.config['prometheus']['filename']
        )

    def test_valid_config_temp_filename_given(self) -> None:
        """
        Assert config is valid when all required keys are passed and the
        optional temp_filename key is passed
        """
        self.config['prometheus'].update({
            'temp_filename': 'temp-ping-stats.prom'
        })
        promfile = PromFile(self.config)
        self.assertEqual(
            promfile.filepath,
            os.path.realpath(self.config['prometheus']['filepath'])
        )
        self.assertEqual(
            promfile.filename,
            self.config['prometheus']['filename']
        )
        self.assertEqual(
            promfile.temp_filepath,
            os.path.realpath(self.config['prometheus']['temp_filepath'])
        )
        self.assertEqual(
            promfile.temp_filename,
            self.config['prometheus']['temp_filename']
        )

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
