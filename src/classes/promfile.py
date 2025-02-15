#!/usr/bin/env python3
"""
PromFile() class file
"""

import os


class PromFile:
    """
    Manage the creation of folders related to Prometheus text file collection.

    This class uses both a main filepath and a temporary filepath.
    """

    REQUIRED_CONFIG_KEYS = [
        'filepath', 'temp_filepath', 'filename'
    ]

    OPTIONAL_CONFIG_KEYS = [
        'temp_filename'
    ]

    def __init__(self, config: dict) -> None:
        self.config = config
        for key, value in self.config.items():
            setattr(self, key, value)
        if 'temp_filename' not in self.config.keys():
            self.temp_filename = self.filename

    @property
    def config(self) -> dict:
        """
        config.getter

        :return: A dictionary containing the current configuration of the
        program
        :rtype: dict
        """
        return self._config

    @config.setter
    def config(self, config: dict) -> None:
        """
        config.setter

        :param config: A configuration of the current program
        :type config: dict
        :raise ValueError: If a required key is missing
        :raise ValueError: If an unknown key is present
        :raise KeyError: If a required section is missing
        :return: None
        :rtype: None
        """
        self._config = {}
        section = 'prometheus'
        try:
            # Ensure required configuration to operate is present
            for key in self.REQUIRED_CONFIG_KEYS:
                if key not in config[section].keys():
                    raise ValueError(f'{key} key is missing but is required!')

            # Ensure there aren't any unknown keys that could hurt
            # the operation
            for key in config[section].keys():
                if (key not in self.REQUIRED_CONFIG_KEYS and
                        key not in self.OPTIONAL_CONFIG_KEYS):
                    raise ValueError(
                        f'{key} key is invalid and must be removed!')

        except KeyError as e:
            raise KeyError(
                f'{section} section is missing but is required!') from e

        self._config = config[section]

    @property
    def filepath(self) -> str:
        """
        filepath.getter

        :return: The full path to the main file
        :rtype: str
        """
        return self._filepath

    @filepath.setter
    def filepath(self, filepath) -> None:
        """
        filepath.setter

        :param filepath: A relative or absolute filepath
        :type filepath: str
        :raise ValueError: If filepath is not a string
        :return: None
        :rtype: None
        """
        if not isinstance(filepath, str):
            raise ValueError(f'{filepath} is not a string!')
        self._filepath = os.path.realpath(filepath)

    @property
    def temp_filepath(self) -> str:
        """
        temp_filepath.getter

        :return: The full path to the temp file
        :rtype: str
        """
        return self._temp_filepath

    @temp_filepath.setter
    def temp_filepath(self, temp_filepath) -> None:
        """
        temp_filepath.setter

        :param filepath: A relative or absolute filepath
        :type filepath: str
        :raise ValueError: If filepath is not a string
        :return: None
        :rtype: None
        """
        if not isinstance(temp_filepath, str):
            raise ValueError(f'{temp_filepath} is not a string!')
        self._temp_filepath = os.path.realpath(temp_filepath)

    @property
    def filename(self) -> str:
        """
        filename.getter

        :return: The main filename
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename) -> None:
        """
        filename.setter

        :param filename: A name of a file
        :type filename: str
        :raise ValueError: If filename is not a string
        :return: None
        :rtype: None
        """
        if not isinstance(filename, str):
            raise ValueError(f'{filename} is not a string!')
        self._filename = filename

    @property
    def temp_filename(self) -> str:
        """
        temp_filename.getter

        :return: The temp filename
        :rtype: str
        """
        return self._temp_filename

    @temp_filename.setter
    def temp_filename(self, temp_filename) -> None:
        """
        temp_filename.setter

        :param filename: A name of a file
        :type filename: str
        :raise ValueError: If filename is not a string
        :return: None
        :rtype: None
        """
        if not isinstance(temp_filename, str):
            raise ValueError(f'{temp_filename} is not a string!')
        self._temp_filename = temp_filename

    def create_filepath(self) -> bool:
        """
        Create the folder from self.filepath

        :return: True if folder is created or already exists,
        False if not created
        :rtype: bool
        """
        try:
            os.mkdir(self.filepath, mode=0o755)
            return True
        except FileExistsError:
            # This indicates the folder already exists
            return True
        except FileNotFoundError:
            # This indicates that a folder in the path, a parent folder,
            # does not exist
            print(f'Parent directory not found in {self.filepath}!')
            return False
        except PermissionError:
            # The user running the script does not have permissions to
            # create a new folder in this path
            print(f'Permission denied while creating {self.filepath}!')
            return False

    def create_temp_filepath(self) -> bool:
        """
        Create the folder from self.temp_filepath

        :return: True if folder is created or already exists,
        False if not created
        :rtype: bool
        """
        try:
            os.mkdir(self.temp_filepath, mode=0o755)
            return True
        except FileExistsError:
            # This indicates the folder already exists
            return True
        except FileNotFoundError:
            # This indicates that a folder in the path, a parent folder,
            # does not exist
            print(f'Parent directory not found in {self.temp_filepath}!')
            return False
        except PermissionError:
            # The user running the script does not have permissions to
            # create a new folder in this path
            print(f'Permission denied while creating {self.temp_filepath}!')
            return False
