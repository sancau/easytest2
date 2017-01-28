# -*- coding: utf8 -*-

from collections import namedtuple

from easytest import Test
from report.builder import ReportBuilder

LogDescriptions = namedtuple('LogDescriptions', ['DT1', 'DT2', 'KT'])
DESC = LogDescriptions('DT1', 'DT2', 'KT')


t = Test()  # user creates TEST

# user adds modes and log files
TEST_HUMIDITY_MODE = {
    'logs': [
        {
            'file': 'test_data/humidity/1.xlsx',
            'desc': DESC.DT1
        },
        {
            'file': 'test_data/humidity/2.xlsx',
            'desc': DESC.DT2
        },
        {
            'file': 'test_data/humidity/2.xlsx',
            'desc': DESC.KT
        }
    ],
    'target': {
        'humidity': 90,
        'temperature': 25
    },
    'md': {
        'humidity': [90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
        'temperature': [25, 25, 25, 25, 25, 25, 25, 25, 25, 25]
    }
}

# user adds modes and log files
TEST_TEMPERATURE_MODE = {
    "target": "0",
    "logs": [
        {
            "file": "test_data/0_left.txt",
            "sensors_count": "8",
        },
        {
            "file": "test_data/0_right.txt",
            "sensors_count": "8"
        }
    ],
    "cp": [
        "0", "0", "0", "0", "0",
        "0", "0", "0", "0", "0"
    ],
    "md": [
        "0.2", "0", "0", "0", "0",
        "0", "0.3", "0.2", "0", "0.1"
    ]
}

# user adds modes to the test object
t.add_temperature_mode(TEST_TEMPERATURE_MODE)
t.add_humidity_mode(TEST_HUMIDITY_MODE)

# user adds report data
t.data['specialist'] = 'Татчин А.В.'

# user adds tools data
t.data['tools'] = [  # tools data
    'GTH 5050',
    'Гидрометр ФЫ-2'
]

# user adds system data
t.data['system'] = {  # system info
    'name': 'Votsch 7250',
    'year_of_production': '2013',
    'manufacturer': 'Votsch, Германия',
    'factory_number': '90123XXASAC123',
    'description': 'Повышенная и пониженная температура от -80 до +180С, пониженная и повышеннвя влажность от 25% до 98%',
    'test_program': 'Программа аттестации Votsch 7250 от 12 ноября 2013 года',
    'test_method': 'Методика аттестации Votsch 7250 (ГОСТ 34512)',
}


t.calculate()  # invoking test calculation logic

# user can save test to file and reload it from the file
t.path = 'tests/test_1.json'
t.save()
print('Calculated and saved to:', t.path)


# TEMPLATE

# user specifies output path for report
report_path = r'C:\Users\2065\Desktop\easytest2\reports'  # ask user every time


# user can generate report files in MS WORD format
def make_report():
    builder = ReportBuilder(t, report_path)
    builder.build_additions()
    builder.build_main()

make_report()

print('Reports created.')
