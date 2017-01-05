# -*- coding: utf-8 -*-
from temperature.log import Log


class Meta:
    """
    Describes temperature mode meta data object.
    """
    def __init__(self, payload):
        self.sensors_total = int(payload['sensors_total'])
        self.cp = [float(v) for v in payload['cp']]
        self.md = [float(v) for v in payload['md']]
        self.target = float(payload['target'])
        self.slice_length = int(payload['slice_length'])
        self.max_deviation = float(payload['max_deviation'])
        self.round_to = int(payload['round_to'])
        self.logs = [Log(log) for log in payload['logs']]
        self.date = payload.get('date', None)
        self.time = payload.get('time', None)

    def validate(self):
        """
        Validates provided meta data.
        :return: Dict of boolean result and errors.
        """
        result = {
            'errors': []
        }

        # validate cp / md / slice_length relations
        if self.slice_length > len(self.cp) or \
                self.slice_length > len(self.md):
            result['errors'].append(
                'Not enough CP / MD values to fit required slice length.')

        # if we have too much values for cp - cut it
        if self.slice_length < len(self.cp):
            self.cp = self.cp[:self.slice_length]

        # same with md
        if self.slice_length < len(self.md):
            self.md = self.md[:self.slice_length]

        result['valid'] = len(result['errors']) == 0
        return result
