"""
Application settings and defaults
"""

from datetime import datetime

DEFAULT_TEST = {
    'date_created': datetime.now(),
    'specialist': None,
    'responsible_specialist': 'Ксенофонтов Б.А.',
    'system': None,
    'tools': [],
    'humidity': [],
    'temperature': [],
    'report': None,
    'settings': {
        'humidity': {  # default humidity settings
            'slice_length': 10,
            'round_to': 1,
            'max_deviation': {
                'temperature': 2,
                'humidity': {
                    'default': (3, -3),
                    '98': (2, -3)
                }
            }
        },
        'temperature': {  # default temperature settings
            'sensors_total': 8,
            'slice_length': 10,
            'round_to': 1,
            'max_deviation': 2
        }
    }
}

MAIN_TPL = r'report/templates/main_tpl.docx'
TEMPERATURE_MODE_TPL = r'report/templates/tmode_tpl.docx'
HUMIDITY_MODE_TPL = r'report/templates/hmode_tpl.docx'
