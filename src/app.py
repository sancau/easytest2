# -*- coding: utf-8 -*-

"""
Easytest 2 UI Application
"""
import sys

from PyQt5 import uic, QtWidgets as QW
from PyQt5.QtCore import QTranslator

from bl.easytest import Test


class EasyTest(QW.QMainWindow):
    def __init__(self):
        super(EasyTest, self).__init__()
        uic.loadUi('easytest2.ui', self)
        self.test = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('EasyTest 2')
        self.tabWidget.close()
        self.init_menu()
        self.bind_test_to_ui()
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

    # MENU ACTION HANDLERS
    ################################################################################################

    def init_new_test_handler(self):

        def execute():
            self.test = Test()
            self.update_test_widget()
            self.tabWidget.show()
            self.setWindowTitle('EasyTest 2 - Новая аттестация')
            self.save_as.setEnabled(True)

            # NEW TEST INIT CODE

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
            fname = QW.QFileDialog.getOpenFileName(self, 'Окрыть файл аттестации', '.')
            if not fname[0]:
                return
            else:
                try:
                    self.test = Test(fname[0])  # init Test object
                    self.update_test_widget()  # push data to UI
                    self.tabWidget.show()
                    self.setWindowTitle('EasyTest 2 - ' + fname[0])

                    # OPEN TEST INIT CODE
                    print('Opening test from {}'.format(fname[0]))
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
        self.statusBar().showMessage('Аттестация сохранена', 2000)

    def save_test_as_handler(self):
        fname = QW.QFileDialog.getSaveFileName(self, 'Выберите путь для сохранения', '.')
        if not fname[0]:
            return
        else:
            try:
                self.test.save_as(fname[0] + '.json')
                self.save.setEnabled(True)

            except Exception as e:
                print(e)

    # HELPERS
    ################################################################################################

    def update_test_widget(self):
        pass

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
