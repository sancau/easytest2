# -*- coding: utf-8 -*-

REQUIRED_INPUT_INFO = {
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
