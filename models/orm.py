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
            print(new_interaction)
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
                    print(key, value)
                    setattr(interaction_to_update, key, value)

                db.session.commit()
                return interaction_to_update
            else:
                print(f"No se encontró la interacción con ciclo_id {ciclo_id}")
                return None
        except Exception as e:
            print("Error ", e)
            db.session.rollback()
            return None

    ### Consultas
    @classmethod
    def getLastId(cls):
        try:
            # Consulta para obtener la última interacción por fecha descendente
            last_interaction = db.session.query(cls).order_by(cls.fecha.desc()).first()
            return last_interaction
        except Exception as e:
            print("Error ", e)
            return "No_found"
        


for c in range(1, 21):
    setattr(Database, f'ciclo_{c}', Column(Float))


    