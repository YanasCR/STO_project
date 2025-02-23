from pydantic import BaseModel
from enum import Enum

# Возможные статусы работы
class WorkStatus(str, Enum):
    planned = "planned"  # Запланировано
    in_progress = "in_progress"  # В процессе
    completed = "completed"  # Выполнено

# Базовая схема работы
class WorkBase(BaseModel):
    name: str
    car_id: int
    mechanic_id: int
    status: WorkStatus = WorkStatus.planned

# Схема для создания работы
class WorkCreate(WorkBase):
    pass

# Схема для обновления работы
class WorkUpdate(BaseModel):
    status: WorkStatus

# Схема для ответа
class WorkResponse(WorkBase):
    id: int

    class Config:
        from_attributes = True
