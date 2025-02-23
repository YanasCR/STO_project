from pydantic import BaseModel
from enum import Enum

# Возможные статусы запчастей
class PartStatus(str, Enum):
    not_purchased = "not_purchased"  # Не закуплена
    purchased = "purchased"  # Закуплена
    received = "received"  # Получена

# Базовая схема запчасти
class PartBase(BaseModel):
    name: str
    car_id: int
    status: PartStatus = PartStatus.not_purchased

# Схема для создания запчасти
class PartCreate(PartBase):
    pass

# Схема для обновления запчасти
class PartUpdate(BaseModel):
    status: PartStatus

# Схема для ответа
class PartResponse(PartBase):
    id: int

    class Config:
        from_attributes = True
