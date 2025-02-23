from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.work import Work
from app.schemas.work_schema import WorkCreate, WorkUpdate
from app.middlewares.auth_middleware import get_current_user

router = APIRouter()

# 🔹 Добавить новую работу
@router.post("/", response_model=WorkCreate)
def add_work(work: WorkCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_work = Work(name=work.name, car_id=work.car_id, status="pending", mechanic_id=user.id)
    db.add(new_work)
    db.commit()
    db.refresh(new_work)
    return new_work

# 🔹 Получить все работы по ID машины
@router.get("/{car_id}")
def get_works(car_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    works = db.query(Work).filter(Work.car_id == car_id).all()
    return works

# 🔹 Получить конкретную работу по ID
@router.get("/work/{work_id}")
def get_work(work_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    work = db.query(Work).filter(Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Работа не найдена")
    return work

# 🔹 Обновить статус работы
@router.put("/{work_id}", response_model=WorkUpdate)
def update_work(work_id: int, work_update: WorkUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    work = db.query(Work).filter(Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Работа не найдена")
    work.status = work_update.status
    db.commit()
    db.refresh(work)
    return work

# 🔹 Удалить работу
@router.delete("/{work_id}")
def delete_work(work_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    work = db.query(Work).filter(Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Работа не найдена")
    db.delete(work)
    db.commit()
    return {"message": "Работа удалена"}

# 🔹 Получить работы по статусу
@router.get("/status/{status}")
def get_works_by_status(status: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    works = db.query(Work).filter(Work.status == status).all()
    return works
