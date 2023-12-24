from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from models import db

Base = db.base

class Database(Base):
    __tablename__ = 'LaMariaCosecha'

    ciclo_id = Column(String, primary_key = True)
    fecha = Column(Date)

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
            interaction_to_update = db.session.query(cls).filter_by(ciclo_id=ciclo_id).first()
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
    def delete(cls, ciclo_id):
        try:
            interaction_to_delete = db.session.query(cls).filter_by(ciclo_id=ciclo_id).first()

            if interaction_to_delete:
                db.session.delete(interaction_to_delete)
                db.session.commit()
                return "Eliminado Exitosamente"
            else:
                print(f"No se encontró la interacción con ciclo_id {ciclo_id}")
                return "Error: No se encontró la interacción"
        except Exception as e:
            print("Error ", e)
            db.session.rollback()
            return "Error en la eliminación"

    ### Consultas
    @classmethod
    def getLastId(cls):
        try:
            # Consulta para obtener la última interacción por fecha descendente
            last_interaction = db.session.query(cls).order_by(cls.fecha.desc()).first()
            return last_interaction
        except Exception as e:
            print("Error ", e)
            return None
        


for c in range(1, 21):
    setattr(Database, f'ciclo_{c}', Column(Float))


    