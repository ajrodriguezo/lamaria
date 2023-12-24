def obj2dict(session_object):
    # Filtrar solo las claves que son columnas de la base de datos
    columnas_validas = [column.name for column in session_object.__table__.columns]
    # Crear un diccionario con las columnas y valores
    datos_dict = {column: getattr(session_object, column) for column in columnas_validas}

    return datos_dict