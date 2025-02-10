from config import Config
import openmeteo_requests
import requests_cache
from retry_requests import retry

from internal.services.weather.contracts import MeteoSource
from internal.services.weather.dto import GetCurrentByLocationOut, CurrentWeather

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

class OpenMeteo(MeteoSource):
    __api_path = 'https://api.open-meteo.com/v1/forecast'   # Путь к API OpenMeteo для получения данных о погоде

    def __init__(self, config: Config):
        super().__init__()
        self.__config = config

    def get_current_weather(self, lat: float, lon: float) -> GetCurrentByLocationOut:
        """
        Получение текущей погоды для заданных географических координат (широты и долготы)
        с использованием API OpenMeteo.

        Запрашиваем текущие данные о погоде, включая температуру, влажность, осадки,
        дождь и скорость ветра.
        """

        url = self.__api_path
        params = {
            "timezone": "Europe/Moscow",
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "rain",
                "wind_speed_10m",
            ],
        }

        responses = openmeteo.weather_api(url, params=params)

        # Если ответ пуст, выбрасываем исключение
        if len(responses) == 0:
            raise Exception("No data received from OpenMeteo API")

        response = responses[0]
        current = response.Current()

        # Возвращаем результат в нужном формате, округляя значения
        return GetCurrentByLocationOut(data=CurrentWeather(
            temperature=round(current.Variables(0).Value()),
            relative_humidity = round(current.Variables(1).Value()),
            precipitation = round(current.Variables(2).Value(), 1),
            rain = round(current.Variables(3).Value(), 1),
            wind_speed = round(current.Variables(4).Value()),
        ))

