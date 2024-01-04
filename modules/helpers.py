import numpy as np
import uuid
from datetime import datetime

def obj2dict(session_object):
    # Filtrar solo las claves que son columnas de la base de datos
    columnas_validas = [column.name for column in session_object.__table__.columns]
    # Crear un diccionario con las columnas y valores
    datos_dict = {column: getattr(session_object, column) for column in columnas_validas}
    return datos_dict

def suma_y_promedio(datos_dict):
    vec_suma = [
        i if i is not None else np.nan for k, i in datos_dict.items() if "semana" in k
    ]
    
    suma_total = np.nansum(vec_suma)
    cantidad_valores = len(vec_suma) - np.isnan(vec_suma).sum()
    
    promedio = suma_total / cantidad_valores if cantidad_valores > 0 else 0
    
    return suma_total, promedio

def ajustar_grafica(datos_dict):
    acumulador = 0
    vec_grafica = []
    for n, (k,i) in enumerate(datos_dict.items()):
        if n == 0: bf = i
        if "semana" in k:
            if i != None:
                acumulador += i
            vec_grafica.append({"x":  n, "y": acumulador})
            # " ".join(k.split("_"))
        if bf == None and i == None: break
        bf = i
    return vec_grafica

def generate_semana_id():
    return str(uuid.uuid4())[:8]

def generate_ciclo_id(fecha):
    print(fecha)
    return "ciclo_"+ str(fecha) + "-" +  str(uuid.uuid4())[:3]

def verf_date(date:str, current_date:datetime):
    input_date = datetime.strptime(date, "%Y-%m-%d").date()

    if input_date > current_date:
        return None
    else:
        return input_date
    