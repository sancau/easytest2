# -*- coding: utf-8 -*-
"""
Temperature data processor.
"""
IN_PROGRESS = 'The processing is in progress.'
INVALID_DATA = 'The processing canceled due to invalid input data.'
TEST_FAIL = 'The data was processed. The test is NOT passed.'
TEST_FAIL_AMPLITUDE = 'The data was processed. Amplitude > 0.5.'
TEST_SUCCESS = 'The data was processed. The test is passed.'


class TemperatureDataProcessor:
    """
    This class contains processing logic for temperature data.

    It has one interface method process(data), that accepts a data object
    and returns a result object of type dict.

    The class constructor requires kw argument 'slice_length' of type int.
    """
    @staticmethod
    def _validate_input(data):
        """
        Ensures that the provided data length is at least equal to
        the required 'slice_length'.
        """
        return True and data  # can be specified later

    def process(self, data, meta):
        """
        Processing the given data.
        Returns a dict object containing result, reason and values.
        """
        res = {'done': False, 'reason': IN_PROGRESS, 'values': None}

        try:
            if not self._validate_input(data):
                res['reason'] = INVALID_DATA
                return res
            amplitudes = []
            for sensor in data:
                amplitudes.append(sensor.negative_deviation)
                amplitudes.append(sensor.positive_deviation)
            max_amplitude = max(amplitudes)

            if max_amplitude >= 0.5:
                res['reason'] = TEST_FAIL_AMPLITUDE
                return res

            # should cp and md columns be included into t_max/min calculation ?
            t_max = max([sensor.average for sensor in data])
            t_min = min([sensor.average for sensor in data])
            t_md = [sensor.average for sensor in data if
                    sensor.name == 'md'][0]
            t_cp = [sensor.average for sensor in data if
                    sensor.name == 'cp'][0]

            positive_delta = abs(abs(t_max) - abs(meta.target))
            negative_delta = abs(abs(t_min) - abs(meta.target))
            md_delta = abs(abs(t_md) - abs(t_cp))
            deviation = abs(abs(t_max) - abs(t_min))
            max_deviation = meta.max_deviation

            def _build_sensor_values_list(s):
                """
                Returns all the sensor data as a list of floats
                :param s: sensor object
                :return: [float]
                """
                return s.values + \
                    [s.average, s.max_temperature, s.min_temperature,
                     s.positive_deviation, s.negative_deviation]

            meta.logs = [log.__dict__ for log in meta.logs]

            res['values'] = {
                'meta': meta.__dict__,
                'sensors': [_build_sensor_values_list(s) for s in data],
                't_max': t_max,
                't_min': t_min,
                't_md': t_md,
                't_cp': t_cp,
                'negative_delta': negative_delta,
                'md_delta': md_delta,
                'deviation': deviation,
                'max_deviation': max_deviation
            }

            # check if the test is passed
            for i in [positive_delta, negative_delta]:
                res['done'] = i < (abs(max_deviation) - abs(md_delta))
                if not res['done']:
                    res['reason'] = TEST_FAIL
                    return res
            res['reason'] = TEST_SUCCESS

            return res

        except Exception as e:
            res['reason'] = e
        return res
