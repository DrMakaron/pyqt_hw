"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""
import sys

from PyQt5 import QtWidgets

from ui import sys_info
from a_threads import SystemInfo


class SysInfoWidget(QtWidgets.QWidget, sys_info.Ui_Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.sys_info = SystemInfo()

        self.setupWindow()
        self.initSignals()
        self.startSysMonitor()

    def setupWindow(self):
        self.cpu_persent.setAccessibleName('cpu_usage')
        self.ram_persent.setAccessibleName('ram_usage')

    def initSignals(self):
        self.sys_info.systemInfoReceived.connect(self.showSysData)
        self.spinBox.valueChanged.connect(self.updateDelay)

    def startSysMonitor(self):
        self.sys_info.start()

    def showSysData(self, data):
        for element in self.findChildren(QtWidgets.QLabel):
            if element.accessibleName() in data._fields:
                element.setText(str(eval(f'data.{element.accessibleName()}')))

    def updateDelay(self):
        sender = self.sender()
        self.sys_info.delay = sender.value()
        self.sys_info.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = SysInfoWidget()
    window.show()

    app.exec()
