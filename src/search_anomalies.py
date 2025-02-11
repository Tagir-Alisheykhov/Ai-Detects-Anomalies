"""
Содержит для выявления аномалий

"""

import os
import numpy as np
import pandas as pd
import logging

from src.cls_logger import Logger

log1 = Logger(
    filename=__name__ + "_debug",
    status_filewr=logging.DEBUG,
)

log1 = log1.get_log()


class AiAnmlSearch:
    """
    Класс для обучения модели анализу
    сетевого трафика и выявления аномалий

    """

    directory_name = "data_traffic"
    file_name = "anomalies_in_traffic.csv"

    def __init__(self, autoencoder):
        """
        Инициализация параметров.
        :param autoencoder: Обученный автоэнкодер

        """
        self.autoencoder = autoencoder
        log1.debug("Автоэнкодер инициализирован")

    def process_packet(
        self, df_scaled: np.ndarray, df: pd.DataFrame
    ):
        """
        Обработка отформатированных данных сетевого трафика,
        Выявление аномалий.
        :param df_scaled: Масштабированные данные
        :param df: Сырые данные.
        :return: Пропуск итерации, либо вывод аномалий
        в консоль и запись в файл.

        """
        log1.debug("Обработка данных")
        try:
            if df.empty:
                log1.info("Нет данных для обработки. Пропуск итерации\n")
                return pd.DataFrame()

            anomalies = self.detect_anomalies(df_scaled, self.autoencoder, df)
            self.save_anomalies_to_file(anomalies, self.__path_create())

            if not anomalies.empty:
                detected = f">>> [ ANOMALIES DETECTED ] " f"\n{anomalies}\n" f"<<<\n"
                return detected
            else:
                return "- Not found -"
        except Exception as err:
            log1.error(f"Возникла ошибка: {err}")

    @staticmethod
    def detect_anomalies(
        df_scaled: pd.DataFrame | np.ndarray,
        autoencoder,
        df: pd.DataFrame,
        threshold: float = 0.99,
    ) -> pd.DataFrame:
        """
        Обнаружение аномалий с помощью обученной модели.
        :param df_scaled: Нормализованные данные.
        :param autoencoder: Обученная модель автоэнкодера.
        :param df: Исходный DataFrame.
        :param threshold: Порог для определения аномалий.
        :return: DataFrame с аномалиями.

        """
        log1.debug("Выявление аномалий")
        try:
            if df_scaled.size == 0 or df.empty:
                log1.warning("\nПустые данные . . .")
                return pd.DataFrame()
            reconstructed = autoencoder.predict(df_scaled)
            mse = np.mean(np.power(df_scaled - reconstructed, 2), axis=1)
            threshold = np.quantile(mse, threshold)
            anomalies_indices = np.where(mse > threshold)[0]
            anomalies = df.iloc[anomalies_indices]
        except Exception as err:
            log1.error(f"Возникла ошибка: {err}")
            return pd.DataFrame()
        else:
            if anomalies.empty:
                anomalies = pd.DataFrame()
                log1.info("\nАномалии не обнаружены")
                return anomalies
            if not anomalies.empty:
                return anomalies

    @staticmethod
    def save_anomalies_to_file(
        anomalies: pd.DataFrame, file_name: str = "anomalies.csv"
    ) -> None:
        """
        Сохранение аномалий в файл.
        :param anomalies: DataFrame с аномалиями.
        :param file_name: Имя файла для сохранения.

        """
        anomalies.to_csv(
            file_name, index=False, mode="a", header=not os.path.exists(file_name)
        )
        log1.debug("Сохранение аномалий -> data_traffic/anomalies_in_traffic.csv")

    def __path_create(self) -> str:
        """
        Формирование пути до файла
        :return: Полный путь до файла

        """
        directory_name = self.directory_name
        filename = self.file_name
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_dir = os.path.join(base_dir, directory_name)
        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)
        return os.path.join(path_to_dir, filename)
