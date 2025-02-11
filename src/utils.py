"""
Модуль для связки всей функциональности
проекта в пользовательском интерфейсе.

"""

import logging
import os
import time

import pandas as pd
from keras.src.saving import load_model
from src.cls_logger import Logger
from src.pack_capture import PackCapt
from src.pack_transform import PackTransform
from src.create_autoencoder import CreateAutoencoder
from src.search_anomalies import AiAnmlSearch

log1 = Logger(
    filename=__name__ + "_debug",
    console=False,
    status_filewr=logging.DEBUG,
).get_log()

log2 = Logger(
    filename=__name__,
    console=True,
    filewr=False,
).get_log()

directory_name_default = "data_encoders"
file_name_default = "base_learned_autoencoder.keras"
path_to_base_autoencoder = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    directory_name_default,
    file_name_default,
)
learned_autoencoder_path = path_to_base_autoencoder

debug_message1 = """
-------------------------------------------------------------------------
Отсутствует директория, или файл с обученной моделью автоэнкодера.\n
Требуется обучить модель. Пожалуйста, установите "НЕТ (обучить заново)",\n
затем выберите время обучения модели автоэнкодера (в секундах)
-------------------------------------------------------------------------
"""
debug_message2 = """
Программа запущена.\nДля принудительного прекращения\nработы зажмите/нажимайте клавиши `Ctrl + C`"""
inp_message1 = """
\nВведите время (в секундах [integer]) для обучения автоэнкодера.\nПо умолчанию 86400сек=24ч\nВвод: """
inp_message2 = """
\nВведите название директории [string].\nИли оставьте по умолчанию [Enter]\nВвод: """
inp_message3 = """
\nВведите название файла [string].\nИли оставьте по умолчанию [Enter]\nВвод: """
inp_message4 = """
\nВы хотите воспользоваться обученной моделью для поиска аномалий,\nили обучить модель заново 
(по умолчанию 24 часа) ?\n[ ДА (обученной) | НЕТ (обучить заново) ]\nВвод: """


def user_interface():
    """
    Интерфейс для взаимодействия с пользователем.

    """
    log1.debug("Запуск интерфейса")
    log2.info(debug_message2)
    time.sleep(3)
    global learned_autoencoder_path
    cycle_true = True
    while cycle_true:
        answer_user = input(inp_message4).lower()
        if (
            answer_user == "да"
            or answer_user == ""
            or answer_user == "yes"
            or answer_user == "y"
        ):
            answer_user = True
        if (
            answer_user == "нет"
            or answer_user == "не"
            or answer_user == "no"
            or answer_user == "n"
        ):
            answer_user = False
        if answer_user is True:
            log1.debug("Пользователь выбрал `обученную модель`")
            if os.path.exists(learned_autoencoder_path):
                autoencoder = load_model(learned_autoencoder_path)
                try:
                    while True:
                        yield search_anomalies(autoencoder)
                except Exception as err:
                    log1.error(f"Возникла ошибка: {err}")
            else:
                log1.debug(debug_message1)
                time.sleep(5)
        if answer_user is False:
            log1.debug("Пользователь выбрал `обучить модель`")
            timeout = int(input(inp_message1))
            dir_name = input(inp_message2)
            filename = input(inp_message3)
            learned_autoencoder = learn_autoencoder(
                timeout=timeout, dir_name=dir_name, filename=filename
            )
            learned_autoencoder_path = learned_autoencoder.path_to_file
            log2.info(f"Saved in path: {learned_autoencoder_path}")


def learn_autoencoder(
    timeout: int = 5, dir_name: str = None, filename: str = None
) -> CreateAutoencoder:
    """
    Создание автоэнкодера. Обучение модели.

    """
    time.sleep(2)
    log1.info("\nЗахват сетевого трафика.\nloading...\n")
    packets = PackCapt(time_capture_sec=timeout)
    packets.write_packs_pcap_time()
    packets = packets.read_packs_pcap()

    log1.info("\nФорматирование данных.\nloading...\n")
    formatter = PackTransform(packets)
    df_scaled, df = formatter.get_formatted_data

    log1.info("\nСоздание и обучение автоэнкодера.\nloading...\n")
    create_autoencoder = CreateAutoencoder(
        data_scaled=df_scaled, dir_name=dir_name, filename=filename
    )
    # Вывод автоэнкодера
    time.sleep(2)
    log1.info("\nАвтоэнкодер успешно создан и обучен!\n")
    return create_autoencoder


def search_anomalies(
    autoencoder: CreateAutoencoder, in_one_capture=15, filename="realtime.pcap"
) -> AiAnmlSearch | pd.DataFrame:
    """
    Основной скрипт для захвата сетевого трафика,
    обработки данных и выявления аномалий.
    :return: Аномалии.

    """
    log2.info(f"\nЗахват трафика. Count packs: {in_one_capture}.\n")
    packets = PackCapt(count=in_one_capture, filename=filename)
    packets.write_packs_pcap_count()
    packets = packets.read_packs_pcap()
    # Форматирование данных.
    formatter = PackTransform(packets)
    df_scaled, df_raw = formatter.get_formatted_data
    # Выявление аномалий.
    detect_anomalies = AiAnmlSearch(autoencoder)
    # Вывод аномалий
    return detect_anomalies.process_packet(df_scaled, df_raw)
