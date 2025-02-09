import os
from concurrent.futures import ThreadPoolExecutor

# Глобальный ThreadPoolExecutor, который будет использоваться во всех файлах
executor = ThreadPoolExecutor(max_workers=os.cpu_count())