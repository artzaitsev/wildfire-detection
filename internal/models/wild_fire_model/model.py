import numpy as np
import pandas as pd
from catboost import CatBoostClassifier

from internal.services.prediction.contracts import FireRiskModel
from internal.services.weather.dto import GetCurrentWeatherOut

import asyncio

from internal.unitls.executor import executor


def adjust_fire_probability(probability: float, temperature: float, humidity: float) -> float:
    """
    Корректирует вероятность лесного пожара в зависимости от температуры и влажности с учетом сглаживания.
    Модель обучена на данных с температурой > 20 °C, необходимо плавно корректировать прогноз.
    :param probability: Исходная вероятность (от 0 до 1)
    :param temperature: Температура в °C
    :param humidity: Относительная влажность воздуха в % (0-100)
    :return: Скорректированная вероятность (от 0 до 1, сглаженная)
    """
    # Важность признаков в модели
    w_T = 0.357  # Коэффициент влияния температуры
    w_H = 0.5  # Коэффициент влияния влажности

    # Коррекция по температуре (сглаженное снижение)
    if temperature < 20:
        temp_penalty = np.log1p(20 - temperature) / 10
        probability *= (1 - w_T * temp_penalty)

    # Коррекция по влажности
    if humidity > 50:
        humidity_penalty = (humidity - 50) / 100  # Чем выше влажность, тем больше снижение
        probability *= (1 - w_H * humidity_penalty)

    # Гарантируем, что вероятность остается в пределах [0.0, 1.0]
    return float(np.clip(probability, 0.0, 1.0))


class WildFireModel(FireRiskModel):
    __model_path = 'modeling/models/external.cbm'  # Путь к модели
    __model: CatBoostClassifier  # Тип модели CatBoost

    def __init__(self):
        self.__model = CatBoostClassifier()  # Инициализация модели CatBoost
        self.__model.load_model(self.__model_path)  # Загрузка обученной модели из файла

    # Синхронный метод для предсказания риска пожара
    def __predict_sync(self, df: pd.DataFrame) -> float:
        # Используем модель для получения вероятности риска пожара
        return self.__model.predict_proba(df)[:, 1][0]

    async def get_fire_risk_proba(self, weather_data: GetCurrentWeatherOut) -> float:
        """
        # Асинхронный метод для получения вероятности риска пожара
        :param weather_data: данные о погоде
        :return: float
        """

        # Формируем данные для модели из информации о текущей погоде
        data = {
            "Temperature": [weather_data.weather.temperature],
            "RH": [weather_data.weather.relative_humidity],
            "Ws": [weather_data.weather.wind_speed],
            "Rain": [weather_data.weather.rain],
            "FFMC": [weather_data.wfi.ffmc],
            "DMC": [weather_data.wfi.dmc],
            "DC": [weather_data.wfi.dc],
            "ISI": [weather_data.wfi.isi],
            "BUI": [weather_data.wfi.bui],
            "FWI": [weather_data.wfi.fwi],
        }

        # Создаем DataFrame из данных
        df = pd.DataFrame(data)

        # При частых запросах модель может забивать потоки, так как предсказание синхронное
        # Поэтому используем асинхронное выполнение, чтобы не блокировать другие операции
        res = await asyncio.get_running_loop().run_in_executor(executor, self.__predict_sync, df)

        # Возвращаем откорректированную вероятность на основе температуры и влажности
        return adjust_fire_probability(res, weather_data.weather.temperature, weather_data.weather.relative_humidity)

