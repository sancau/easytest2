# -*- coding: utf8 -*-

from easytest import Test
from test_input.temperature import TEST_TEMPERATURE_MODE
from test_input.humidity import TEST_HUMIDITY_MODE

t = Test()  # user creates TEST

# user adds modes and log files
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)

# user adds report data
t.data['specialist'] = 'Татчин А.В.'
t.data['tools'] = [  # tools data
    'GTH 5050',
    'Гидрометр ФЫ-2'
]
t.data['system'] = {  # system info
    'name': 'Votsch 7250',
    'year_of_production': '2013',
    'manufacturer': 'Votsch, Германия',
    'factory_number': '90123XXASAC123',
    'description': 'Повышенная и пониженная температура от -80 до +180С, пониженная и повышеннвя влажность от 25% до 98%',
    'test_program': 'Программа аттестации Votsch 7250 от 12 ноября 2013 года',
    'test_method': 'Методика аттестации Votsch 7250 (ГОСТ 34512)',
}

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
