# -*- coding: utf-8 -*-

"""
Easytest 2 UI Application
"""
import datetime
import json
import sys
import traceback

import requests

from dateutil import parser

from PyQt5 import uic, QtWidgets as QW
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QListWidgetItem

from bl.easytest import Test


class TMode(QW.QWidget):
    def __init__(self, mode=None, parent=None):
        super(TMode, self).__init__()
        uic.loadUi('tmode.ui', self)
        self.is_edit = bool(mode)
        self.mode = mode if mode else {
            'logs': [],
            'target': None,
            'cp': [],
            'md': []
        }
        if not self.is_edit:  # if it's new mode hide the delete button
            self.remove.hide()
        self.parent = parent
        self.setAcceptDrops(True)
        self.bind_ui()

    def bind_ui(self):
        self.target.setText(self.mode['target'])
        self.cp_values.setText(' | '.join(self.mode['cp']))
        self.md_values.setText(' | '.join(self.mode['md']))

        for log in self.mode['logs']:
            list_item = QListWidgetItem('{} (датчиков: {})'.format(log['file'],
                                                                   log['sensors_count']))
            self.logs.addItem(list_item)

        self.save.clicked.connect(self.save_tmode)
        self.remove.clicked.connect(self.remove_mode)
        self.target.textEdited.connect(self.on_target_edit)
        self.cp_values.textEdited.connect(self.on_cp_edit)
        self.md_values.textEdited.connect(self.on_md_edit)
        self.logs.itemDoubleClicked.connect(self.on_logs_doubleclick)

    def on_target_edit(self, value):
        self.mode['target'] = value
        if value:
            default_cp_and_md = ' | '.join([value + '.0' for i in range(10)])
        else:
            default_cp_and_md = None

        self.cp_values.setText(default_cp_and_md)
        self.md_values.setText(default_cp_and_md)
        self.mode['cp'] = [v for v in default_cp_and_md.split(' | ')]
        self.mode['md'] = [v for v in default_cp_and_md.split(' | ')]

    def save_tmode(self):
        try:
            if self.is_edit:
                self.parent.update_test_widget()
            else:
                self.parent.test.add_temperature_mode(self.mode)
                list_item = QListWidgetItem('Режим {}. Файлов: {}'.format(self.mode['target'],
                                                                          len(self.mode['logs'])))
                self.parent.tmodes_list.addItem(list_item)
            self.close()
        except Exception as e:
            print(e)

    def remove_mode(self):
        try:
            reply = QW.QMessageBox.question(self,
                                            'Подтвердите дейтсвие',
                                            'Вы действительно удалить данный режим? ',
                                            QW.QMessageBox.Yes | QW.QMessageBox.No,
                                            QW.QMessageBox.No)
            if reply == QW.QMessageBox.Yes:
                to_remove = [i for i in self.parent.test.data['temperature'] \
                             if i['mode'] == self.mode]
                if to_remove:
                    to_remove = to_remove[0]
                self.parent.test.data['temperature'].remove(to_remove)
                self.parent.update_test_widget()
                self.close()
            else:
                return
        except Exception as e:
            print(e)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [str(u.toLocalFile()) for u in event.mimeData().urls()]
        for f in files:
            num, ok = QW.QInputDialog.getInt(self,
                                             'Параметры файла лога',
                                             'Количество датчиков (файл {}):'.format(f))
            if ok and num > 0:
                list_item = QListWidgetItem('{} (датчиков: {})'.format(f, num))
                self.logs.addItem(list_item)
                self.mode['logs'].append({'file': f, 'sensors_count': str(num)})

    def on_cp_edit(self, val):
        self.mode['cp'] = [v for v in val.split(' | ')]

    def on_md_edit(self, val):
        self.mode['md'] = [v for v in val.split(' | ')]

    def on_logs_doubleclick(self, item):
        self.logs.takeItem(self.logs.row(item))
        clicked_file = item.text().split(' ')[0]
        log = [i for i in self.mode['logs'] if i['file'] == clicked_file]
        if not log:
            return
        self.mode['logs'].remove(log[0])


class HMode(QW.QWidget):
    def __init__(self, mode=None, parent=None):
        super(HMode, self).__init__()
        uic.loadUi('hmode.ui', self)
        self.is_edit = bool(mode)
        self.mode = mode if mode else {
            'logs': [],
            'target': {
                'humidity': None,
                'temperature': None
            },
            'md': {
                'humidity': [],
                'temperature': []
            }
        }
        if not self.is_edit:  # if it's new mode hide the delete button
            self.remove.hide()
        self.parent = parent
        self.setAcceptDrops(True)
        self.bind_ui()

    def bind_ui(self):
        self.target_temp.setText(self.mode['target']['temperature'])
        self.target_hum.setText(self.mode['target']['humidity'])

        self.md_hum.setText(' | '.join(self.mode['md']['humidity']))
        self.md_temp.setText(' | '.join(self.mode['md']['temperature']))

        for log in self.mode['logs']:
            list_item = QListWidgetItem('{} (для {})'.format(log['file'],
                                                             log['desc']))
            self.logs.addItem(list_item)

        self.save.clicked.connect(self.save_hmode)
        self.remove.clicked.connect(self.remove_mode)

        self.target_temp.textEdited.connect(self.on_target_temp_edit)
        self.target_hum.textEdited.connect(self.on_target_hum_edit)

        self.md_hum.textEdited.connect(self.on_md_hum_edit)
        self.md_temp.textEdited.connect(self.on_md_temp_edit)

        self.logs.itemDoubleClicked.connect(self.on_logs_doubleclick)

    def on_target_temp_edit(self, value):
        self.mode['target']['temperature'] = value
        if value:
            default_md_temp = ' | '.join([value + '.0' for i in range(10)])
        else:
            default_md_temp = None

        self.md_temp.setText(default_md_temp)
        self.mode['md']['temperature'] = [v for v in default_md_temp.split(' | ')]

    def on_target_hum_edit(self, value):
        self.mode['target']['humidity'] = value
        if value:
            default_md_hum = ' | '.join([value + '.0' for i in range(10)])
        else:
            default_md_hum = None

        self.md_hum.setText(default_md_hum)
        self.mode['md']['humidity'] = [v for v in default_md_hum.split(' | ')]

    def save_hmode(self):
        try:
            if self.is_edit:
                self.parent.update_test_widget()
            else:
                self.parent.test.add_humidity_mode(self.mode)
                list_item = QListWidgetItem(
                    'Режим {}/{}. Файлов: {}'.format(self.mode['target']['temperature'],
                                                     self.mode['target']['humidity'],
                                                     len(self.mode['logs'])))

                self.parent.hmodes_list.addItem(list_item)
            self.close()
        except Exception as e:
            print(e)

    def remove_mode(self):
        try:
            reply = QW.QMessageBox.question(self,
                                            'Подтвердите дейтсвие',
                                            'Вы действительно удалить данный режим? ',
                                            QW.QMessageBox.Yes | QW.QMessageBox.No,
                                            QW.QMessageBox.No)
            if reply == QW.QMessageBox.Yes:
                to_remove = [i for i in self.parent.test.data['humidity'] \
                             if i['mode'] == self.mode]
                if to_remove:
                    to_remove = to_remove[0]
                self.parent.test.data['humidity'].remove(to_remove)
                self.parent.update_test_widget()
                self.close()
            else:
                return
        except Exception as e:
            print(e)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [str(u.toLocalFile()) for u in event.mimeData().urls()]
        items = ['DT1', 'DT2', 'KT']
        for f in files:
            item, ok = QW.QInputDialog.getItem(self,
                                               'Параметры файла лога',
                                               'Использовать как (файл {}):'.format(f), items)
            if ok and item:
                list_item = QListWidgetItem('{} ({})'.format(f, item))
                self.logs.addItem(list_item)
                self.mode['logs'].append({'file': f, 'desc': str(item)})

    def on_md_hum_edit(self, val):
        self.mode['md']['humidity'] = [v for v in val.split(' | ')]

    def on_md_temp_edit(self, val):
        self.mode['md']['temperature'] = [v for v in val.split(' | ')]

    def on_logs_doubleclick(self, item):
        self.logs.takeItem(self.logs.row(item))
        clicked_file = item.text().split(' ')[0]
        log = [i for i in self.mode['logs'] if i['file'] == clicked_file]
        if not log:
            return
        self.mode['logs'].remove(log[0])


class EasyTest(QW.QMainWindow):
    def __init__(self):
        super(EasyTest, self).__init__()
        uic.loadUi('easytest2.ui', self)
        self.test = None
        self.children = []

        systems = [] # requests.get('http://sqlisp:5000/inventory/systems').json()
        systems = [s for s in systems if s['purpose'] == 'climatic']
        self.db_systems = sorted(systems, key=lambda s: (s['name']))

        tools = [] # requests.get('http://sqlisp:5000/inventory/tools').json()
        self.db_tools = tools

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('EasyTest 2')
        self.tabWidget.close()
        self.init_menu()
        self.bind_test_to_ui()
        self.init_db_integrated_controls()
        self.show()

    def init_menu(self):  # initialize top menu
        self.exit.triggered.connect(self.close)
        self.new_test.triggered.connect(self.init_new_test_handler)
        self.open_test.triggered.connect(self.open_test_handler)
        self.save.triggered.connect(self.save_test_handler)
        self.save_as.triggered.connect(self.save_test_as_handler)
        self.create_report.triggered.connect(self.create_report_handler)

    def bind_test_to_ui(self):
        def bind(field, value):
            self.test.data[field] = value
        self.specialist.textEdited.connect(lambda x: bind('specialist', x))
        self.test_start_date.dateChanged.connect(lambda x: bind('test_start_date',
                                                                x.toString('yyyy-MM-dd')))
        self.test_end_date.dateChanged.connect(lambda x: bind('test_end_date',
                                                              x.toString('yyyy-MM-dd')))

        self.system_select.activated[str].connect(self.on_system_select)
        self.tools_available.itemDoubleClicked.connect(self.on_available_tool_doubleclick)
        self.tools_selected.itemDoubleClicked.connect(self.on_selected_tool_doubleclick)

        # modes
        self.btn_add_tmode.clicked.connect(self.on_add_tmode_click)
        self.btn_add_hmode.clicked.connect(self.on_add_hmode_click)
        self.tmodes_list.itemDoubleClicked.connect(self.on_tmode_doubleclick)
        self.hmodes_list.itemDoubleClicked.connect(self.on_hmode_doubleclick)

    def init_db_integrated_controls(self):
        # Systems
        systems = [i['name'] for i in self.db_systems]
        items = ['Не выбрана']
        items.extend(systems)
        self.system_select.addItems(items)

        # Tools
        for tool in sorted(self.db_tools, key=lambda tool: (tool['name'])):
            list_item = QListWidgetItem(tool['name'])
            self.tools_available.addItem(list_item)

    # MENU ACTION HANDLERS
    ################################################################################################
    def init_new_test_handler(self):

        def execute():
            self.test = Test()
            self.update_test_widget()
            self.tabWidget.show()
            self.setWindowTitle('EasyTest 2 - Новая аттестация')
            self.save_as.setEnabled(True)
            self.save.setEnabled(False)
            self.create_report.setEnabled(True)

        if self.test:
            reply = QW.QMessageBox.question(self,
                                            'Подтвердите дейтсвие',
                                            'Вы действительно хотите создать новую аттестацию? ' +
                                            'Все несохранённые изменения будут потеряны!',
                                            QW.QMessageBox.Yes | QW.QMessageBox.No,
                                            QW.QMessageBox.No)
            if reply == QW.QMessageBox.Yes:
                execute()
            else:
                return
        else:
            execute()

    def open_test_handler(self):

        def execute():
            fname = QW.QFileDialog.getOpenFileName(self, 'Окрыть файл аттестации', '.',
                                                   filter='*.et2')
            if not fname[0]:
                return
            else:
                try:
                    self.test = Test(fname[0])  # init Test object
                    self.update_test_widget()  # push data to UI
                    self.tabWidget.show()
                    self.setWindowTitle('EasyTest 2 - ' + fname[0])
                    self.save_as.setEnabled(True)
                    self.save.setEnabled(True)
                    self.create_report.setEnabled(True)
                except Exception as e:
                    print(e)

        if self.test:
            reply = QW.QMessageBox.question(self,
                                            'Подтвердите дейтсвие',
                                            'Вы действительно хотите открыть другую аттестацию? ' +
                                            'Все несохранённые изменения будут потеряны!',
                                            QW.QMessageBox.Yes | QW.QMessageBox.No,
                                            QW.QMessageBox.No)

            if reply == QW.QMessageBox.Yes:
                execute()
            else:
                return
        else:
            execute()

    def save_test_handler(self):
        self.test.save()
        self.statusBar().showMessage('Сохранено', 2000)

    def save_test_as_handler(self):
        fname = QW.QFileDialog.getSaveFileName(self, 'Выберите путь для сохранения', '.et2',
                                               filter='*.et2')
        if not fname[0]:
            return
        else:
            try:
                self.test.save_as(fname[0])
                self.save.setEnabled(True)
                self.statusBar().showMessage('Сохранено в {}'.format(fname[0]), 3000)
            except Exception as e:
                print(e)

    def create_report_handler(self):
        try:
            dir_name = QW.QFileDialog.getExistingDirectory(self, 'Выберите путь для создания протокола')
            if not dir_name:
                return
            else:
                self.test.create_report(dir_name)
                msg = QW.QMessageBox()
                msg.setIcon(QW.QMessageBox.Information)
                msg.setText('Протокол для расчитанных режимов успешно создан в {}'.format(dir_name))
                msg.setWindowTitle('Все готово')
                msg.setStandardButtons(QW.QMessageBox.Ok)
                msg.exec_()
        except Exception as e:
            print(e)
            et, ev, tb = sys.exc_info()
            msg = QW.QMessageBox()
            msg.setIcon(QW.QMessageBox.Information)
            msg.setText(
                'Ошибка {} при создании протокола: {} Traceback: {}'.format(et, ev,
                                                                            traceback.format_tb(
                                                                                tb)))
            msg.setWindowTitle('Ошибка')
            msg.setStandardButtons(QW.QMessageBox.Ok)
            msg.exec_()

    # HELPERS
    ################################################################################################
    def update_test_widget(self):
        data = self.test.data
        self.specialist.setText(data['specialist'])

        start_date = parser.parse(data['test_start_date']) if data['test_start_date'] else \
            datetime.date.today()

        end_date = parser.parse(data['test_end_date']) if data['test_end_date'] else \
            datetime.date.today()

        self.test_start_date.setDate(start_date)
        self.test_end_date.setDate(end_date)

        # system select
        system = data['system']
        name = system['name'] if system else 'Не выбрана'
        index = self.system_select.findText(name)
        if index >= 0:
            self.system_select.setCurrentIndex(index)
        self.on_system_select(name)

        # selected tools  TODO maybe there's a need for a check if a tool from saved test is in db
        self.tools_selected.clear()
        for tool in sorted(data['tools'], key=lambda t: (t['name'])):
            list_item = QListWidgetItem(tool['name'])
            self.tools_selected.addItem(list_item)

        # tmodes
        self.tmodes_list.clear()
        for tmode in sorted(data['temperature'], key=lambda m: (m['mode']['target'])):
            mode = tmode['mode']
            list_item = QListWidgetItem('Режим {}. Файлов: {}'.format(mode['target'],
                                                                      len(mode['logs'])))
            self.tmodes_list.addItem(list_item)

        # hmodes
        self.hmodes_list.clear()
        for hmode in sorted(data['humidity'], key=lambda m: (m['mode']['target']['temperature'])):
            mode = hmode['mode']
            list_item = QListWidgetItem(
                'Режим {}/{}. Файлов: {}'.format(mode['target']['temperature'],
                                                 mode['target']['humidity'],
                                                 len(mode['logs'])))
            self.hmodes_list.addItem(list_item)

    def on_system_select(self, name):
        display_keys = [
            'name', 'manufacturer', 'yearOfProduction',
            'code', 'inventoryNumber', 'actualPlacement', 'techDetails', 'comment'
        ]

        def get_verbose_key(k):
            """Returns user friendly repr for a system dict key"""
            mapping = {
                'name': 'Наименование',
                'manufacturer': 'Производитель',
                'yearOfProduction': 'Год выпуска',
                'code': 'Код',
                'inventoryNumber': 'Инвентарный номер',
                'actualPlacement': 'Расположение',
                'comment': 'Примечание',
                'techDetails': 'Тех. характеристики'
            }
            return mapping.get(k, k)

        self.system_info.clear()

        if name == 'Не выбрана':
            self.test.data['system'] = None
        else:
            tmp = [i for i in self.db_systems if i['name'] == name]
            if len(tmp) != 1:
                raise LookupError('Zero or more then one system found by name: {}'.format(name))
            else:
                system = tmp[0]
                self.test.data['system'] = system

                # system info code
                for k in display_keys:
                    list_item = QListWidgetItem('{} - {}'.format(get_verbose_key(k), system[k]))
                    self.system_info.addItem(list_item)

    def on_available_tool_doubleclick(self, item):
        selected_tools = [self.tools_selected.item(i) for i in range(self.tools_selected.count())]

        selected_names = [i.text() for i in selected_tools]

        clicked_name = item.text()

        if clicked_name not in selected_names:
            list_item = QListWidgetItem(clicked_name)
            self.tools_selected.addItem(list_item)

        in_test = [t['name'] for t in self.test.data['tools']]
        if clicked_name in in_test:
            return
        tool = [i for i in self.db_tools if i['name'] == clicked_name]
        if not tool:
            raise LookupError('Could not find tool in db')
        self.test.data['tools'].append(tool[0])

    def on_selected_tool_doubleclick(self, item):
        self.tools_selected.takeItem(self.tools_selected.row(item))
        clicked_name = item.text()
        tool = [i for i in self.test.data['tools'] if i['name'] == clicked_name]
        if not tool:
            return
        self.test.data['tools'].remove(tool[0])

    def on_add_tmode_click(self):
        tmode_window = TMode(parent=self)
        self.children.append(tmode_window)
        tmode_window.show()

    def on_add_hmode_click(self):
        hmode_window = HMode(parent=self)
        self.children.append(hmode_window)
        hmode_window.show()

    def on_tmode_doubleclick(self, item):
        text = item.text()
        target = text.split('.')[0]
        target = target.split(' ')[1]
        mode = [i for i in self.test.data['temperature'] if i['mode']['target'] == target]
        if mode:
            mode = mode[0]['mode']
        tmode_window = TMode(parent=self, mode=mode)
        self.children.append(tmode_window)
        tmode_window.show()

    def on_hmode_doubleclick(self, item):
        text = item.text()
        text = text.split('.')[0]
        text = text.split(' ')[1]
        target_temp, target_hum = text.split('/')
        mode = [i for i in self.test.data['humidity'] if \
                i['mode']['target']['temperature'] == target_temp and \
                i['mode']['target']['humidity'] == target_hum]
        if mode:
            mode = mode[0]['mode']
        hmode_window = HMode(parent=self, mode=mode)
        self.children.append(hmode_window)
        hmode_window.show()

    # EVENT OVERLOADING
    ################################################################################################
    def closeEvent(self, event):
        reply = QW.QMessageBox.question(self,
                                        'Выход из программы',
                                        'Вы действительно хотите выйти? ' +
                                        'Все несохранённые изменения будут потеряны!',
                                        QW.QMessageBox.Yes | QW.QMessageBox.No,
                                        QW.QMessageBox.No)

        if reply == QW.QMessageBox.Yes:
            for w in self.children:
                w.close()  # close all the children
            event.accept()

        else:
            event.ignore()

if __name__ == '__main__':
    app = QW.QApplication(sys.argv)

    # localization
    qtTranslator = QTranslator()
    if qtTranslator.load('translations\qtbase_ru'):
        app.installTranslator(qtTranslator)

    window = EasyTest()
    sys.exit(app.exec_())
