#-*- coding: utf8 -*-
"""
Validation logic
"""

def validate_temperature_mode(mode):
    """Ensures the temperature mode 
       has the right data schema
    """
    errors = []

    schema = {
        "target": "Target temperature mode value.",
        "logs": [
            {
                "file": "*** SEND A LOG FILE AS BASE64 STRING ***",
                "sensors_count": "How many sensors to parse from the file.",
            }
        ],
        "sensors_total": "How many sensors to  use in test logic.",
        "slice_length": "The number of iterations to use in test logic.",
        "round_to": "All values will be rounded to the given number of digits.",
        "cp": "Control point values as a list.",
        "md": "Measurement device values as a list.",
        "max_deviation": "Maximum allowed deviation to pass the test."
    }

    try:
        errors.extend(['{} not found'.format(key) 
                       for key in schema.keys() if not key in mode])

        if 'logs' in mode:
            for i, log in enumerate(mode['logs']):
                errors.extend(['{} not found in log {}'.format(key, i)
                              for key in schema['logs'][0].keys() 
                              if not key in log])
    except Exception as e:
        errors.append('Exception: {}'.format(e))

    return errors
