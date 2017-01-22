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
        return {
            'report': {
                'date': get_verbose_date(datetime.now()),
                'number': 'НОМЕР ПРОТОКОЛА',
                'specialist': test.data['specialist'],
                'responsible_specialist': test.data['responsible_specialist'],
                'total_additions_count': len(test.data['humidity']) + len(test.data['temperature'])
            },
            'system': {
                'name': 'НАЗВАНИЕ СИСТЕМЫ',
                'year_of_production': 'ГОД ВЫПУСКА',
                'manufacturer': 'ИЗГОТОВИТЕЛЬ',
                'factory_number': 'ЗАВ. НОМЕР',
                'description': 'ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ',
                'test_program': 'ПРОГРАММА АТТЕСТАЦИИ',
                'test_method': 'МЕТОДИКА АТТЕСТАЦИИ',
            },
            'tools': [
                'ПРИБОР 1',
                'ПРИБОР 2',
                'ПРИБОР 3',
                'ПРИБОР 4',
                'ПРИБОР 5'
            ],
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
                    'hmax_md_delta': 'МАКС. ПОГРЕШНОСТЬ ИУ ВЛАГИ',
                },
                'tmodes': [  # TODO sort by target_temp
                    {
                        'verbose_temp': 'РЕЖИМ 1',
                        'positive_delta': 'ПОЛОЖИТЕЛЬНОЕ ОТКЛОНЕНИЕ ТЕМП.',
                        'negative_delta': 'ОТРИЦАТЕЛЬНОЕ ОТКЛОНЕНИЕ ТЕМП.',
                        'md_delta': 'ПОГРЕШНОСТЬ ИУ',
                        'positive_total_error': 'ПОЛ. СУММ. ПОГРЕШНОСТЬ Т',
                        'negative_total_error': 'ОТР. СУММ. ПОГРЕШНОСТЬ Т',
                        'verbose_max_deviation': 'ДОПУСК Т',
                    }
                ],
                'hmodes': [  # TODO sort by target_hum then by target_temp
                    {
                        'verbose_hum': 'РЕЖИМ 1 (ВЛАГА)',
                        'verbose_temp': 'РЕЖИМ 1 (ТЕМПЕРАТУРА)',
                        'positive_delta': 'ПОЛОЖИТЕЛЬНОЕ ОТКЛОНЕНИЕ ВЛАГИ',
                        'negative_delta': 'ОТРИЦАТЕЛЬНОЕ ОТКЛОНЕНИЕ ВЛАГИ',
                        'md_delta': 'ПОГРЕШНОСТЬ ИУ',
                        'positive_total_error': 'ПОЛ. СУММ. ПОГРЕШНОСТЬ ВЛ',
                        'negative_total_error': 'ОТР. СУММ. ПОГРЕШНОСТЬ ВЛ',
                        'verbose_max_deviation': 'ДОПУСК ВЛАГА',
                    }
                ]
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
        system_description = self.test.data['system'] or 'UNKNOWN_SYSTEM'
        filename = 'Протокол аттестации ' + system_description + '.docx'
        path = os.path.join(self.report_path, filename)
        self.build_docx(MAIN_TPL, ctx, path)
