import numpy as np
import uuid

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
        if "semana" in k:
            if i != None:
                acumulador += i
            vec_grafica.append({"x":  n, "y": acumulador})
            # " ".join(k.split("_"))
    return vec_grafica

def generate_semana_id():
    return str(uuid.uuid4())[:8]

def generate_ciclo_id(fecha):
    return "ciclo_"+ fecha.strftime("%y/%m/%d") + "-" +  str(uuid.uuid4())[:3]