import numpy as np
def obj2dict(session_object):
    # Filtrar solo las claves que son columnas de la base de datos
    columnas_validas = [column.name for column in session_object.__table__.columns]
    # Crear un diccionario con las columnas y valores
    datos_dict = {column: getattr(session_object, column) for column in columnas_validas}

    vec_suma = [
    i if i != None else np.nan for k, i in datos_dict.items() if "semana" in k
    ]

    acumulador = 0
    vec_grafica = {}
    for i,v in enumerate(vec_suma):
        if not np.isnan(v):
            acumulador += v
        vec_grafica[f"semana {i+1}"] = acumulador

    return vec_grafica, np.nansum(vec_suma)