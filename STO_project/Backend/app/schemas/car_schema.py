from pydantic import BaseModel, Field

# Создание машины
class CarCreate(BaseModel):
    brand: str
    model: str
    year: int
    vin: str = Field(..., min_length=17, max_length=17, pattern="^[A-HJ-NPR-Z0-9]+$")  # VIN-код 17 символов

# Обновление машины
class CarUpdate(BaseModel):
    brand: str
    model: str
    year: int

# Ответ от API
class CarResponse(CarCreate):
    id: int

    class Config:
        orm_mode = True
