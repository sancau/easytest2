# coding=utf-8
import os
import sys
import traceback

from datetime import datetime, timedelta

from dateutil import parser

from docxtpl import DocxTemplate

from bl.report.utils import get_verbose_date

from bl.settings import MAIN_TPL
from bl.settings import HUMIDITY_MODE_TPL
from bl.settings import get_temperature_template


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
            res = round(2 - float(md_delta), tmode['mode']['round_to'])

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
        def get_verbose_max_dev_hum(dev):
            if dev['humidity'][0] + dev['humidity'][1] == 0:
                return u'\u00B1' + str(dev['humidity'][0])
            else:
                return '+' + str(dev['humidity'][0]) + ', ' + str(dev['humidity'][1])

        def b_res_string(hmode, delta, notation):
            if not float(delta):
                return ''

            md_delta = hmode['processed']['md_delta_humidity']

            max_hum_dev = hmode['processed']['max_allowed_deviation']['humidity'][int(notation) - 1]
            max_hum_dev = abs(max_hum_dev)
            res = round(max_hum_dev - float(md_delta), hmode['mode']['round_to'])

            word = 'СООТВЕТСТВУЕТ' if delta < res else 'НЕ СООТВЕТСТВУЕТ'

            return ('\u0394\u03C6{} = {} cтрого меньше |+/- \u0394\u03C6нор|'
                    ' - \u0394\u03C6иy  = {} – {}  = {}    {}')\
                .format(notation, delta, max_hum_dev, md_delta, res, word)

        def b_delta_string(value, notation):
            if not float(value):
                return ''
            else:
                return '\u0394\u03C6{} = {} \u00B0C'.format(notation, value)

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

        processed = mode['processed']

        sensors = [
            processed['dt1_humidity'],
            processed['dt2_humidity'],
            processed['kt_temperature'],
            processed['kt_humidity'],
            processed['md_temperature'],
            processed['md_humidity'],
        ]

        return {
            'max_deviation_hum': get_verbose_max_dev_hum(processed['max_allowed_deviation']),
            'max_deviation_temp': processed['max_allowed_deviation']['temperature'],
            'target': processed['target'],
            'page': page,
            'date': '{}.{}.{}'.format(str(processed['date'])[8:],
                                      str(processed['date'])[5:7],
                                      str(processed['date'])[:4]),

            'md_delta': processed['md_delta_humidity'],
            'deviation': processed['humidity_deviation'],

            'positive_delta': b_delta_string(processed['positive_deviation'], '1'),
            'negative_delta': b_delta_string(processed['negative_deviation'], '2'),

            'res_string_pos': b_res_string(mode, processed['positive_deviation'], '1'),
            'res_string_neg': b_res_string(mode, processed['negative_deviation'], '2'),
            'specialist': test.data['specialist'],

            'p': processed,
            'rows': get_rows_for_word(sensors)
        }

    @staticmethod
    def build_main_ctx(test):
        def make_tool_report_string(tool):
            name = 'Информация о приборе некорректна'.upper()
            try:
                name = tool['name']
                date = tool['tests'][0]['date']
                valid_until = \
                    (parser.parse(date) - timedelta(days=1)).strftime('%d.%m.%Y')
                test_doc = tool['comment']

                return '{}; срок поверки до {}; документ поверки: {}'.format(name, valid_until,
                                                                             test_doc)
            except Exception as e:
                print(e)
                return name + ' (Информация о приборе может быть некорректна)'.upper()

        def make_system_report_object(system):
            obj = {}
            for i in ['name', 'yearOfProduction', 'manufacturer',
                      'factoryNumber', 'techDetails', 'testProgram',
                      'testMethod']:
                obj[i] = system.get(i, '[НЕТ ДАННЫХ {}]'.format(i))
            return obj

        def btmode(mode):
            res = mode['processed']['values']
            pos_delta = res.get('positive_delta', '')
            neg_delta = res.get('negative_delta', '')
            return {
                'target': mode['mode']['target'],
                'positive_delta': pos_delta,
                'negative_delta': '-' + str(neg_delta),
                'md_delta': res['md_delta'],
                'positive_total_error': round(pos_delta + res['md_delta'], mode['mode']['round_to']) if pos_delta else '',
                'negative_total_error': '-' + str(round(neg_delta + res['md_delta'], mode['mode']['round_to'])) if neg_delta else '',
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
                'positive_total_error': round(pos_delta + res['md_delta_humidity'], mode['mode']['round_to']) if pos_delta else '',
                'negative_total_error': '-' + str(round(neg_delta + res['md_delta_humidity'], mode['mode']['round_to'])) if neg_delta else '',
                'verbose_max_deviation': get_verbose_max_dev_hum(res['max_allowed_deviation'])
            }

        try:  # TODO think of better solution
            # HUM
            max_hmode_hum = max([mode['mode']['target']['humidity'] for mode in test.data['humidity']])
            min_hmode_temp = min([mode['mode']['target']['temperature'] for mode in test.data['humidity']])
            max_hmode_temp = max([mode['mode']['target']['temperature'] for mode in test.data['humidity']])
            hmax_deviation = max([mode['processed']['humidity_deviation'] for mode in test.data['humidity']])
            hmax_md_delta = max([mode['processed']['md_delta_humidity'] for mode in test.data['humidity']])

            # TEMP
            tmax_deviation = max([mode['processed']['values']['deviation'] for mode in test.data['temperature']])
            tmax_md_delta = max([mode['processed']['values']['md_delta'] for mode in test.data['temperature']])
            tmax_amplitude = max(
                [max([mode['processed']['values'].get('positive_delta', 0),
                      mode['processed']['values'].get('negative_delta', 0)])
                 for mode in test.data['temperature']])

        except Exception as e:
            print(e)
            max_hmode_hum = None
            min_hmode_temp = None
            max_hmode_temp = None
            hmax_deviation = None
            hmax_md_delta = None
            tmax_deviation = None
            tmax_md_delta = None
            tmax_amplitude = None

        return {
            'report': {
                'date': get_verbose_date(datetime.now()),
                'test_start_date': get_verbose_date(
                    datetime.strptime(test.data['test_start_date'], '%Y-%m-%d')),
                'test_end_date': get_verbose_date(
                    datetime.strptime(test.data['test_end_date'], '%Y-%m-%d')),
                'specialist': test.data['specialist'],
                'responsible_specialist': test.data['responsible_specialist'],
                'total_additions_count': (len([i for i in test.data['humidity'] if i[
                    'processed']['result']['summary_mode_result']]) +
                                         len([i for i in test.data['temperature'] if i[
                                             'processed']['done']]))
            },
            'system': make_system_report_object(test.data['system']),
            'tools': [make_tool_report_string(t) for t in test.data['tools']],
            'modes': {
                'summary': {
                    'max_tmode': max([int(mode['mode']['target']) for mode in test.data[
                        'temperature']]),
                    'min_tmode': min([int(mode['mode']['target']) for mode in test.data[
                        'temperature']]),

                    'max_hmode_hum': max_hmode_hum,
                    'min_hmode_temp': min_hmode_temp,
                    'max_hmode_temp': max_hmode_temp,

                    'tmax_deviation': tmax_deviation,
                    'tmax_md_delta': tmax_md_delta,

                    'tmax_amplitude': tmax_amplitude,

                    'hmax_deviation': hmax_deviation,
                    'hmax_md_delta': hmax_md_delta
                },
                'tmodes': [btmode(mode) for mode in sorted(test.data['temperature'], key=lambda
                    k: k['mode']['target']) if mode['processed']['done']],

                # TODO sort by target_hum then by target_temp
                'hmodes': [bhmode(mode) for mode in sorted(test.data['humidity'], key=lambda k:
                    k['mode']['target']['humidity']) if mode['processed']['result'][
                    'summary_mode_result']],
            }
        }

    def build_additions(self):
        data = self.test.data

        hmodes = data['humidity']
        tmodes = data['temperature']

        page = 1
        for mode in tmodes:
            try:
                ctx = self.build_temperature_mode_ctx(mode, page, self.test)
                target = int(mode['mode']['target'])
                prefix = '+' if target > 0 else ''
                filename = prefix + str(target) + '.docx'
                path = os.path.join(self.tmode_path, filename)
                self.build_docx(get_temperature_template(mode), ctx, path)
                page += 1
            except Exception as e:
                ex_t, ex_v, tb = sys.exc_info()
                print(ex_t, ex_v)
                print(traceback.format_tb(tb))

        for mode in hmodes:
            try:
                ctx = self.build_humidity_mode_ctx(mode, page, self.test)
                t_target = str(mode['mode']['target']['temperature'])
                h_target = str(mode['mode']['target']['humidity'])
                filename = '_'.join([t_target, h_target]) + '.docx'
                path = os.path.join(self.hmode_path, filename)
                self.build_docx(HUMIDITY_MODE_TPL, ctx, path)
                page += 1
            except Exception as e:
                print(e)

    def build_main(self):
        ctx = self.build_main_ctx(self.test)
        system_description = self.test.data['system']['name'] or 'UNKNOWN_SYSTEM'
        filename = 'Протокол аттестации ' + system_description + '.docx'
        filename = filename.replace(r'\\', ' ').replace('/', ' ')
        path = os.path.join(self.report_path, filename)
        self.build_docx(MAIN_TPL, ctx, path)
