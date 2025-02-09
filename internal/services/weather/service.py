from datetime import datetime

from internal.services.weather.contracts import MeteoSource
from internal.services.weather.dto import GetCurrentWeatherOut, WeatherWfi, GetCurrentByLocationIn
from internal.services.weather.fwi import FireWeatherIndex


class WeatherService:
    def __init__(
            self,
            meteo_source: MeteoSource,
    ):
        self.__meteo_source = meteo_source

    def get_current(self, params: GetCurrentByLocationIn) -> GetCurrentWeatherOut:
        w_res = self.__meteo_source.get_current_weather(params.lat, params.lon)
        w = w_res.data

        month = datetime.now().month

        f_res = FireWeatherIndex(
            temp=w.temperature,
            rh=w.relative_humidity,
            ws=w.wind_speed,
            prec=w.precipitation,
            lat=params.lat,
            mon=month
        )

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