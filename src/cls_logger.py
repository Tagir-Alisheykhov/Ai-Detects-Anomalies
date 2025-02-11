"""
Содержит класс для логирования событий при работе программы
и вывода информации в консоль в реальном времени.

"""

import os
import logging


class Logger:
    """
    Класс для отслеживания
    событий в программе.

    """

    filename: str
    console: bool
    filewr: bool

    def __init__(
        self,
        filename=__name__,
        console=False,
        filewr=True,
        status_console=logging.DEBUG,
        status_filewr=logging.DEBUG,
        setlevel=logging.DEBUG,
    ):
        """
        Инициализация параметров
        :param console: Вывод лога в консоль, по умолчанию - False (Нет).
        :param filewr: Запись лога в файл, по умолчанию - True (Да).
        :param status_console: Класс `logger` и статус для вывода (напр. DEBUG).
        :param status_filewr: Класс `logger` и статус для вывода (напр. DEBUG).

        """
        self.filename = filename
        self.filewr = filewr
        self.console = console
        self.status_console = status_console
        self.status_filewr = status_filewr
        self.setlevel = setlevel
        self.__path_to_file = self.__path_create(self.filename)

    def get_log(self):
        """
        Вызов Логера.

        """
        logger = logging.getLogger(self.filename)
        logger.setLevel(self.setlevel)

        if self.filewr is True:
            file_handler = self._file_write()
            file_handler.setLevel(self.status_filewr)
            logger.addHandler(file_handler)
        else:
            self.filewr = False

        if self.console is True:
            console_handler = self._console_output()
            console_handler.setLevel(self.status_console)
            logger.addHandler(console_handler)
        else:
            self.console = False

        if self.__value_err_message(self.filewr, self.console) is True:
            return logger

    @staticmethod
    def _console_output():
        """
        Метод для вывода логов в консоль.
        :return: Настройки для вывода лога в консоль.

        """
        cons_handler = logging.StreamHandler()
        return cons_handler

    def _file_write(self):
        """
        Метод для записи логов в файл.
        :return: Настройки для записи логов в файл.

        """
        file_formatted = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler(
            self.__path_to_file, mode="w", encoding="UTF-8"
        )
        file_handler.setFormatter(file_formatted)
        return file_handler

    @staticmethod
    def __value_err_message(filewr, console):
        """
        Вывод сообщения, при условии, если один из параметров
        экземпляра класса (console=bool, filewr=bool) не указан.
        :return: Отладочное сообщение.

        """
        try:
            if not filewr and not console:
                raise ValueError(
                    "При создании класса, хотя-бы один из "
                    "двух параметров (console=bool, filewr=bool) "
                    "должен иметь аргумент True"
                )
        except ValueError:
            print("Пожалуйста, установите один из параметров.")
            return False
        else:
            return True

    @staticmethod
    def __path_create(filename: str, directory_name: str = "logs") -> str:
        """
        Формирование пути до файла.
        :param directory_name: Название директории, в которой будут храниться логи.
        :param filename: Имя файла с логами (относительно вызываемого модуля).
        :return: Полный путь до файла.

        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_dir = os.path.join(base_dir, directory_name)
        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)
        return os.path.join(path_to_dir, filename + ".txt")
