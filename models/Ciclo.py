from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, Time
from sqlalchemy.orm import relationship
from models import db
import numpy as np
from models.Precios import Precios
from models.Gramos import Gramos

Base = db.base

class Ciclo(Base):
    __tablename__ = 'ciclo'
    ciclo_id = Column(String, primary_key = True)
    activa = Column(Boolean)
    fecha_inicial = Column(Date)
    fecha_final = Column(Date)

    gramos_id = relationship("Gramos", back_populates="gramos_owner")
    precio_id = relationship("Precios", back_populates="precio_owner")

    #Acciones
    @classmethod
    def add(cls, dict_new):

        cont = [1 if k in dict_new.keys() else 0 for k in ["ciclos", "precio", "gramo"]]
            
        flag = False
        if sum(cont) == 3:
            dict_ciclo = dict_new["ciclos"]
            dict_precio = dict_new["precio"]
            dict_gramo = dict_new["gramo"]
            id = dict_ciclo["ciclo_id"]

            dict_precio["precio_owner_id"] = id
            dict_gramo["gramos_owner_id"] = id

            flag = True
        elif sum(cont) > 1:
            raise Exception("No estan los parametros completos")

        try:
            if flag:
                Ciclo.add(dict_ciclo)
                Precios.add(dict_precio)
                dict_gramo["id"] = db.session.query(Precios).filter_by(precio_owner_id=id).first().id
                Gramos.add(dict_gramo)
            else:
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
            last_interaction = db.session.query(cls).order_by(cls.fecha_inicial.desc()).first()
            return last_interaction
        except Exception as e:
            print("Error ", e)
            return None
        

"""
for c in range(1, 21):
    setattr(Ciclo, f'semana_{c}', Column(Float, default= np.nan))
"""

    