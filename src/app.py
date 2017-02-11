# -*- coding: utf-8 -*-

"""
Easytest2 UI Application
"""

from PyQt5 import uic, QtWidgets as QW
from PyQt5.QtCore import QTranslator, QObject, QVariant

import sys


class EasyTest(QW.QMainWindow):
    def __init__(self):
        super(EasyTest, self).__init__()
        uic.loadUi('easytest2.ui', self)
        self.init_ui()

    def init_ui(self):
        self.test_active = False
        self.setWindowTitle('EasyTest 2')
        self.tabWidget.close()
        self.init_menu()
        self.show()

    def init_menu(self):  # initialize top menu
        self.exit.triggered.connect(self.close)
        self.new_test.triggered.connect(self.init_new_test)
        self.open_test.triggered.connect(self.open_test_handler)

    def init_new_test(self):
        if self.test_active:
            reply = QW.QMessageBox.question(self,
                                            'Подтвердите дейтсвие',
                                            'Вы действительно хотите создать новую аттестацию? ' +
                                            'Все несохранённые изменения будут потеряны!',
                                            QW.QMessageBox.Yes | QW.QMessageBox.No,
                                            QW.QMessageBox.No)

            if reply == QW.QMessageBox.Yes:
                self.clear_test_widget()
                self.test_active = True
                self.tabWidget.show()
                self.setWindowTitle('EasyTest 2 - Новая аттестация')
            else:
                return
        else:
            self.clear_test_widget()
            self.test_active = True
            self.tabWidget.show()
            self.setWindowTitle('EasyTest 2 - Новая аттестация')

    def open_test_handler(self):
        fname = QW.QFileDialog.getOpenFileName(self, 'Окрыть файл аттестации', '.')

        if not fname[0]:
            return
        else:
            try:
                print('Opening test from {}'.format(fname[0]))
            except Exception as e:
                print(e)

    def clear_test_widget(self):
        print('Clearing widget')

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
