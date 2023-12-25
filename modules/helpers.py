import numpy as np
def obj2dict(session_object):
    # Filtrar solo las claves que son columnas de la base de datos
    columnas_validas = [column.name for column in session_object.__table__.columns]
    # Crear un diccionario con las columnas y valores
    datos_dict = {column: getattr(session_object, column) for column in columnas_validas}
    return datos_dict

def suma_total(datos_dict):
    vec_suma = [
    i if i != None else np.nan for k, i in datos_dict.items() if "semana" in k
    ]
    return np.nansum(vec_suma)

def ajustar_grafica(datos_dict):
    acumulador = 0
    vec_grafica = []
    for k,i in datos_dict.items():
        if "semana" in k:
            if i != None:
                acumulador += i
            vec_grafica.append({'x': " ".join(k.split("_")) , 'y': acumulador})

    print(vec_grafica)
    return vec_grafica