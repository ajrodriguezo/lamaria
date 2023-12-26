from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from models import db
import numpy as np

Base = db.base

class Semana(Base):
    __tablename__ = 'semana'
    semana_id = Column(String, primary_key=True)
    gr_metro = Column(Float)
    precio_prom = Column(Float)
    
    ciclos_id = Column(String, ForeignKey("ciclo.ciclo_id"))
    owner = relationship("Ciclo", back_populates="semana_id")

    #Acciones
    @classmethod
    def add(cls, dict_new):
        try:
            new_interaction = cls(**dict_new)
            db.session.add(new_interaction)
            db.session.commit()
            return "Creado Exitosamente"
        except Exception as e:
            print("Error ", e)
            db.session.rollback()
            return "Error en la creación"