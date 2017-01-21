# -*- coding: utf8 -*-

from easytest import Test
from test_input.temperature import TEST_TEMPERATURE_MODE
from test_input.humidity import TEST_HUMIDITY_MODE

t = Test()
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)

t.calculate()

t.path = 'tests/test_1.json'

t.save()

print('Calculated and saved to:', t.path)


# TEMPLATE
from report.builder import ReportBuilder

report_path = r'C:\Users\2065\Desktop\easytest2\reports'  # ask user every time

builder = ReportBuilder(t, report_path)

builder.build_additions()
builder.build_main()

print('Reports created.')