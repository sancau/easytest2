# -*- coding: utf-8 -*-

"""
Easytest 2 UI Application
"""
import datetime
import json
import sys

from dateutil import parser

from PyQt5 import uic, QtWidgets as QW
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QListWidgetItem

from bl.easytest import Test


class EasyTest(QW.QMainWindow):
    def __init__(self):
        super(EasyTest, self).__init__()
        uic.loadUi('easytest2.ui', self)
        self.test = None

        with open('inventory_data/systems.json', 'r', encoding='utf-8') as f:
            self.db_systems = json.loads(f.read())

        with open('inventory_data/tools.json', 'r', encoding='utf-8') as f:
            self.db_tools = json.loads(f.read())

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

    def on_system_select(self, name):
        def get_verbose_key(k):
            """Returns user friendly repr for a system dict key"""
            return k.upper()  # not implemented yet

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
                for k, v in system.items():
                    list_item = QListWidgetItem('{} - {}'.format(get_verbose_key(k), v))
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
