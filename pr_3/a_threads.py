"""
Модуль в котором содержаться потоки Qt
"""

import time
import requests
from typing import NamedTuple

from loguru import logger
import psutil
from PyQt5 import QtCore


class SysInfo(NamedTuple):
    cpu_usage: float
    ram_usage: float


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.pyqtSignal(SysInfo) # TODO Создайте экземпляр класса Signal и передайте ему в конструктор тип данных передаваемого значения (в текущем случае list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # TODO создайте атрибут класса self.delay = None, для управлением задержкой получения данных
        logger.info(f'{__class__.__name__}: {self.__dict__}')

    def run(self) -> None:  # TODO переопределить метод run
        if self.delay is None:  # TODO Если задержка не передана в поток перед его запуском
            self.delay = 1  # TODO то устанавливайте значение 1

        while True:  # TODO Запустите бесконечный цикл получения информации о системе
            cpu_value = psutil.cpu_percent()  # TODO с помощью вызова функции cpu_percent() в пакете psutil получите загрузку CPU
            ram_value = psutil.virtual_memory()  # TODO с помощью вызова функции virtual_memory().percent в пакете psutil получите загрузку RAM
            self.systemInfoReceived.emit(SysInfo(cpu_usage=cpu_value, ram_usage=ram_value.percent))  # TODO с помощью метода .emit передайте в виде списка данные о загрузке CPU и RAM
            time.sleep(self.delay)  # TODO с помощью функции .sleep() приостановите выполнение цикла на время self.delay


class WeatherHandler(QtCore.QThread):
    # TODO Пропишите сигналы, которые считаете нужными

    weather_response = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__api_url = None
        self.__delay = 10
        self.__status = None
        logger.info(f'{__class__.__name__}: {self.__dict__}')

    def buildRequest(self, coordinates):
        logger.info(coordinates)
        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude=" \
                         f"{coordinates.latitude}&longitude={coordinates.longitude}&current_weather=true"

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта

        :param delay: время задержки обновления информации о доступности сайта
        :return: None
        """

        self.__delay = delay
        logger.info(f'Delay updated: {delay}')

    def setStatus(self, status):
        self.__status = status
        logger.info(f'Status updated: {status} {self.__status=}')

    def run(self) -> None:
        # TODO настройте метод для корректной работы

        self.__status = True

        while self.__status:
            response = requests.get(self.__api_url)
            data = response.json()
            self.weather_response.emit(data)
            time.sleep(self.__delay)
