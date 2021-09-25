import json
import logging
import os

class Configuration:
    DEFAULT_CONFIG = "config.json.default"

    def __init__(self, config: str = DEFAULT_CONFIG):
        self._file_path = config
        self._settings = {}

    def __isValid(self, setting: list) -> bool:

        if 'token' not in setting or not setting['token']:
            return False
        if 'data_interval' not in setting or not setting['data_interval']:
            return False
        if 'diag_interval' not in setting or not setting['diag_interval']:
            return False

        return True        

    def __load(self, path: str):
        with open(path, 'r') as json_file:
            temp_settings = json.load(json_file)

            if self.__isValid(temp_settings) == False:
                raise ValueError('Invalid configuration file')

            self._settings = temp_settings

    def load(self):
        return self.__load(self._file_path)

    @property
    def settings(self):
        return self._settings

    @property
    def file(self) -> str:
        return self._file_path

    @file.setter
    def file(self, new_file: str):
        if os.path.isfile(new_file):
            try:
                self.__load(new_file)
            except Exception as e:
                raise Exception from e

            self._file_path = new_file
            logging.info('configuraiton is updated from {0}'.format(self._file_path))
        else:
            raise FileNotFoundError('file: ' + new_file + ' is not found')

    @property
    def token(self) -> str:
        return self._settings['token']

    @property
    def data_interval(self) -> int:
        return self._settings['data_interval']
    
    @property
    def diag_interval(self) -> int:
        return self._settings['diag_interval']

    @property
    def log(self) -> str:
        return self._settings['log']

