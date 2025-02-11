"""
Тестирование функционала для преобразования данных.

"""

import numpy as np
import pandas as pd

from src.pack_transform import PackTransform


def test_pcap_to_df(sample_packets: list):
    """
    Тест на преобразование пакетов в DataFrame.
    :param sample_packets: Тестовые данные.

    """
    pack_transform = PackTransform(sample_packets)
    df_scaled, df_raw = pack_transform.get_formatted_data

    assert isinstance(df_scaled, np.ndarray)
    assert isinstance(df_raw, pd.DataFrame)
    assert len(df_scaled) > 0
    assert len(df_raw) > 0

    expected_columns = [
        "src_ip",
        "dst_ip",
        "proto",
        "ttl",
        "length",
        "flags",
        "sport",
        "dport",
        "timestamp",
    ]
    assert all(col in df_raw.columns for col in expected_columns)


def test_df_modification(sample_packets: list):
    """
    Тест на модификацию DataFrame
    :param sample_packets: Тестовые данные.

    """
    pack_transform = PackTransform(sample_packets)
    _, df_raw = pack_transform.get_formatted_data

    modified_df = pack_transform.df_modification(df_raw)
    assert isinstance(modified_df, pd.DataFrame)


def test_empty_data():
    """
    Тест на обработку пустых данных.

    """
    pack_transform = PackTransform(list())
    df_scaled, df_raw = pack_transform.get_formatted_data
    assert len(df_scaled) == 0
    assert len(df_raw) == 0
