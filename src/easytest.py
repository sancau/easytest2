# -*- coding: utf8 -*-

import json

from datetime import datetime

from temperature.interface import TemperatureModeHandler

from settings import DEFAULT_TEST
from validators import validate_temperature_mode
from validators import validate_test_settings
from utils import json_handler


class Test:
    def __init__(self, path=None):
        self.data = DEFAULT_TEST
        self.path = path

        if self.path:
            try:
                with open(self.path, 'r', encoding='UTF8') as data_file:
                    string_data = data_file.read()
                    self.data = json.loads(string_data)
            except Exception as e:
                print(e)
    
    def calculate(self):  # calculates/recalculates all modes in the test
        modes = {
            'humidity': lambda x: {'test': 42},  # TODO
            'temperature': TemperatureModeHandler().handle
        }

        for mode_type, handler in modes.items():
            for index, mode in enumerate(self.data[mode_type]):
                this = self.data[mode_type][index]
                self.data[mode_type][index] = handler(this)  

    def create_report(self):
        raise NotImplementedError('This method is not implemented yet')

    def save_as(self, path):  # saves the test object as json to given path
        with open(path, 'w+', encoding='UTF8') as data_file:
            json_data = json.dumps(self.data, 
                                   ensure_ascii=False, 
                                   sort_keys=True,
                                   default=json_handler,
                                   indent=2)
            data_file.write(json_data)
        self.path = path

    def save(self):  # saves objects that has path as json
        if not self.path:
            print('No file path to save to')
            return
        else:
            self.save_as(self.path)

    def edit_test_settings(self, settings):  # updates test global settings
        errors = validate_test_settings(settings)
        if not errors:
            self.data['settings'].append(settings)
        else:
            print('Validation errors:', errors)
 
    def add_temperature_mode(self, mode):  # adds a temperature mode to the test
        errors = validate_temperature_mode(mode)
        if not errors:
            mode.update(self.data['settings']['temperature'])  # add settings
            self.data['temperature'].append(mode)
        else:
            print('Validation errors:', errors)

    def add_humidity_mode(self, mode):  # adds a humidity mode to the test
        raise NotImplementedError('This method is not implemented yet')
