from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.car_schema import CarCreate, CarUpdate, CarResponse
from app.services.car_service import create_car, get_cars, get_car, update_car, delete_car
from app.models.car import Car
from typing import Optional

router = APIRouter()

# CREATE (Добавить новую машину с валидацией VIN)
@router.post("/", response_model=CarResponse)
def add_car(car: CarCreate, db: Session = Depends(get_db)):
    # Проверяем, есть ли машина с таким VIN в базе
    existing_car = db.query(Car).filter(Car.vin == car.vin).first()
    if existing_car:
        raise HTTPException(status_code=400, detail="Car with this VIN already exists")

    return create_car(db, car)

# READ (Получить список машин с пагинацией)
@router.get("/", response_model=list[CarResponse])
def list_cars(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_cars(db, skip, limit)

# READ (Получить одну машину по ID)
@router.get("/{car_id}", response_model=CarResponse)
def retrieve_car(car_id: int, db: Session = Depends(get_db)):
    car = get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

# READ (Поиск машины по VIN)
@router.get("/vin/{vin}", response_model=CarResponse)
def retrieve_car_by_vin(vin: str, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.vin == vin).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

# READ (Фильтрация машин по марке и году)
@router.get("/filter/", response_model=list[CarResponse])
def filter_cars(
    brand: Optional[str] = Query(None, description="Filter by car brand"),
    year: Optional[int] = Query(None, description="Filter by car year"),
    db: Session = Depends(get_db)
):
    query = db.query(Car)
    if brand:
        query = query.filter(Car.brand == brand)
    if year:
        query = query.filter(Car.year == year)
    
    cars = query.all()
    return cars

# UPDATE (Обновить данные машины)
@router.put("/{car_id}", response_model=CarResponse)
def modify_car(car_id: int, car_data: CarUpdate, db: Session = Depends(get_db)):
    updated_car = update_car(db, car_id, car_data)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated_car

# DELETE (Удалить машину, возвращая объект)
@router.delete("/{car_id}", response_model=CarResponse)
def remove_car(car_id: int, db: Session = Depends(get_db)):
    deleted_car = delete_car(db, car_id)
    if not deleted_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return deleted_car  # Возвращаем удаленную машину
