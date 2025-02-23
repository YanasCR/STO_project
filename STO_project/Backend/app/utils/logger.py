import logging
import sys
from loguru import logger

# 🔹 Настройки логирования
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
LOG_FILE = "logs/app.log"

# 🔹 Очищаем стандартные обработчики FastAPI-логов
logging.getLogger().handlers = []

# 🔹 Настраиваем Loguru
logger.remove()
logger.add(sys.stdout, format=LOG_FORMAT, level="INFO")  # Вывод в консоль
logger.add(LOG_FILE, format=LOG_FORMAT, level="DEBUG", rotation="10 MB")  # Лог в файл (макс. 10 MB)

# 🔹 Функция для логирования ошибок
def log_error(error_message):
    logger.error(f"❌ {error_message}")

# 🔹 Функция для логирования успешных действий
def log_info(message):
    logger.info(f"✅ {message}")

# 🔹 Функция для логирования предупреждений
def log_warning(message):
    logger.warning(f"⚠️ {message}")
