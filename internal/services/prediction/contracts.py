from abc import ABC, abstractmethod

from internal.services.weather.dto import GetCurrentWeatherOut


class FireRiskModel(ABC):
    @abstractmethod
    async def get_fire_risk_proba(self, weather_data: GetCurrentWeatherOut) -> float:
        pass