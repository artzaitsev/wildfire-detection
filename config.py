from dotenv import load_dotenv
import os

class Config:
    __instance = None

    def __init_internal(self):
        load_dotenv()

        self.__open_meteo_api_key: str = os.getenv('OPEN_METEO_API_KEY')

    @property
    def open_meteo_api_key(self):
        return self.__open_meteo_api_key


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
        obj.__init_internal()  # Вызов инициализатора
        return obj

    def __init__(self):
        raise RuntimeError("Use get_instance() to create an object")