# -*- coding: utf-8 -*-

from datetime import datetime

from temperature.meta import Meta
from temperature.parser import TemperatureDataParser
from temperature.preprocessor import TemperatureDataPreprocessor
from temperature.processor import TemperatureDataProcessor


class TemperatureModeHandler:
    @staticmethod
    def _test_temperature_mode(meta):
        """
        High level processing method.
        :param meta: An object of type dict containing all the meta
        information and data that is required for the test to be processed.
        :return: An object of type dict containing the test result and all the
        resulting values and meta information.
        """
        data_chunks = []
        for log in meta.logs:
            parser = TemperatureDataParser(
                sensors_count=log.sensors_count,
                digits=meta.round_to,
                base64='.txt' not in log.file)

            data, date, time = parser.parse(log.file)
            try:
                if not meta.date or \
                                datetime.strptime(meta.date, '%d.%m.%Y') < \
                                datetime.strptime(date, '%d.%m.%Y'):
                    meta.date = date
                    meta.time = time
            except ValueError:
                print('Date parsing error, %d' % date)

            meta.time = time
            data_chunks.append(data)

        preprocessor = TemperatureDataPreprocessor()
        processor = TemperatureDataProcessor()

        result = {}
        for chunk in preprocessor.get_merged_chunk(
                data_chunks=data_chunks,
                meta=meta):
            result = processor.process(chunk, meta)
            if result['done']:
                break
        return result

    @staticmethod
    def handle(data):
        """
        Top level method to handle temperature mode data.
        :param data: Mode data as an object of type dict.
        :return: Resulting object, containing resolution and values.
        """
        payload = Meta(data)
        validation_status = payload.validate()
        if validation_status['valid']:
            result = TemperatureModeHandler._test_temperature_mode(payload)
        else:
            result = {
                'done': False,
                'errors': validation_status['errors']
            }
        return result
