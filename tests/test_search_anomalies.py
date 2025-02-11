"""
Тестирование функционала выявления аномалий.

"""

import numpy as np
import pandas as pd

from src.search_anomalies import AiAnmlSearch


def test_detect_anomalies(ai_anml_search_instance: AiAnmlSearch):
    """
    Тест для метода `detect_anomalies`.
    :param ai_anml_search_instance: Экземпляр класса AiAnmlSearch.

    """
    df_scaled = pd.DataFrame({"feature1": [0.1, 0.2, 0.1], "feature2": [0.2, 0.1, 0.1]})
    df = pd.DataFrame({"feature1": [1, 2, 1], "feature2": [2, 1, 1]})
    ai_anml_search_instance.autoencoder.predict.return_value = np.array(
        [[0.1, 0.2], [0.2, 0.1], [0.1, 0.1]]
    )
    anomalies = ai_anml_search_instance.detect_anomalies(
        df_scaled=df_scaled,
        autoencoder=ai_anml_search_instance.autoencoder,
        df=df,
        threshold=0.99,
    )
    assert anomalies.empty


def test_processed_packet_empty_data(ai_anml_search_instance):
    """
    Тест для метода `processed_packet` с пустыми данными.
    :param ai_anml_search_instance: Экземпляр класса AiAnmlSearch.

    """
    df_scaled = pd.DataFrame()
    df = pd.DataFrame()
    result = ai_anml_search_instance.process_packet(df_scaled=df_scaled, df=df)
    assert result.empty


def test_save_anomalies_to_file(ai_anml_search_instance, tmp_path):
    """
    Тест на запись аномалий в файл.
    :param ai_anml_search_instance: Экземпляр класса AiAnmlSearch.

    """
    anomalies = pd.DataFrame({"feature1": [1, 2, 1], "feature2": [2, 1, 1]})
    file_name = tmp_path.joinpath("anomalies.csv")
    ai_anml_search_instance.save_anomalies_to_file(
        file_name=file_name, anomalies=anomalies
    )
    assert file_name.exists()
    saved_data = pd.read_csv(file_name)
    assert not saved_data.empty


def test_path_create(ai_anml_search_instance):
    """
    Тест на формирование пути до файла.
    :param ai_anml_search_instance: Экземпляр класса AiAnmlSearch.
    """
    path = ai_anml_search_instance._AiAnmlSearch__path_create()
    assert "data_traffic" in path
    assert "anomalies_in_traffic.csv" in path
