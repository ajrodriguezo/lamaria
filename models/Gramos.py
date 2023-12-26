from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from models import db
import numpy as np
from modules import helpers

Base = db.base

class Gramos(Base):
    __tablename__ = 'gramos'
    id = Column(String, primary_key=True)
    
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
        
    @classmethod
    def update(cls, ciclo_id, dict_update):
        try:
            interaction_to_update = db.session.query(cls).filter_by(gramos_owner_id=ciclo_id).first()
            if interaction_to_update:
                for key, value in dict_update.items():
                    setattr(interaction_to_update, key, value)

                db.session.commit()
                return f"Actualizacion de {ciclo_id}"
            else:
                print(f"No se encontró la interacción con ciclo_id {ciclo_id}")
                return None
        except Exception as e:
            print("Error ", e)
            db.session.rollback()
            return f"Error en actualizacion de {ciclo_id}"
        
    @classmethod
    def getById(cls, ciclo_id):
        try:
            last_interaction = db.session.query(cls).filter_by(gramos_owner_id=ciclo_id).first()
            if last_interaction:
                return last_interaction
        except Exception as e:
            print("Error ", e)
            return None
        
for c in range(1, 21):
    setattr(Gramos, f'semana_{c}', Column(Float, default= np.nan))