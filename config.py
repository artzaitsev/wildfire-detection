from dotenv import load_dotenv

class Config:
    """
    Cинглтон конфигурации приложени.
    Подгружает environment variables, включая .env.
    Вызывается через статичный метод get_instance,
    """
    __instance = None

    def __init_internal(self):
        load_dotenv()


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