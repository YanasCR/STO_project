from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL, DB_ECHO

# Создаем движок базы данных
engine = create_engine(DATABASE_URL, echo=DB_ECHO, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функци¤ для получения сессии базы данных (используетс¤ в зависимостях FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
