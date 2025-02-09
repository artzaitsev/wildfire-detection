from internal.services.prediction.contracts import FireRiskModel
from internal.services.prediction.dto import GetFireRiskPredictionOut
from internal.services.weather.dto import GetCurrentWeatherOut


class PredictionService:
    def __init__(
        self,
        fire_risk_model: FireRiskModel
    ):
        self.__fire_risk_model = fire_risk_model

    async def get_fire_risk_prediction(self, weather_data: GetCurrentWeatherOut) -> GetFireRiskPredictionOut:
        proba = await self.__fire_risk_model.get_fire_risk_proba(weather_data)

        return GetFireRiskPredictionOut(data=proba)