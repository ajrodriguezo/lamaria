from fastapi import FastAPI, Request, File, UploadFile, Form, status, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import os
from pathlib import Path
from datetime import datetime, timedelta
import logging
import warnings
warnings.filterwarnings("ignore")

from models.Ciclo import Ciclo
from models.Precios import Precios
from models.Gramos import Gramos
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

        
    else:
        print("No hay resultados")
        total_gr = 0
    return templates.TemplateResponse("main.html",{"request": request, "title": title, 
                                                   "datos_grafica": datos_grafica, "total_gr": total_gr,
                                                   "prom_precio": prom_precio})

## Ingreso Datos
@app.get("/LaMaria/ingresoDatos")
async def home(request: Request):
    print
    title = 'Finca La Marina'
    return templates.TemplateResponse("datos.html",{"request": request, "title": title})

