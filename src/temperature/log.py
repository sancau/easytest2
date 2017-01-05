# -*- coding: utf-8 -*-
class Log:
    """
    Describes single log object that embedded to a Meta object.
    """
    def __init__(self, payload):
        self.file = payload['file']
        self.sensors_count = int(payload['sensors_count'])
