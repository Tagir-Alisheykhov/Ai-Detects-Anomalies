"""
Главный модуль - входная точка для запуска всей программы.
В данном модуле вызывается интерфейс для взаимодействия
программы с пользователем.

"""

import os
import time
import logging

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from src.cls_logger import Logger
from src.utils import user_interface


log = Logger(
    filename=__name__ + "ANOMALIES",
    console=True,
    filewr=True,
    status_console=logging.INFO,
    status_filewr=logging.DEBUG,
)
log = log.get_log()


def main():
    try:
        program_response = user_interface()
        for anomalies_detected in program_response:
            log.warning(f"\n{anomalies_detected}\n")
    except KeyboardInterrupt:
        log.info("\nПрограмма завершена пользователем.\n")
    except Exception as err:
        log.error(f"\nВозникла ошибка: {err}\n")


if __name__ == "__main__":
    log.info("\nLoading . . .\nPlease wait.\n")
    time.sleep(3)
    main()
