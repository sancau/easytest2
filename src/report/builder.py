# coding=utf-8
import os
from datetime import datetime

from docxtpl import DocxTemplate

from report.utils import get_verbose_date

from settings import MAIN_TPL
from settings import HUMIDITY_MODE_TPL
from settings import TEMPERATURE_MODE_TPL


class ReportBuilder:
    def __init__(self, test, report_path):
        self.test = test
        self.report_path = report_path
        self.hmode_path = os.path.join(report_path, 'Влага')
        self.tmode_path = os.path.join(report_path, 'Температура')

    @staticmethod
    def ensure_path_exists(path):
        dir_ = os.path.dirname(path)
        if not os.path.exists(dir_):
            os.makedirs(dir_)

    @staticmethod
    def build_docx(template, context, path):
        doc = DocxTemplate(template)
        doc.render(context)
        ReportBuilder.ensure_path_exists(path)
        doc.save(path)

    @staticmethod
    def build_temperature_mode_ctx(mode, page, test):
        def b_res_string(tmode, delta, notation):
            if not float(delta):
                return ''

            md_delta = tmode['processed']['values']['md_delta']
            res = round(2 - float(md_delta), 1)  # TODO

            return ('\u0394{} = {} cтрого меньше |+/- \u0394нор|'
                    ' - \u0394 иy  = 2 – {}  = {}    СООТВЕТСТВУЕТ').format(notation, delta, md_delta, res)

        def b_delta_string(value, notation):
            if not float(value):
                return ''
            else:
                return '\u0394{} = {} \u00B0C'.format(notation, value)

        def get_rows_for_word(sensors):
            rows_index_map = {0: 1, 1: 2, 2: 3, 3: 4,
                              4: 5, 5: 6, 6: 7, 7: 8,
                              8: 9, 9: 10,
                              10: 'Средн', 11: 'Т мах', 12: 'T мин',
                              13: 'А мах', 14: 'А мин'}

            sensor_index_map = {0: 'one', 1: 'two', 2: 'three',
                                3: 'four', 4: 'five', 5: 'six',
                                6: 'seven', 7: 'eight', 8: 'nine',
                                9: 'ten', 10: 'eleven', 11: 'twelve',
                                12: 'thirteen', 13: 'fourteen',
                                14: 'fifteen', 15: 'sixteen',
                                16: 'seventeen', 17: 'eighteen'}
            rows = []
            for i in range(len(sensors[0])):
                r = {'i': rows_index_map[i]}
                for idx, sensor in enumerate(sensors):
                    r[sensor_index_map[idx]] = sensor[i]
                rows.append(r)
            return rows

        mode_vals = mode['processed']['values']

        return {
            'max_deviation': mode_vals['max_deviation'],
            'max_amplitude': mode_vals['max_amplitude'],
            'md_delta': mode_vals['md_delta'],
            'deviation': mode_vals['deviation'],
            'target': mode_vals['meta']['target'],
            'date': mode_vals['meta']['date'],
            'page': page,
            'positive_delta': b_delta_string(mode_vals['positive_delta'], 'T1'),
            'negative_delta': b_delta_string(mode_vals['negative_delta'], 'Т2'),
            'res_string_pos': b_res_string(mode, mode_vals['positive_delta'], 'Т1'),
            'res_string_neg': b_res_string(mode, mode_vals['negative_delta'], 'Т2'),
            'specialist': test.data['specialist'],
            't_max': mode_vals['t_max'],
            't_min': mode_vals['t_min'],
            't_md': mode_vals['t_md'],
            't_cp': mode_vals['t_cp'],
            'rows': get_rows_for_word(mode_vals['sensors'])
        }

    @staticmethod
    def build_humidity_mode_ctx(mode, page, test):
        return {

        }

    @staticmethod
    def build_main_ctx(test):
        def btmode(mode):
            res = mode['processed']['values']
            pos_delta = res.get('positive_delta', '')
            neg_delta = res.get('negative_delta', '')
            return {
                'target': mode['mode']['target'],
                'positive_delta': pos_delta,
                'negative_delta': '-' + str(neg_delta),
                'md_delta': res['md_delta'],
                'positive_total_error': round(pos_delta + res['md_delta'], 1) if pos_delta else '',  # todo
                'negative_total_error': '-' + str(neg_delta + res['md_delta']) if neg_delta else '',
                'verbose_max_deviation': u'\u00B1' + str(res['max_deviation'])
            }

        def bhmode(mode):
            res = mode['processed']
            pos_delta = res.get('positive_deviation', '')
            neg_delta = res.get('negative_deviation', '')

            def get_verbose_max_dev_hum(dev):
                if dev['humidity'][0] + dev['humidity'][1] == 0:
                    return u'\u00B1' + str(dev['humidity'][0])
                else:
                    return '+' + str(dev['humidity'][0]) + ', ' + str(dev['humidity'][1])

            return {
                'verbose_hum': res['target']['humidity'],
                'verbose_temp': res['target']['temperature'],
                'positive_delta': pos_delta,
                'negative_delta': '-' + str(neg_delta),
                'md_delta': res['md_delta_humidity'],
                'positive_total_error': round(pos_delta + res['md_delta_humidity'], 1) if pos_delta else '',  # todo
                'negative_total_error': '-' + str(neg_delta + res['md_delta_humidity']) if neg_delta else '',
                'verbose_max_deviation': get_verbose_max_dev_hum(res['max_allowed_deviation'])
            }

        return {
            'report': {
                'date': get_verbose_date(datetime.now()),
                'specialist': test.data['specialist'],
                'responsible_specialist': test.data['responsible_specialist'],
                'total_additions_count': len(test.data['humidity']) + len(test.data['temperature'])
            },
            'system': test.data['system'],
            'tools': test.data['tools'],
            'modes': {
                'summary': {
                    'max_tmode': max([mode['mode']['target'] for mode in test.data['temperature']]),
                    'min_tmode': min([mode['mode']['target'] for mode in test.data['temperature']]),
                    'max_hmode_hum': max([mode['mode']['target']['humidity'] for mode in test.data['humidity']]),
                    'min_hmode_temp': min([mode['mode']['target']['temperature'] for mode in test.data['humidity']]),
                    'max_hmode_temp': max([mode['mode']['target']['temperature'] for mode in test.data['humidity']]),

                    'tmax_deviation': max([mode['processed']['values']['deviation'] for mode in test.data['temperature']]),
                    'tmax_md_delta': max([mode['processed']['values']['md_delta'] for mode in test.data['temperature']]),

                    'tmax_amplitude': max(
                        [max([mode['processed']['values'].get('positive_delta', 0),
                              mode['processed']['values'].get('negative_delta', 0)])
                                                            for mode in test.data['temperature']]),

                    'hmax_deviation': max([mode['processed']['humidity_deviation'] for mode in test.data['humidity']]),
                    'hmax_md_delta': max([mode['processed']['md_delta_humidity'] for mode in test.data['humidity']])
                },
                'tmodes': [btmode(mode) for mode in sorted(test.data['temperature'], key=lambda k: k['mode']['target'])],

                # TODO sort by target_hum then by target_temp
                'hmodes': [ bhmode(mode) for mode in sorted(test.data['humidity'], key=lambda k: k['mode']['target']['humidity'])],
            }
        }

    def build_additions(self):
        data = self.test.data

        hmodes = data['humidity']
        tmodes = data['temperature']

        page = 1
        for mode in tmodes:
            ctx = self.build_temperature_mode_ctx(mode, page, self.test)
            target = int(mode['mode']['target'])
            prefix = '+' if target > 0 else ''
            filename = prefix + str(target) + '.docx'
            path = os.path.join(self.tmode_path, filename)
            self.build_docx(TEMPERATURE_MODE_TPL, ctx, path)
            page += 1

        for mode in hmodes:
            ctx = self.build_humidity_mode_ctx(mode, page, self.test)
            t_target = str(mode['mode']['target']['temperature'])
            h_target = str(mode['mode']['target']['humidity'])
            filename = '_'.join([t_target, h_target]) + '.docx'
            path = os.path.join(self.hmode_path, filename)
            self.build_docx(HUMIDITY_MODE_TPL, ctx, path)
            page += 1

    def build_main(self):
        ctx = self.build_main_ctx(self.test)
        system_description = self.test.data['system']['name'] or 'UNKNOWN_SYSTEM'
        filename = 'Протокол аттестации ' + system_description + '.docx'
        path = os.path.join(self.report_path, filename)
        self.build_docx(MAIN_TPL, ctx, path)
