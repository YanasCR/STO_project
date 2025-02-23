import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from database import Base, engine, SessionLocal
from app.routes import auth, cars, works, parts
from app.utils.logger import log_error
from dotenv import load_dotenv
import os

# 📌 Загружаем переменные окружения
load_dotenv()

# 📌 Настраиваем логирование (запись в файл)
logging.basicConfig(level=logging.INFO, filename="logs/app.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# 📌 Контекстный менеджер для управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🔄 Проверяем и создаем таблицы в базе данных...")
    try:
        Base.metadata.create_all(engine)
        logging.info("✅ Таблицы успешно созданы!")
    except Exception as e:
        logging.error(f"Ошибка при создании таблиц: {e}")
    yield
    logging.info("🛑 Закрываем соединение с базой данных")
    SessionLocal().close()

# 📌 Создаем FastAPI-приложение
app = FastAPI(title="СТО API", lifespan=lifespan)

# 🎯 Разрешаем CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Разрешаем все заголовки
)

# 📌 Middleware для логирования всех запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"📥 Запрос: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"📤 Ответ: {response.status_code}")
    return response

# 📌 Глобальная обработка ошибок
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_error(f"Ошибка: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(cars.router, prefix="/cars", tags=["Cars"])
app.include_router(works.router, prefix="/works", tags=["Works"])
app.include_router(parts.router, prefix="/parts", tags=["Parts"])


# 📌 Точка входа (запуск сервера)
if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)), reload=True)
