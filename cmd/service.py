import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import httpx
from contextlib import asynccontextmanager
from internal.unitls.executor import executor
from internal.services.prediction.dto import GetFireRiskPredictionOut
from fastapi.params import Depends, Query
from internal.services.weather.dto import GetCurrentWeatherOut, GetCurrentByLocationIn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, Response
from internal.di import DI

IS_DEV = "dev" in sys.argv

# 🔹 Корректное завершение ThreadPoolExecutor
@asynccontextmanager
async def lifespan(a: FastAPI):
    print("Starting application...")
    yield  # Здесь выполняется работа сервера
    print("Shutting down ThreadPoolExecutor...")
    executor.shutdown(wait=True)
    print("ThreadPoolExecutor shut down successfully.")

# Создаем экземпляр FastAPI с указанием контекста для завершения работы
app = FastAPI(lifespan=lifespan)

# Подключаем React-статические файлы
app.mount("/assets", StaticFiles(directory="web/dist/assets"), name="assets")
app.mount("/static", StaticFiles(directory="web/dist/static"), name="static")

# Инициализируем DI контейнер
container = DI.get_instance()

# URL фронтенда для разработки
DEV_FRONTEND_URL = "http://localhost:5173"

@app.get("/api/v1/weather/current", response_model=GetCurrentWeatherOut)
async def get_weather_current(
    lat: float = Query(55.7386, title="Широта", description="Latitude"),
    lon: float = Query(37.6068, title="Долгота", description="Longitude")
):
    """
    Роут получения текущей погоды по географическим координатам
    :param lat: широта
    :param lon: долгота
    """

    weather = container.weather_service.get_current(
        params=GetCurrentByLocationIn(
            lat=lat,
            lon=lon
        )
    )
    return weather

@app.get("/api/v1/wildfire/predict", response_model=GetFireRiskPredictionOut)
async def wild_fire_predict(
    lat: float = Query(55.7386, title="Широта", description="Latitude"),
    lon: float = Query(37.6068, title="Долгота", description="Longitude")
):
    """
    Роут предсказания риска пожара на основе текущей погоды
    :param lat: широта
    :param lon: долгота
    """
    weather = container.weather_service.get_current(
        params=GetCurrentByLocationIn(
            lat=lat,
            lon=lon
        )
    )

    prediction = await container.prediction_service.get_fire_risk_prediction(
        weather_data=weather
    )

    return prediction

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """
    Роут для обслуживания SPA-приложения, все запросы отдают фронтенд

    :param full_path: любой путь отдает фронтенд
    """

    # Возвращаем главный HTML файл для продакшн-режима
    if not IS_DEV:
        return FileResponse("web/dist/index.html")

    # Проксируем запросы на фронт в режиме разработки
    async with httpx.AsyncClient() as client:
        frontend_url = f"{DEV_FRONTEND_URL}/{full_path}"
        try:
            response = await client.get(frontend_url)
            return Response(content=response.content, status_code=response.status_code, headers=response.headers)
        except httpx.RequestError:
            return Response(content="Frontend server is not running", status_code=502)
