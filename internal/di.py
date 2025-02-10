from config import Config
from internal.models.wild_fire_model.model import WildFireModel
from internal.services.prediction.service import PredictionService
from internal.services.weather.service import WeatherService
from internal.sources.open_meteo.open_meteo import OpenMeteo


class DI:
    __instance = None

    def __init_deps(self):
        """
        Инициализация зависимостей для контейнера.

        Здесь настраиваются источники данных, модели и сервисы,
        которые будут использоваться в приложении.
        """

        config = Config.get_instance()

        # Источники
        meteo_source = OpenMeteo(config=config)

        # Модели
        wild_fire_model = WildFireModel()

        # Сервисы
        self.__weather_service = WeatherService(meteo_source=meteo_source)
        self.__prediction_service = PredictionService(fire_risk_model=wild_fire_model)

    @property
    def weather_service(self):
        """
        Сервис получения данных о погоде.
        """
        return self.__weather_service

    @property
    def prediction_service(self):
        """
        Сервис для предсказания риска пожара.
        """
        return self.__prediction_service


    @classmethod
    def get_instance(cls):
        """
        Получение экземпляра класса DI (синглтон).

        Если экземпляр еще не создан, вызывается __create_instance для его создания.
        """
        if cls.__instance is None:
            # Вызов скрытого конструктора
            cls.__instance = cls.__create_instance()
        return cls.__instance

    @classmethod
    def __create_instance(cls):
        """
        Приватный метод для создания экземпляра DI.

        Создается новый объект и инициализируются все зависимости.
        """

        # Приватный доступ к конструктору
        obj = super().__new__(cls)
        obj.__init_deps()  # Вызов инициализатора
        return obj

    def __init__(self):
        """
        Запрещено создание экземпляра напрямую.

        Используйте метод get_instance() для получения экземпляра.
        """

        raise RuntimeError("Use get_instance() to create an object")