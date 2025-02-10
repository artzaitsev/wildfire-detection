from datetime import datetime
from internal.services.weather.contracts import MeteoSource
from internal.services.weather.dto import GetCurrentWeatherOut, WeatherWfi, GetCurrentByLocationIn
from internal.services.weather.fwi import FireWeatherIndex


class WeatherService:
    def __init__(
            self,
            meteo_source: MeteoSource, # Контракт источника данных о погоде
    ):
        self.__meteo_source = meteo_source

    def get_current(self, params: GetCurrentByLocationIn) -> GetCurrentWeatherOut:
        """
        Получение текущей погоды для заданных географических координат (широты и долготы).

        В результате выполнения:
            - Запрашиваются данные о текущей погоде
            - Рассчитываются индексы опасности для лесных пожаров
            - Возвращаются все эти данные в нужном формате.
        """

        # Запрашиваем текущие данные о погоде из источника
        w_res = self.__meteo_source.get_current_weather(params.lat, params.lon)
        w = w_res.data

        # Получаем текущий месяц для использования в расчетах
        month = datetime.now().month

        # Рассчитываем индексы для оценки лесных пожаров
        f_res = FireWeatherIndex(
            temp=w.temperature,
            rh=w.relative_humidity,
            ws=w.wind_speed,
            prec=w.precipitation,
            lat=params.lat,
            mon=month
        )

        # Формируем и возвращаем итоговый объект с данными о погоде и индексами для лесных пожаров
        return GetCurrentWeatherOut(
            weather=w_res.data,
            wfi=WeatherWfi(
                fwi=round(f_res.get_fwi(), 1),
                bui=round(f_res.get_bui(), 1),
                isi=round(f_res.get_isi(), 1),
                ffmc=round(f_res.get_ffmc(), 1),
                dmc=round(f_res.get_dmc(), 1),
                dc=round(f_res.get_dc(), 1),
            )
        )