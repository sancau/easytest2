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
        "humidity": {  # default humidity settings
            "slice_length": 10,
            "round_to": 1,
            "max_deviation": {
                "SOME_EXCEPTION": [2, 2],  # special case (pos, neg)
                "default": [2, 2]  # default humidity max_deviation (pos, neg)
            }
        },
        "temperature": {  # default temperature settings
            "sensors_total": 8,
            "slice_length": 10,
            "round_to": 1,
            "max_deviation": 2
        }
    }
}