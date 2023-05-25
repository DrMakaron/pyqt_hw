"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from b_systeminfo_widget import SysInfoWidget
from c_weatherapi_widget import WeatherWidget


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.sys_widget = SysInfoWidget()
        self.weather_widget = WeatherWidget()

        self.setupUI()

    def setupUI(self):
        layout_sys = QtWidgets.QHBoxLayout()
        layout_weather = QtWidgets.QHBoxLayout()
        layout_main = QtWidgets.QVBoxLayout()

        layout_sys.addWidget(self.sys_widget)
        layout_weather.addWidget(self.weather_widget)

        layout_main.addLayout(layout_sys)
        layout_main.addLayout(layout_weather)

        self.setLayout(layout_main)
        self.setWindowTitle('AppName')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    app.exec()
