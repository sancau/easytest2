# -*- coding: utf8 -*-
"""
Validation logic
"""


def validate_temperature_mode(mode):  # TODO more type specific validation
    """Ensures the temperature mode
       has the right data schema
    """
    errors = []

    schema = {
        'target': 'Target temperature mode value.',
        'logs': [
            {
                'file': '*** SEND A LOG FILE AS BASE64 STRING ***',
                'sensors_count': 'How many sensors to parse from the file.',
            }
        ],
        'cp': 'Control point values as a list.',
        'md': 'Measurement device values as a list.'
    }

    try:
        errors.extend(['{} not found'.format(key)
                       for key in schema.keys() if key not in mode])

        if 'logs' in mode:
            for i, log in enumerate(mode['logs']):
                errors.extend(['{} not found in log {}'.format(key, i)
                              for key in schema['logs'][0].keys()
                              if key not in log])
    except Exception as e:
        errors.append('Exception: {}'.format(e))

    return errors


def validate_humidity_mode(mode):  # TODO more type specific validation
    """Ensures the humidity mode
       has the right data schema
    """
    errors = []

    schema = {
        'logs': [
            {
                'file': 'Log file path',
                'desc': 'Signals if this log file is DT OR KT'
            }
        ],
        'target': {
            'humidity': 'Target humidity value.',
            'temperature': 'Target temperature value.'
        },
        'md': {
            'humidity': 'Humidity measurement device values as a list.',
            'temperature': 'Temperature measurement device values as a list.'
        }
    }

    try:
        errors.extend(['{} not found'.format(key)
                       for key in schema.keys() if key not in mode])

        if 'logs' in mode:
            for i, log in enumerate(mode['logs']):
                errors.extend(['{} not found in log {}'.format(key, i)
                              for key in schema['logs'][0].keys()
                              if key not in log])
    except Exception as e:
        errors.append('Exception: {}'.format(e))

    return errors


def validate_test_settings(settings):  # TODO more type specific validation
    """Ensures the global test settings are valid
    """
    errors = []

    schema = {
        'temperature': {
            'sensors_total': 'How many sensors to  use in test logic.',
            'slice_length': 'The number of iterations to use in test logic.',
            'round_to': 'Values will be rounded to the given number of digits.',
            'max_deviation': 'Maximum allowed deviation to pass the test.'
        },
        'humidity': {
            'slice_length': 'The number of iterations to use in test logic.',
            'round_to': 'Values will be rounded to the given number of digits.',
            'max_deviation': {
                'temperature': 'Maximum allowed deviation to pass the test.',
                'humidity': {},  # k -> v as humidity value -> tuple(pos, neg)
            }
        }
    }

    try:
        errors.extend(['{} not found'.format(key)
                       for key in schema.keys() if key not in settings])

        errors.extend(['{} not found'.format(key)
                       for key in schema['temperature'].keys()
                       if key not in settings])

        errors.extend(['{} not found'.format(key)
                       for key in schema['humidity'].keys()
                       if key not in settings])

    except Exception as e:
        errors.append('Exception: {}'.format(e))

    return errors
