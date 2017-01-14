# -*- coding: utf8 -*-

from easytest import Test
from test_input.temperature import TEST_TEMPERATURE_MODE
from test_input.humidity import TEST_HUMIDITY_MODE

t = Test()
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)

t.calculate()

t.path = 'tests/test_1.json'

t.save()

print('Calculated and saved to:', t.path)
