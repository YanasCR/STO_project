import uuid
import hashlib
import random
import string
from datetime import datetime, timedelta

# 🔹 Генерация случайного UUID
def generate_uuid():
    return str(uuid.uuid4())

# 🔹 Хэширование строки (например, VIN-кода)
def hash_string(value: str):
    return hashlib.sha256(value.encode()).hexdigest()

# 🔹 Генерация случайного пароля
def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return "".join(random.choice(chars) for _ in range(length))

# 🔹 Проверка, истек ли срок действия (например, токена)
def is_expired(expiry_date: datetime):
    return datetime.utcnow() > expiry_date

# 🔹 Форматирование даты в читабельный вид
def format_date(date: datetime, format="%Y-%m-%d %H:%M:%S"):
    return date.strftime(format)

# 🔹 Получение текущей даты + X дней
def get_future_date(days: int):
    return datetime.utcnow() + timedelta(days=days)
