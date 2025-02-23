from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.part import Part
from app.schemas.part_schema import PartCreate, PartUpdate
from app.middlewares.auth_middleware import get_current_user

router = APIRouter()

# 🔹 Добавить запчасть
@router.post("/", response_model=PartCreate)
def add_part(part: PartCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_part = Part(name=part.name, car_id=part.car_id, status="not purchased")
    db.add(new_part)
    db.commit()
    db.refresh(new_part)
    return new_part

# 🔹 Получить все запчасти по ID машины
@router.get("/{car_id}")
def get_parts(car_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    parts = db.query(Part).filter(Part.car_id == car_id).all()
    return parts

# 🔹 Получить конкретную запчасть по ID
@router.get("/part/{part_id}")
def get_part(part_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Запчасть не найдена")
    return part

# 🔹 Обновить статус запчасти
@router.put("/{part_id}", response_model=PartUpdate)
def update_part(part_id: int, part_update: PartUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Запчасть не найдена")
    part.status = part_update.status
    db.commit()
    db.refresh(part)
    return part

# 🔹 Удалить запчасть
@router.delete("/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Запчасть не найдена")
    db.delete(part)
    db.commit()
    return {"message": "Запчасть удалена"}

# 🔹 Получить запчасти по статусу
@router.get("/status/{status}")
def get_parts_by_status(status: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    parts = db.query(Part).filter(Part.status == status).all()
    return parts
