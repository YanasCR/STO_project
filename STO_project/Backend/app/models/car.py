from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    vin = Column(String, unique=True, index=True)

    works = relationship("Work", back_populates="car", cascade="all, delete")
    parts = relationship("Part", back_populates="car", cascade="all, delete") 