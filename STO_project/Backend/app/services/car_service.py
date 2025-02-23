from sqlalchemy.orm import Session
from app.models.car import Car
from app.schemas.car_schema import CarCreate, CarUpdate

# CREATE (Создать машину)
def create_car(db: Session, car_data: CarCreate):
    new_car = Car(**car_data.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

# READ (Получить список машин)
def get_cars(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Car).offset(skip).limit(limit).all()

# READ (Получить одну машину по ID)
def get_car(db: Session, car_id: int):
    return db.query(Car).filter(Car.id == car_id).first()

# UPDATE (Обновить машину)
def update_car(db: Session, car_id: int, car_data: CarUpdate):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return None
    for key, value in car_data.model_dump().items():
        setattr(car, key, value)
    db.commit()
    db.refresh(car)
    return car

# DELETE (Удалить машину)
def delete_car(db: Session, car_id: int):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return None
    db.delete(car)
    db.commit()
    return car
