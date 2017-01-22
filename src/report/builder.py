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
    def build_temperature_mode_ctx(mode, page):
        return {

        }

    @staticmethod
    def build_humidity_mode_ctx(mode, page):
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
                'positive_total_error': pos_delta + res['md_delta'] if pos_delta else '',
                'negative_total_error': '-' + str(neg_delta + res['md_delta']) if neg_delta else '',
                'verbose_max_deviation': u'\u00B1' + str(res['max_deviation'])
            }

        def bhmode(mode):
            res = mode['processed']
            pos_delta = res.get('positive_deviation', '')
            neg_delta = res.get('negative_deviation', '')

            def get_verbose_max_dev_hum(dev):
                print(dev)
                if dev['humidity'][0] + dev['humidity'][1] == 0:
                    return u'\u00B1' + str(dev['humidity'][0])
                else:
                    return '+' + str(dev['humidity'][0]) + ', ' + '-' + str(dev['humidity'][1])

            return {
                'verbose_hum': res['target']['humidity'],
                'verbose_temp': res['target']['temperature'],
                'positive_delta': pos_delta,
                'negative_delta': '-' + str(neg_delta),
                'md_delta': res['md_delta_humidity'],
                'positive_total_error': pos_delta + res['md_delta_humidity'] if pos_delta else '',
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
                    'max_tmode': 'МАКС. РЕЖИМ ТЕМПЕРАТУРЫ',
                    'min_tmode': 'МИН. РЕЖИМ ТЕМПЕРАТУРЫ',
                    'max_hmode_hum': 'МАКС. РЕЖИМ ВЛАГИ',
                    'min_hmode_temp': 'МИН. РЕЖИМ ТЕМП. ВЛАГИ',
                    'max_hmode_temp': 'МАКС. РЕЖИМ ТЕМП. ВЛАГИ',
                    'tmax_deviation': 'МАКС. НЕРАВНОМЕРНОСТЬ ТЕМПЕРАТУРЫ',
                    'tmax_md_delta': 'МАКС. ПОГРЕШНОСТЬ ИУ ТЕМПЕРАТУРЫ',
                    'tmax_amplitude': 'МАКС. АМПЛИТУДА КОЛЕБАНИЙ ТЕМПЕРАТУРЫ',
                    'hmax_deviation': 'МАКС. НЕРАВНОМЕРНОСТЬ ВЛАГИ',
                    'hmax_md_delta': 'МАКС. ПОГРЕШНОСТЬ ИУ ВЛАГИ'
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
            ctx = self.build_temperature_mode_ctx(mode, page)
            target = int(mode['mode']['target'])
            prefix = '+' if target > 0 else ''
            filename = prefix + str(target) + '.docx'
            path = os.path.join(self.tmode_path, filename)
            self.build_docx(HUMIDITY_MODE_TPL, ctx, path)
            page += 1

        for mode in hmodes:
            ctx = self.build_humidity_mode_ctx(mode, page)
            t_target = str(mode['mode']['target']['temperature'])
            h_target = str(mode['mode']['target']['humidity'])
            filename = '_'.join([t_target, h_target]) + '.docx'
            path = os.path.join(self.hmode_path, filename)
            self.build_docx(TEMPERATURE_MODE_TPL, ctx, path)
            page += 1

    def build_main(self):
        ctx = self.build_main_ctx(self.test)
        system_description = self.test.data['system']['name'] or 'UNKNOWN_SYSTEM'
        filename = 'Протокол аттестации ' + system_description + '.docx'
        path = os.path.join(self.report_path, filename)
        self.build_docx(MAIN_TPL, ctx, path)
