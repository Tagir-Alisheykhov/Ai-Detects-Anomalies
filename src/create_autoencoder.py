"""
Модуль для создания и обучения Autoencoder(а)

"""

import os
import pandas as pd

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense

from src.cls_logger import Logger

lo = Logger(__name__)


class CreateAutoencoder:
    """
    Класс для создания обучения модели автоэнкодера.

    """

    data_frame: pd.DataFrame
    dir_name: str
    filename: str

    directory_name_default = "data_encoders"
    file_name_default = "autoencoder_model_default_name.keras"

    def __init__(self, data_scaled, dir_name=None, filename=None):
        """
        Инициализация параметров.
        :param data_scaled: Данные в формате DataFrame для обучения модели.
        :param dir_name: Имя директории, в которой будет располагаться файл.
        :param filename: Имя файла, с обученным autoencoder(ом).

        """
        self.__scaled_df = data_scaled
        self.dir_name = self.directory_name_default if not dir_name else dir_name
        self.filename = self.file_name_default if not filename else filename
        self.path_to_file = self.__path_for_write(self.dir_name, self.filename)
        self.__autoencoder = self.__learn_autoencoder()

    @classmethod
    def __path_for_write(cls, dir_name, filename) -> str:
        """
        Формирование пути до файла.
        :param dir_name: Имя директории.
        :param filename: Имя файла

        """
        dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        abs_path = os.path.join(str(dir_path), filename)
        return abs_path

    def __created_autoencoder(self):
        """
        Создание автоэнкодера.
        :return: Созданный автоэнкодер

        """
        input_dim = self.__scaled_df.shape[1]
        encoding_dim = 10
        input_layer = Input(shape=(input_dim,))
        encoder = Dense(encoding_dim, activation="relu")(input_layer)
        decoder = Dense(input_dim, activation="sigmoid")(encoder)
        autoencoder = Model(inputs=input_layer, outputs=decoder)
        autoencoder.compile(optimizer="adam", loss="mean_squared_error")
        return autoencoder

    def __learn_autoencoder(self):
        """
        Обучение автоэнкодера. Обучение на основе ОВ.
        Сохранение обученной модели.
        :return: Обученный автоэнкодер.

        """
        df_scaled = self.__scaled_df
        autoencoder = self.__created_autoencoder()
        autoencoder.fit(
            df_scaled,
            df_scaled,
            epochs=50,
            batch_size=32,
            shuffle=True,
            validation_split=0.2,
        )
        autoencoder.save(self.path_to_file)
        return autoencoder

    @property
    def autoencoder(self):
        """
        Геттер для вызова автоэнкодера.
        :return: Созданный и обученный автоэнкодер.

        """
        return self.__autoencoder
