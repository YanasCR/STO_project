import os  # ← Добавляем этот импорт
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# 🔹 Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
DB_ECHO = os.getenv("DB_ECHO", "False") == "True"  # Логирование SQL-запросов

# 🔹 Безопасность
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY не установлен! Укажите его в .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# 🔹 Настройки сервера
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("APP_PORT", 8000))
