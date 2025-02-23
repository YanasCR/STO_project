from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="запланировано")

    car = relationship("Car", back_populates="works")  # <-- Проверяем это!
