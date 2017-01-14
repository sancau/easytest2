from collections import namedtuple

LogDescriptions = namedtuple('LogDescriptions', ['DT1', 'DT2', 'KT'])
DESC = LogDescriptions('DT1', 'DT2', 'KT')

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
