"""
Тестирование создания и обучения автоэнкодера.

"""

import os
from keras.src.saving import load_model

from src.create_autoencoder import CreateAutoencoder


def test_autoencoder_creation_and_training(sample_numpy):
    """
    Тест на создание и обучение автоэнкодера.
    :param sample_numpy: Готовые тестовые данные Numpy

    """
    autoencoder_model = CreateAutoencoder(sample_numpy)
    assert autoencoder_model.autoencoder
    assert os.path.exists(autoencoder_model.path_to_file), "Не удалось создать файл."


def test_saved_load_model(sample_numpy):
    """
    Тест на загрузку сохранённой модели.
    :param sample_numpy: Готовые тестовые данные Numpy

    """
    autoencoder_model = CreateAutoencoder(sample_numpy)
    loaded_model = load_model(autoencoder_model.path_to_file)
    assert loaded_model is not None
    assert len(loaded_model.layers) == len(autoencoder_model.autoencoder.layers)
