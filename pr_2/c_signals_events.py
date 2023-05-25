"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""

import sys
from dataclasses import dataclass
from datetime import datetime as dt
from collections import namedtuple

from PyQt5 import QtWidgets  # сделал на PyQt5 вмето PySide6 т.к на Linux PySide6 некорректно работает

from ui import c_form


@dataclass
class WindowCoordinates:
    pos_x: int
    pos_y: int


class Window(QtWidgets.QWidget, c_form.Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.coordinates = WindowCoordinates(0, 0)

        self.default()
        self.initSignals()

    def resizeEvent(self, a0):
        print(self.getWindowSize('current'))

    def moveEvent(self, a0):
        print(self.pos(), a0.pos(), a0.oldPos())

    def default(self):
        self.spinBoxX.setAccessibleName('x')
        self.spinBoxY.setAccessibleName('y')
        self.pushButtonCenter.setAccessibleName('center')
        self.pushButtonLT.setAccessibleName('lt')
        self.pushButtonRT.setAccessibleName('rt')
        self.pushButtonLB.setAccessibleName('lb')
        self.pushButtonRB.setAccessibleName('rb')

    def initSignals(self):
        self.spinBoxX.valueChanged.connect(self.updateWindowCoordinates)
        self.spinBoxY.valueChanged.connect(self.updateWindowCoordinates)
        self.pushButtonMoveCoords.clicked.connect(self.moveWindowToCoodinates)
        self.pushButtonGetData.clicked.connect(self.showScreenData)
        self.pushButtonCenter.clicked.connect(self.moveWindowToPos)
        self.pushButtonLT.clicked.connect(self.moveWindowToPos)
        self.pushButtonRT.clicked.connect(self.moveWindowToPos)
        self.pushButtonLB.clicked.connect(self.moveWindowToPos)
        self.pushButtonRB.clicked.connect(self.moveWindowToPos)

    @staticmethod
    def decorateToNamedTuple(name, fields, values):
        nt = namedtuple(name, fields)
        return nt(*values)

    def updateWindowCoordinates(self):
        sender = self.sender()

        if sender.accessibleName() == 'x':
            self.coordinates.pos_x = sender.value()
        if sender.accessibleName() == 'y':
            self.coordinates.pos_y = sender.value()

    def moveWindowToCoodinates(self):
        self.move(self.coordinates.pos_x, self.coordinates.pos_y)

    def moveWindowToPos(self):
        sender = self.sender()
        place = sender.accessibleName()
        screen = self.getConnectedScreens()[0]
        screen_geometry = screen.availableGeometry()
        window_size = self.getWindowSize('current')

        match place:
            case 'center':
                self.move(int(screen_geometry.width() / 2 - window_size.x / 2),
                          int(screen_geometry.height() / 2 - window_size.y / 2))
            case 'lt':
                self.move(screen_geometry.x(), screen_geometry.y())
            case 'rt':
                self.move(int(screen_geometry.width() - window_size.x), screen_geometry.y())
            case 'lb':
                self.move(screen_geometry.x(), screen_geometry.height() - window_size.y)
            case 'rb':
                self.move(int(screen_geometry.width() - window_size.x), screen_geometry.height() - window_size.y)

    @staticmethod
    def getConnectedScreens():
        return QtWidgets.QApplication.screens()

    @staticmethod
    def getScreenResolution():
        return [str(i + 1) + ": " + str(screen.size().width()) + "x" + str(screen.size().height())
                for i, screen in enumerate(QtWidgets.QApplication.screens())]

    def getWindowSize(self, flag: str):
        x = None
        y = None

        if flag == 'current':
            x = self.size().width()
            y = self.size().height()
        if flag == 'minimal':
            x = self.minimumSize().width()
            y = self.minimumSize().height()

        return self.decorateToNamedTuple('Size', 'x y', (x, y))

    def getWindowCoordinates(self):
        return self.decorateToNamedTuple('WindowCoordinates', 'x y', (self.pos().x(), self.pos().y()))

    def getWindowCenterCoordinates(self):
        x = self.pos().x() + self.size().width() / 2
        y = self.pos().y() + self.size().height() / 2
        return self.decorateToNamedTuple('WindowCenter', 'x y', (x, y))

    def getWindowStatus(self):
        return f'Minimized={self.isMinimized()}, ' \
               f'Maximized={self.isMaximized()}, ' \
               f'Active={self.isActiveWindow()}, ' \
               f'Visible={self.isVisible()}'

    def showScreenData(self):
        info_string = f'{dt.now()}\n'\
                      f'Screens quantity: {len(self.getConnectedScreens())}\n' \
                      f'Current active window:\n' \
                      f'Screens resolution: {self.getScreenResolution()}\n' \
                      f'Window on screen: \n' \
                      f'Window size: {self.getWindowSize("current")}\n' \
                      f'Minimal window size: {self.getWindowSize("minimal")}\n' \
                      f'Current window coordinates: {self.getWindowCoordinates()}\n' \
                      f'Window center coordinates: {self.getWindowCenterCoordinates()}\n' \
                      f'Window condition: {self.getWindowStatus()}'

        self.plainTextEdit.setPlainText(info_string)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()

    app.exec()
