"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатие на кнопку
"""

import sys
from typing import NamedTuple

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from loguru import logger

from ui import weather_info
from a_threads import WeatherHandler


class Coordinates(NamedTuple):
    latitude: int
    longitude: int


class WeatherWidget(QtWidgets.QWidget, weather_info.Ui_Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.coordinates = None
        self.weather = WeatherHandler()

        self.default()
        self.initSignals()

    def default(self):
        self.pushButton.setText('START')
        self.temperature.setAccessibleName('temperature')
        self.wind_speed.setAccessibleName('windspeed')

    def initSignals(self):
        self.pushButton.clicked.connect(self.startWeatherMonitor)
        self.weather.weather_response.connect(self.showWeather)

    @pyqtSlot()
    def startWeatherMonitor(self):
        self.updateButtonText()
        self.defineCoordinates()
        self.blockSetupWidgets()
        self.controlWeatherMonitor()

    def updateButtonText(self):
        sender = self.sender()
        if sender.isChecked():
            text = 'STOP'
        else:
            text = 'START'

        sender.setText(text)

    def defineCoordinates(self):
        sender = self.sender()
        if sender.isChecked():
            self.coordinates = Coordinates(latitude=self.spinBox.value(), longitude=self.spinBox_2.value())
            logger.info(self.coordinates)

    def blockSetupWidgets(self):
        sender = self.sender()

        for element in self.findChildren(QtWidgets.QSpinBox):
            element.setDisabled(sender.isChecked())

    def controlWeatherMonitor(self):
        sender = self.sender()
        self.weather.setStatus(sender.isChecked())
        self.weather.setDelay(self.spinBox_3.value())
        self.weather.buildRequest(self.coordinates)

        if sender.isChecked():
            self.weather.start()

    def showWeather(self, data):
        weather_data = data['current_weather']
        logger.info(weather_data)
        for element in self.findChildren(QtWidgets.QLabel):
            if element.accessibleName() in weather_data.keys():
                element.setText(str(weather_data[element.accessibleName()]))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = WeatherWidget()
    window.show()

    app.exec()
