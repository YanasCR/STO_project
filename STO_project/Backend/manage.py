import sys
import uvicorn
from database import Base, engine, SessionLocal
from app.models.user import User
from passlib.hash import bcrypt

def create_tables():
    """Создает таблицы в базе данных"""
    Base.metadata.create_all(engine)
    print("✅ Таблицы успешно созданы!")

def drop_tables():
    """Удаляет все таблицы из базы данных"""
    Base.metadata.drop_all(engine)
    print("⚠️ Все таблицы удалены!")

def create_admin():
    """Создает администратора с дефолтными данными"""
    db = SessionLocal()
    email = "admin@example.com"
    password = "admin123"
    existing_user = db.query(User).filter(User.email == email).first()
    
    if existing_user:
        print("❌ Администратор уже существует!")
    else:
        admin = User(email=email, password=bcrypt.hash(password), role="admin")
        db.add(admin)
        db.commit()
        print(f"✅ Администратор создан: {email} / {password}")

    db.close()

def run():
    """Запускает FastAPI сервер"""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

def show_help():
    """Выводит список доступных команд"""
    print("""
Управление проектом:

python manage.py migrate    - Создать таблицы в БД
python manage.py dropdb     - Удалить все таблицы
python manage.py createsuperuser - Создать администратора
python manage.py runserver  - Запустить сервер FastAPI
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
    else:
        command = sys.argv[1]
        if command == "migrate":
            create_tables()
        elif command == "dropdb":
            drop_tables()
        elif command == "createsuperuser":
            create_admin()
        elif command == "runserver":
            run()
        else:
            print("❌ Неизвестная команда!")
            show_help()
