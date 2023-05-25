"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

import sys

from loguru import logger
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot

from ui import d_form


class Window(QtWidgets.QWidget, d_form.Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.settings = QtCore.QSettings('Home', 'DevQT_lab2_d')

        self.lcd_modes = {'dec': QtWidgets.QLCDNumber.Mode.Dec,
                          'hex': QtWidgets.QLCDNumber.Mode.Hex,
                          'bin': QtWidgets.QLCDNumber.Mode.Bin,
                          'oct': QtWidgets.QLCDNumber.Mode.Oct}

        self.whereIsMySettings()
        self.setupWindow()
        self.initSignals()

    def whereIsMySettings(self):
        logger.info(f'Settings path: {self.settings.fileName()}')

    def setupWindow(self):
        self.resize(800, 600)

        for element in self.lcd_modes.keys():
            self.comboBox.addItem(element)

        self.comboBox.setCurrentIndex(int(self.settings.value('Mode', 0)))
        self.lcdNumber.display(self.settings.value('LCD', 0))

        self.setupLcd(self.comboBox.currentText())

    def initSignals(self):
        self.dial.valueChanged.connect(self.dialValueChanged)
        self.horizontalSlider.valueChanged.connect(lambda: self.updateWidgetValue(self.dial))
        self.comboBox.currentIndexChanged.connect(self.comboBoxValueChanged)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Plus:
            self.dial.setValue(self.dial.value() + 1)
            logger.info(f'Dial value modified by button: {self.dial.value()}')
        if event.key() == Qt.Key_Minus:
            self.dial.setValue(self.dial.value() - 1)
            logger.info(f'Dial value modified by button: {self.dial.value()}')
        if event.key() == Qt.Key_F1:
            self.settings.clear()
            logger.info(f'Settings cleared! {self.settings.fileName()}')

    @pyqtSlot()
    def dialValueChanged(self):
        self.updateWidgetValue(self.horizontalSlider)
        self.showDialValue()

    @pyqtSlot()
    def comboBoxValueChanged(self):
        self.setupLcd(self.comboBox.currentText())
        self.saveLcdMode()

    def updateWidgetValue(self, slave_widget):
        sender = self.sender()
        slave_widget.setValue(sender.value())

    def showDialValue(self):
        sender = self.sender()
        self.lcdNumber.display(sender.value())
        self.settings.setValue('LCD', sender.value())
        logger.info(f'LCD value "{sender.value()}" saved to settings!')

    def setupLcd(self, mode):
        mode_ = self.lcd_modes.get(mode)
        self.lcdNumber.setMode(mode_)
        logger.info(f'Current LCD mode is: {mode_}')

    def saveLcdMode(self):
        self.settings.setValue('Mode', self.comboBox.currentIndex())
        logger.info(f'Mode "{self.comboBox.currentIndex()}" saved to settings!')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()

    app.exec()
