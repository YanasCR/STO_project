from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="не закуплена")

    car = relationship("Car", back_populates="parts")  # Связь с таблицей машин
