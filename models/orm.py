from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from models import db

Base = db.base

class Database(Base):
    __tablename__ = 'LaMariaCosecha'

    ciclo_id = Column(String, primary_key = True)
    fecha = Column(Date)

for c in range(1, 21):
    setattr(Database, f'ciclo_{c}', Column(Float))


    