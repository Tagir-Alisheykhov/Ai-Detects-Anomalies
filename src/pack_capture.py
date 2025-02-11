"""
Содержит класс для захвата пакетов сетевого трафика

"""

import logging
import os
from scapy.all import sniff, wrpcap, rdpcap

from src.cls_logger import Logger

log = Logger(
    filename=__name__ + "_debug",
    status_filewr=logging.DEBUG,
)
log = log.get_log()


class PackCapt:
    """
    Класс для захвата пакетов сетевого трафика,
    записи полученных данных в файл .pcap
    и с возможностью вывода данных.

    """

    time_capture: int
    count: int
    filename: str
    dir_name: str

    def __init__(
        self,
        count=0,
        time_capture_sec=86400,
        dir_name="data_traffic",
        filename="raw_traffic.pcap",
    ):
        """
        Инициализация параметров класса.
        :param count: Количество необходимых пакетов.
        :param time_capture_sec: Установка времени захвата трафика.
        :param filename: Имя файла для записи пакетов

        """
        self.count = count
        self.time_capture = time_capture_sec
        self.dir_name = dir_name
        self.file_name = filename
        self.path_to_file = self.__path_create(self.dir_name, self.file_name)
        log.debug("Захват сетевого трафика")

    @staticmethod
    def __path_create(directory_name: str, filename: str):
        """
        Формирование пути до файла
        :param directory_name:
        :param filename:
        :return: Полный путь до файла

        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_dir = os.path.join(base_dir, directory_name)
        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)
        return os.path.join(path_to_dir, filename)

    def write_packs_pcap_time(self):
        """
        Создание и запись файла с данными в формате .pcap.

        """
        log.debug("Запись пакетов в файл (по времени)")
        try:
            if isinstance(self.time_capture, int):
                packs = sniff(timeout=self.time_capture)
                wrpcap(self.path_to_file, packs)
            else:
                raise TypeError(
                    f"Неверный тип данных: {self.count}.\nОжидался: `integer`."
                )
        except Exception as err:
            log.error(f"Возникла ошибка: {err}")

    def write_packs_pcap_count(self):
        """
        Создание и запись файла с данными в формате .pcap.

        """
        log.debug("Запись пакетов в файл (по количеству)")

        try:
            if isinstance(self.count, int):
                packs = sniff(count=self.count)
                wrpcap(self.path_to_file, packs)
            else:
                raise TypeError(
                    f"Неверный тип данных {self.count}.\nОжидался `integer`."
                )
        except Exception as err:
            log.error(f"Возникла ошибка: {err}")

    def read_packs_pcap(self):
        """
        Чтение сохраненных данных.
        :return: Пакеты сетевого трафика

        """
        log.debug("Вывод данных")
        try:
            return rdpcap(self.path_to_file)
        except Exception as err:
            log.error(f"Возникла ошибка: {err}")
