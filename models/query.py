from models.Ciclo import Ciclo
from models.Precios import Precios
from models.Gramos import Gramos
from models import db

def getAllElementsColumn(tabla, columna):
    resultados = db.session.query(tabla).with_entities(getattr(tabla, columna)).all()
    return [result[0] for result in resultados]
