# -*- coding: utf-8 -*-

"""
Easytest 2 UI Application
"""
import datetime
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
        self.db_systems = [
            {
                '_id': '1',
                'name': 'System 1'
            },
            {
                '_id': '2',
                'name': 'System 2'
            }
        ]
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

    def init_db_integrated_controls(self):
        # Systems
        systems = [i['name'] for i in self.db_systems]
        items = ['Не выбрана']
        items.extend(systems)
        self.system_select.addItems(items)

        # Tools
        # ...

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
