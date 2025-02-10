from abc import ABC, abstractmethod
from internal.services.weather.dto import GetCurrentByLocationOut


class MeteoSource(ABC):
    @abstractmethod
    def get_current_weather(
            self,
            lat: float,
            lon: float
    ) -> GetCurrentByLocationOut:
        pass