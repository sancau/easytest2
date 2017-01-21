# coding=utf-8
import os

from docxtpl import DocxTemplate

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
