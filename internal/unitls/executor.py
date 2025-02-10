import os
from concurrent.futures import ThreadPoolExecutor

# Глобальный ThreadPoolExecutor, пока нужен преимущественно для работы с ML моделью
executor = ThreadPoolExecutor(max_workers=os.cpu_count())