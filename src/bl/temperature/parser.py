# -*- coding: utf-8 -*-
"""
Temperature data parser module for easytest application.
"""
import base64

DEFAULT_DATA_CONFIG = {
    'date_line_number': 0,  # where to look to date and time
    'date_position': (25, 35),  # to cut out date
    'time_position': (44, 52),  # to cut out time
    'first_valuable_line': 4,  # what line is the first that contains values
    'time_substring_slice': (7, 19),  # to cut out the timestamp from a line
    'values_start_at': 19  # char index of the first value start
}


class TemperatureDataParser:
    """
    Provides functionality to parse a digital thermometer
    data from it's log files.

    It has one interface method - parse(file_path).
    Parse returns a tuple of (iterations[], date, time).

    The class constructor requires 2 kw arguments
    'sensors_count' and 'digits'.
    The second one controls the number of digits 
    the data values to be rounded to.
    """
    def __init__(
            self, *, 
            sensors_count,
            digits,
            base64=False, 
            config=DEFAULT_DATA_CONFIG, 
            encoding='1251'):

        self._sensors_count = sensors_count
        self._config = config
        self._digits = digits  # values will be rounded to <digits> digits
        self._encoding = encoding
        self._base64 = base64

    def _get_time(self, line):
        """
        Returns time stamp in seconds for a given log file line.
        """
        start, end = self._config['time_substring_slice']
        try:
            time = float(line[start:end].strip())
            time = round(time, self._digits)
        except ValueError:
            time = None
        return time

    def _get_log_date(self, file_lines):
        """
        Returns date and time of the log by a given file path.
        """
        date_line_number = self._config['date_line_number']
        date_line = file_lines[date_line_number]

        date_start, date_end = self._config['date_position']
        time_start, time_end = self._config['time_position']
        return date_line[date_start:date_end], date_line[time_start:time_end]

    def _get_values(self, line):
        """
        Returns all the values from a given line as an array of floats.
        """
        start = self._config['values_start_at']
        line = line[start:]

        def clean_value(val):
            """
            Insures the value can be parsed as float.
            """
            try:
                res = round(float(val), self._digits)
            except ValueError:
                res = None
            return res

        return [clean_value(v) for v in line.split()][:self._sensors_count]

    def _values_valid(self, values):
        """
        Insures that given array contains floats only.
        """
        if len(values) != self._sensors_count:
            return False

        for v in values:
            if not type(v) is float:
                return False
        return True

    def parse(self, log_file):
        """
        Returns parsed data from a given file path.
        """
        if self._base64:
            bytes_string = bytes(log_file, encoding=self._encoding)
            decoded = base64.decodebytes(bytes_string)
            string = str(decoded, encoding=self._encoding)
        else:
            with open(log_file, 'r', encoding=self._encoding) as f:
                string = f.read()

        file_lines = string.split('\n')
        date, time = self._get_log_date(file_lines)
        iterations = []
        start = self._config['first_valuable_line']
        log = file_lines[start:]
        for line in log:
            timestamp = self._get_time(line)
            values = self._get_values(line)
            if self._values_valid(values):
                iteration = (timestamp, values)
                iterations.append(iteration)
        return iterations, date, time
