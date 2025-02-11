"""
Тестирование захвата сетевого трафика.

"""

import os
import numpy as np


def test_write_and_read_packets(cls_instance_capture: np.array):
    """
    Тест для записи и чтения пакетов.

    """
    pack_capt = cls_instance_capture
    pack_capt.count = 3
    pack_capt.write_packs_pcap_count()
    assert os.path.exists(pack_capt.path_to_file), "Не удалось создать файл."

    packets = pack_capt.read_packs_pcap()
    assert len(packets) == 3, "Количество пакетов не соответствует ожидаемому"


def test_time_capture(cls_instance_capture: np.array):
    """
    Захват пакетов по времени.

    """
    pack_capt = cls_instance_capture
    pack_capt.time_capture = 2
    pack_capt.write_packs_pcap_time()
    assert os.path.exists(pack_capt.path_to_file), "Не удалось создать файл."
