from fastapi import FastAPI, Request, File, UploadFile, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import os
from pathlib import Path
from datetime import datetime, timedelta
import logging
import warnings

from starlette import status
from starlette.routing import URL

warnings.filterwarnings("ignore")

from models.Ciclo import Ciclo
from models.Precios import Precios
from models.Gramos import Gramos
from models import query
from models import db
from modules import helpers

## Create directorys necessary
# Path('temp').mkdir(parents=True, exist_ok=True)
Path('logs').mkdir(parents=True, exist_ok=True)
# Path('modules/backend/db').mkdir(parents=True, exist_ok=True)
# Path('modules/backend/models').mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(filename = 'logs/lamaria.log')
logger = logging.getLogger('ai_app')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', '%d-%m-%Y %I:%M:%S %p')
console_handler = logging.StreamHandler()

try:
    print("Eliminando db ... ")
    os.remove("tmp.db")
except: pass

# Crete app
app = FastAPI()
logging.info('Iniciando App')


db.base.metadata.create_all(bind = db.engine)

# Example
fecha_actual = datetime.now().date()

"""

Ciclo.add({
    'ciclo_id': 'ciclo_test2',
    'activa' : True,
    'fecha_inicial': fecha_actual,
})

Precios.add({
    "semana_1": 10.0,
})

Gramos.add({
    "semana_id":"ahjski",
    "semana_1": 10.0
})
"""

Ciclo.add({
    "ciclos":{
        'ciclo_id': 'ciclo_test3',
        'activa' : True,
        'fecha_inicial': fecha_actual
        },
    "precio": {
        "semana_1": 10.0,
        'semana_2': 11.2,
        'semana_3': 10.2,
        'semana_4': 9.2
    },
    "gramo": {
        "semana_1": 10.0,
        'semana_2': 100,
        'semana_3': 100,
        'semana_4': 400
    },
})

Precios.update(ciclo_id= "ciclo_test3", dict_update= {
    "semana_1": 7.0,
})

Gramos.update(ciclo_id= "ciclo_test3", dict_update= {
    "semana_1": 110
})


print("Ultima session", Ciclo.getLastId().ciclo_id, Ciclo.getLastId().fecha_inicial)

print("Ultima session. Precios", Precios.getById(Ciclo.getLastId().ciclo_id).precio_owner_id)
print("Ultima session. Gramos", Gramos.getById(Ciclo.getLastId().ciclo_id).gramos_owner_id)


## Create templates
app.mount("/static", StaticFiles(directory="modules/static"), name="static")
templates = Jinja2Templates(directory="modules/static/templates")

## Home page
@app.get("/LaMaria/home")
def home(request: Request):
    title = 'Finca La Marina'
    lastId = Ciclo.getLastId()
    if lastId:
        
        id = lastId.ciclo_id
        if Precios.getById(id):

            gr_goal = 7000
            ## Gramos
            objGramos = Gramos.getById(id)
            result_dict_gr = helpers.obj2dict(objGramos)
            # Total
            total_gr, _ = helpers.suma_y_promedio(result_dict_gr)
            # Ajustes
            datos_grafica = helpers.ajustar_grafica(result_dict_gr)

            ## Precio
            objPrecio = Precios.getById(id)
            result_dict_pr = helpers.obj2dict(objPrecio)
            # Promedio
            _ , prom_precio = helpers.suma_y_promedio(result_dict_gr)

            # Otros
            gr_faltantes = gr_goal - total_gr
            vendido = total_gr * prom_precio
            relacion_gr = int((total_gr * 100) / gr_goal)
            print("Extraccion correcta")
        else:
            print("No se ha ingresado informacion")
    else:
        print("No hay resultados")
        datos_grafica = [{}]
        total_gr, prom_precio, gr_faltantes, vendido = 0, 0, 0, 0
        relacion_gr = 0
    return templates.TemplateResponse("main.html",{"request": request, "title": title, 
                                                   "datos_grafica": datos_grafica, "total_gr": total_gr,
                                                   "prom_precio": prom_precio,
                                                   "gr_faltante": gr_faltantes,
                                                   "vendido": vendido,
                                                   "relacion_gr": relacion_gr})

## Ingreso Datos
@app.get("/LaMaria/ingresoDatos")
async def datos(request: Request):
    title = 'Finca La Marina'
    return templates.TemplateResponse("datos.html",{"request": request, "title": title})

@app.post("/LaMaria/ingresoDatos")
async def datos(request: Request, grsemana: int = Form(...), precioseman: float = Form(...), semana: int = Form(...)):
    
    title = 'Finca La Marina'

    print("Gr Acumulados:", grsemana)
    print("Precio Promedio:", precioseman)
    print("Número de Semana:", semana)
    
    lastId = Ciclo.getLastActive()
    if lastId:
        id = lastId.ciclo_id
        if Precios.getById(id):
            try:
                Precios.update(ciclo_id = id, dict_update = {
                    f"semana_{semana}": precioseman
                })
            except Exception as e:
                print(e)
                print("Error actualizacion bd precio")

            try:
                Gramos.update(ciclo_id = id, dict_update = {
                    f"semana_{semana}": grsemana
                })
                print("Se actualizo con exito")
            except Exception as e:
                print(e)
                print("Error actualizacion bd gramos")
            
        else:
            try:
                Precios.add({
                    "precio_owner_id": id,
                    f"semana_{semana}": precioseman
                })
            except Exception as e:
                print(e)
                print("Error guardado bd precio")

            try:
                Gramos.add({
                    "id" : db.session.query(Precios).filter_by(precio_owner_id=id).first().id,
                    "gramos_owner_id": id,
                    f"semana_{semana}": grsemana
                })
                
                print("Se guardo con exito")
            except Exception as e:
                print(e)
                print("Error guardado bd gramos")

    
    else: print("Error, no hay ciclos activos")

    return templates.TemplateResponse("datos.html",{"request": request, "title": title})

@app.post("/LaMaria/ingresoDatos/CrearCiclo")
async def enviar_booleano_endpoint2(request: Request, valor: dict):
    data = valor
    print(f"Valor booleano recibido en el Endpoint 1")
    
    if data["fechaInicio"] != "":
        fecha_actual = datetime.now().date()
        date = helpers.verf_date( data["fechaInicio"] , fecha_actual)
    else:
        err = "Debe elegir una fecha de inicio de ciclo"
        print(err)
        raise HTTPException(status_code=400, detail=str(err))

    if date is None:
        err = f"La fecha no debe ser mayor al dia de hoy {fecha_actual}"
        print(err)
        raise HTTPException(status_code=400, detail=str(err))

    col_activo = query.getAllElementsColumn(Ciclo, "activa")
    
    print(col_activo)

    if True in col_activo:
        err = "Ya existe un ciclo en curso"
        print(err)
        raise HTTPException(status_code=400, detail=str(err))
    else:
        
        try:
            Ciclo.add({
                'ciclo_id': helpers.generate_ciclo_id(date),
                'activa' : True,
                'fecha_inicial': date,
            })
        except Exception as e:
            print(e)
            err = "En la creacion ciclo. Por favor intentelo de nuevo"
            print(err)
            raise HTTPException(status_code=400, detail=str(err))

        print("Creacion exitosa")        

@app.post("/LaMaria/ingresoDatos/FinalizarCiclo")
async def enviar_booleano_endpoint2(request: Request, valor: dict):
    valor_booleano = valor 
    print(f"Valor booleano recibido en el Endpoint 2: {valor_booleano}")
    
    col_id = query.getAllElementsColumn(Ciclo, "ciclo_id")
    col_activo = query.getAllElementsColumn(Ciclo, "activa")
    
    tmp_ids, tmp_flag = [], []
    if True in col_activo:
        for id, f in zip(col_id, col_activo):
            if f: tmp_ids.append(id); tmp_flag.append(f)

        if len(tmp_ids) == 1 and len(tmp_flag) == 1:
            # Actualizacion
            try:
                Ciclo.update(ciclo_id= tmp_ids[0], dict_update= {
                    "activa": False,
                    "fecha_final": datetime.now().date()
                })
                print("Actualizacion correcta")
            except Exception as e:
                err = "Error en la actualizacion. Por favor intentelo de nuevo"
                raise HTTPException(status_code=400, detail=str(err))
        else:
            err = "Datos dañados"
            print(err)
            raise HTTPException(status_code=400, detail=str(err))
    else:
        err = "No existe un ciclo en curso"
        print(err)
        raise HTTPException(status_code=400, detail=str(err))

    

