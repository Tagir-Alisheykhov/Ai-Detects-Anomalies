"""
Готовые данные для написания тестов.

"""

from unittest.mock import MagicMock

import numpy as np
import pytest
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether

from src.pack_capture import PackCapt
from src.search_anomalies import AiAnmlSearch


@pytest.fixture
def cls_instance_capture(
    count=0, time_sec=5, dir_name="data_test", filename="test_traffic.pcap"
) -> PackCapt:
    """
    Создание экземпляра класса.
    :return: Объект класса PackCapt.

    """
    pack_capt = PackCapt(
        count=count, time_capture_sec=time_sec, dir_name=dir_name, filename=filename
    )
    return pack_capt


@pytest.fixture
def sample_numpy() -> np.ndarray:
    """
    Образец простых данных Numpy
    для тестирования.
    :return: DataFrame

    """
    data = [
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.0, 0.1, 0.2, 0.3],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.0, 0.0, 0.1, 0.2, 0.3],
        [0.1, 0.1, 0.3, 0.4, 0.5],
        [0.4, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.0, 0.1, 0.2, 0.3],
        [0.1, 0.3, 0.3, 0.4, 0.5],
        [0.4, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.1, 0.2, 0.2, 0.3],
        [0.1, 0.5, 0.2, 0.4, 0.0],
    ]
    return np.array(data)


@pytest.fixture
def sample_packets() -> list:
    """
    Фикстура для создания тестовых пакетов.
    :return: Список с тестовыми пакетами.

    """
    packets = [
        Ether()
        / IP(src="192.168.1.1", dst="192.168.1.2", proto=6, ttl=64)
        / TCP(sport=12345, dport=80),
        Ether()
        / IP(src="192.168.1.2", dst="192.168.1.1", proto=6, ttl=64)
        / TCP(sport=80, dport=12345),
        Ether()
        / IP(src="192.168.1.3", dst="192.168.1.4", proto=17, ttl=128)
        / TCP(sport=12345, dport=80),
    ]
    return packets


@pytest.fixture
def ai_anml_search_instance():
    """
    Фикстура для создания класса экземпляра класса.
    :return: Объект класса AiAnmlSearch

    """
    autoencoder = MagicMock()
    return AiAnmlSearch(autoencoder=autoencoder)
