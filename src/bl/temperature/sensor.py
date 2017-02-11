# -*- coding: utf-8 -*-
class Sensor:
    """
    This class describes a data set for a certain sensor.
    It provides some useful properties to use while processing the data.
    """
    def __init__(self, *, name, values):
        self.values = values
        self.name = name

    def _round(self, value):
        """Returns the max length of a number in data.
        """
        digits = max([len(str(i).split('.')[1]) for i in self.values])
        return round(value, digits)

    @property
    def average(self):
        res = sum(self.values) / float(len(self.values))
        return self._round(res)

    @property
    def max_temperature(self):
        return max(self.values)

    @property
    def min_temperature(self):
        return min(self.values)

    @property
    def positive_deviation(self):
        res = abs(abs(self.max_temperature) - abs(self.average))
        return self._round(res)

    @property
    def negative_deviation(self):
        res = abs(abs(self.min_temperature) - abs(self.average))
        return self._round(res)
