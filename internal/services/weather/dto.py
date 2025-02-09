from pydantic import BaseModel
from fastapi import Query


class CurrentWeather(BaseModel):
    temperature: float
    relative_humidity: float
    precipitation: float
    rain: float
    wind_speed: float

class GetCurrentByLocationIn(BaseModel):
    lat: float
    lon: float

class GetCurrentByLocationOut(BaseModel):
    data: CurrentWeather

class WeatherWfi(BaseModel):
    ffmc: float
    dmc: float
    dc: float
    isi: float
    bui: float
    fwi: float

class GetCurrentWeatherOut(BaseModel):
    weather: CurrentWeather
    wfi: WeatherWfi