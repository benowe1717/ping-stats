#!/usr/bin/env python3
"""
Ensure the proper Prometheus directories are present along with
creating the relevant .prom file
"""

import os

from src.classes.file_checker import FileChecker


class PromFile:
    """
    Ensure the proper Prometheus directories are present along with
    creating the relevant .prom file
    """

    REQUIRED_CONFIG_KEYS = [
        'filepath', 'temp_filepath', 'filename'
    ]

    OPTIONAL_CONFIG_KEYS = [
        'temp_filename'
    ]

    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self._filepath = ''
        self._temp_filepath = ''
        self._filename = ''
        self._temp_filename = ''
        self._parse_config()

    @property
    def config(self) -> dict:
        """
        Property config: dict
        """
        return self._config

    @config.setter
    def config(self, data: dict) -> None:
        """
        config.setter
        """
        self._config = {}
        section = 'prometheus'
        try:
            for key in self.REQUIRED_CONFIG_KEYS:
                if key not in data[section].keys():
                    raise KeyError(f'{key} is missing but is required!')

            for key in data[section].keys():
                if (key not in self.REQUIRED_CONFIG_KEYS and
                        key not in self.OPTIONAL_CONFIG_KEYS):
                    raise KeyError(f'{key} is invalid and should be removed!')

            self._config_file = data[section]
        except KeyError as e:
            raise KeyError(
                f'{section} section is missing but is required!') from e

    @property
    def config_file(self) -> str:
        """
        Property config_file: str
        """
        return self._config_file

    @config_file.setter
    def config_file(self, file: str) -> None:
        """
        config_file.setter
        """
        self._config_file = ''
        fc = FileChecker(file)
        if not fc.is_file():
            raise ValueError(f'{fc.file} is not a file!')

        if not fc.is_readable():
            raise ValueError(f'{fc.file} is not readable!')

        if not fc.is_yaml():
            raise ValueError(f'{fc.file} is not in YAML format!')

        self._config_file = fc.file
        self._config = fc.yaml

    @property
    def filepath(self) -> str:
        """
        Property filepath: str
        """
        return self._filepath

    @property
    def temp_filepath(self) -> str:
        """
        Property temp_filepath: str
        """
        return self._temp_filepath

    @property
    def filename(self) -> str:
        """
        Property filename: str
        """
        return self._filename

    @property
    def temp_filename(self) -> str:
        """
        Property temp_filename: str
        """
        return self._temp_filename

    def _parse_config(self) -> None:
        """
        Parse the given config and validate all values
        """
        section = 'prometheus'
        try:
            for key, value in self.config[section].items():
                class_key = f'_{key}'
                setattr(self, class_key, value)

        except KeyError as e:
            raise KeyError(
                f'{section} section is missing but is required!') from e

    def create_filepath(self) -> bool:
        """
        Create the folder from self.filepath
        """
        try:
            os.mkdir(self.filepath, mode=0o755)
            return True
        except FileExistsError:
            return True
        except FileNotFoundError:
            print(f'Parent directory not found in {self.filepath}!')
            return False
        except PermissionError:
            print('Permission denied!')
            return False

    def create_temp_filepath(self) -> bool:
        """
        Create the folder from self.temp_filepath
        """
        try:
            os.mkdir(self.filepath, mode=0o755)
            return True
        except FileExistsError:
            return True
        except FileNotFoundError:
            print(f'Parent directory not found in {self.temp_filepath}!')
            return False
        except PermissionError:
            print('Permission denied!')
            return False
