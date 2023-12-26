from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from models import db
import numpy as np
from modules import helpers

Base = db.base

class Gramos(Base):
    __tablename__ = 'gramos'
    semana_id = Column(String, primary_key=True)
    
    gramos_owner_id = Column(String, ForeignKey("ciclo.ciclo_id"))
    gramos_owner = relationship("Ciclo", back_populates="gramos_id")

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
        
for c in range(1, 21):
    setattr(Gramos, f'semana_{c}', Column(Float, default= np.nan))