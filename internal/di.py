from config import Config
from internal.models.wild_fire_model.model import WildFireModel
from internal.services.prediction.service import PredictionService
from internal.services.weather.service import WeatherService
from internal.sources.open_meteo.open_meteo import OpenMeteo


class DI:
    __instance = None

    def __init_deps(self):
        config = Config.get_instance()

        # Sources
        meteo_source = OpenMeteo(config=config)

        # Models
        wild_fire_model = WildFireModel()

        # Services
        self.__weather_service = WeatherService(meteo_source=meteo_source)
        self.__prediction_service = PredictionService(fire_risk_model=wild_fire_model)

    @property
    def weather_service(self):
        return self.__weather_service

    @property
    def prediction_service(self):
        return self.__prediction_service


    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            # Вызов скрытого конструктора
            cls.__instance = cls.__create_instance()
        return cls.__instance

    @classmethod
    def __create_instance(cls):
        # Приватный доступ к конструктору
        obj = super().__new__(cls)
        obj.__init_deps()  # Вызов инициализатора
        return obj

    def __init__(self):
        raise RuntimeError("Use get_instance() to create an object")