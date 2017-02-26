# -*- coding: utf8 -*-

from collections import namedtuple

from bl.easytest import Test
from bl.report.builder import ReportBuilder

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
tmodes = [
    {
        "target": "0",
        "logs": [
            {
                "file": r"test_data/data/0 ПТСВ (1 вариант).txt",
                "sensors_count": "7",
            },
            {
                "file": r"test_data/data/0 ТСП (1 вариант).txt",
                "sensors_count": "7"
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
    },  # OK
    {
        "target": "25",
        "logs": [
            {
                "file": r"test_data/data/25 ПТСВ (1 вариант).txt",
                "sensors_count": "7",
            },
            {
                "file": r"test_data/data/25 ТСП (2 вариант).txt",
                "sensors_count": "7"
            }
        ],
        "cp": [
            "25", "25.1", "25", "25", "25",
            "25", "25", "25", "25", "25"
        ],
        "md": [
            "25.1", "25", "25", "25", "25",
            "25", "25.2", "25.1", "25", "25"
        ]
    },  # OK
    {
        "target": "40",
        "logs": [
            {
                "file": r"test_data/data/40 ПТСВ (2 вариант) !!!!!.txt",
                "sensors_count": "7",
            },
            {
                "file": r"test_data/data/40 ТСП (1 вариант).txt",
                "sensors_count": "7"
            }
        ],
        "cp": [
            "40", "40", "40.1", "40", "40",
            "40", "40", "40", "40.1", "40"
        ],
        "md": [
            "40.2", "40", "40", "40", "39.9",
            "40", "40.1", "40", "40", "40"
        ]
    },  # OK
    {
        "target": "60",
        "logs": [
            {
                "file": r"test_data/data/60 ПТСВ (4 вариант) !!!!!.txt",
                "sensors_count": "7",
            },
            {
                "file": r"test_data/data/60 ТСП (1 вариант) !!!!!.txt",
                "sensors_count": "7"
            }
        ],
        "cp": [
            "60", "60", "60.1", "60", "60",
            "60", "60", "60", "60.1", "60"
        ],
        "md": [
            "60.1", "60", "60", "60", "60.1",
            "60", "60.1", "60", "60", "60"
        ]
    },  # OK
    {
        "target": "90",
        "logs": [
            {
                "file": r"test_data/data/90 ПТСВ (2 вариант).txt",
                "sensors_count": "7",
            },
            {
                "file": r"test_data/data/90 ТСП (1 вариант) !!!!!!!.txt",
                "sensors_count": "7"
            }
        ],
        "cp": [
            "90", "90.1", "90.1", "90", "90",
            "90", "90", "90", "90", "90"
        ],
        "md": [
            "90.1", "90", "90", "89.9", "90",
            "90", "90.1", "90", "90.1", "90"
        ]
    },  # OK
    {
        "target": "-30",
        "logs": [
            {
                "file": r"test_data/data/-30 ПТСВ (2 вариант) !!!!!.txt",
                "sensors_count": "7",
            },
            {
                "file": r"test_data/data/-30 ТСП (1 вариант)!!!.txt",
                "sensors_count": "7"
            }
        ],
        "cp": [
            "-30", "-30.1", "-30.1", "-30", "-30",
            "-30", "-30", "-30", "-30", "-30"
        ],
        "md": [
            "-30.1", "-30", "-30", "-29.9", "-30",
            "-30", "-30.1", "-30", "-30.1", "-30"
        ]
    },  # OK
]

# user adds modes to the test object
for tmode in tmodes:
    t.add_temperature_mode(tmode)

# t.add_humidity_mode(TEST_HUMIDITY_MODE)

# user adds report data
t.data['specialist'] = 'Комаров С.В.'

# user adds tools data
t.data['tools'] = [  # tools data
    'GTH 5050',
    'Гидрометр ФЫ-2'
]

# user adds system data
t.data['system'] = {  # system info
    'name': 'НАИМЕНОВАНИЕ КАМЕРЫ',
    'year_of_production': 'ГОД ВЫПУСКА',
    'manufacturer': 'ПРОИЗВОДИТЕЛЬ',
    'factory_number': 'ЗАВ. НОМЕР',
    'description': 'ТЕХ. ХАРАКТЕРИСТИКИ КАМЕРЫ',
    'test_program': 'ПРОГРАММА',
    'test_method': 'МЕТОДИКА',
}


t.calculate()  # invoking test calculation logic

# user can save test to file and reload it from the file
t.path = 'tests/test_1.json'
t.save()
print('Calculated and saved to:', t.path)


# TEMPLATE

# user specifies output path for report
report_path = r'C:\Users\2065\Desktop\easytest2\reports'   # ask user every time


# user can generate report files in MS WORD format
def make_report():
    builder = ReportBuilder(t, report_path)
    builder.build_additions()
    builder.build_main()

make_report()

print('Reports created.')
