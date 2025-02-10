from internal.services.prediction.contracts import FireRiskModel
from internal.services.prediction.dto import GetFireRiskPredictionOut
from internal.services.weather.dto import GetCurrentWeatherOut


class PredictionService:
    def __init__(
        self,
        fire_risk_model: FireRiskModel # Модель для оценки риска пожара (реализация FireRiskModel)
    ):
        self.__fire_risk_model = fire_risk_model

    # Асинхронный метод для получения предсказания риска пожара
    async def get_fire_risk_prediction(self, weather_data: GetCurrentWeatherOut) -> GetFireRiskPredictionOut:
        # Получаем вероятность риска пожара с помощью модели
        proba = await self.__fire_risk_model.get_fire_risk_proba(weather_data)

        # Возвращаем предсказание, оборачивая вероятность в объект GetFireRiskPredictionOut
        return GetFireRiskPredictionOut(data=proba)