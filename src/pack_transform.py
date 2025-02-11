"""
Содержит класс для преобразования данных, полученных
путём захвата пакетов сетевого трафика.

"""

import logging

import numpy as np
import pandas as pd

from scapy.layers.inet import IP, TCP
from sklearn.preprocessing import LabelEncoder, StandardScaler
from src.cls_logger import Logger

log = Logger(
    filename=__name__ + "_debug",
    status_filewr=logging.DEBUG,
)
log = log.get_log()


class PackTransform:
    """
    Преобразует данные (.pcap) для обучения автоэнкодера.

    """

    data_file: tuple

    def __init__(self, data_file):
        """
        Инициализация параметров
        :param data_file: .pcap файл с пакетами сетевого трафика

        """
        self.__data_file = data_file

    def __pcap_to_df(self) -> tuple[np.ndarray, pd.DataFrame]:
        """
        Преобразует данные из файла .pcap в Numpy и DataFrame
        :return: Декодированные и сырые данные.

        """
        try:
            data = list()
            for packet in self.__data_file:
                if IP in packet:
                    row = {
                        "src_ip": packet[IP].src,
                        "dst_ip": packet[IP].dst,
                        "proto": packet[IP].proto,
                        "ttl": packet[IP].ttl,
                        "length": len(packet),
                        "flags": packet[IP].flags,
                        "sport": packet[TCP].sport if TCP in packet else 0,
                        "dport": packet[TCP].dport if TCP in packet else 0,
                        "timestamp": int(packet.time) if packet.time is not None else 0,
                    }
                    data.append(row)
            df = pd.DataFrame(data)

            df_mod = self.df_modification(df)
            raw_df = df_mod.copy()

            encoder = LabelEncoder()
            df_mod["proto_encoded"] = encoder.fit_transform(df_mod["proto"])
            df_mod["src_ip_encoded"] = encoder.fit_transform(df_mod["src_ip"])
            df_mod["dst_ip_encoded"] = encoder.fit_transform(df_mod["dst_ip"])
            df_mod["timestamp"] = encoder.fit_transform(df_mod["timestamp"])
            df_mod["flags"] = encoder.fit_transform(df_mod["flags"])

            df_mod = df_mod.drop(
                ["src_ip", "dst_ip", "proto", "timestamp", "flags"], axis=1
            )

            scaler = StandardScaler()
            df_scaled = scaler.fit_transform(df_mod)
            log.info("Данные преобразованы.")
            return df_scaled, raw_df
        except Exception as err:
            log.error(f"Возникла ошибка при обработке пакета.\n{err}")
            return np.array([]), pd.DataFrame()

    @staticmethod
    def df_modification(df_mod: pd.DataFrame) -> pd.DataFrame:
        """
        Добавление дополнительных столбцов с информацией о пакетах
        для более точного анализа данных.
        А также проверки на корректность входных данных.
        :param df_mod: Преобразованные данные сетевого трафика.
        :return: Дополненные и отфильтрованные данные.

        """
        try:
            pd.set_option("future.no_silent_downcasting", True)

            if "timestamp" not in df_mod.columns:
                print("Столбец 'timestamp' отсутствует в данных")
                return pd.DataFrame()

            if df_mod["timestamp"].isnull().any():
                print("Обнаружены некорректные значения в 'timestamp'.")
                return pd.DataFrame()

            df_mod["timestamp"] = (
                pd.to_datetime(df_mod["timestamp"], unit="s", errors="coerce")
                .dt.tz_localize("UTC")
                .dt.tz_convert("Europe/Moscow")
                .dt.floor("s")
            )
            if len(df_mod) > 2:
                df_mod["avg_pack_size"] = df_mod.groupby("src_ip")["length"].transform(
                    "mean"
                )
                df_mod["uniq_ports"] = df_mod.groupby("src_ip")["dport"].transform(
                    "nunique"
                )
                df_mod["duration"] = (
                    df_mod.groupby(["src_ip", "dst_ip"])["timestamp"]
                    .transform(lambda x: x.max() - x.min())
                    .dt.total_seconds()
                )
            df_mod["sport"] = df_mod["sport"].fillna(0).astype(float)
            df_mod["dport"] = df_mod["dport"].fillna(0).astype(float)
            return df_mod
        except Exception as error:
            log.error(f"Возникла ошибка при обработке пакета {error}")
            return pd.DataFrame()

    @property
    def get_formatted_data(self) -> tuple[np.ndarray, pd.DataFrame]:
        """
        Вывод масштабированных и сырых данных.
        :return: tuple: __pcap_to_df() = (df_scaled, raw_df)

        """
        log.debug("Вывод данных")
        return self.__pcap_to_df()
