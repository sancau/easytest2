from collections import namedtuple

LogDescriptions = namedtuple('LogDescriptions', ['DT1', 'DT2', 'KT'])
DESC = LogDescriptions('DT1', 'DT2', 'KT')

TEST_HUMIDITY_MODE = {
    'logs': [
        {
            'file': '1.xlsx',
            'desc': DESC.DT1
        },
        {
            'file': '2.xlsx',
            'desc': DESC.DT2
        },
        {
            'file': '2.xlsx',
            'desc': DESC.KT
        }
    ],
    'target': {
        'hum': 90,
        'temp': 25
    },
    'md': {
        'hum': [90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
        'temp': [25, 25, 25, 25, 25, 25, 25, 25, 25, 25]
    }
}
