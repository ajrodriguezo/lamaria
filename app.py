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

from models.orm import Database
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

Database.add({
    'ciclo_id': 'ciclo_test1',
    'fecha': fecha_actual - timedelta(days=1),
    'semana_1': 10,
    'semana_2': 100,
    'semana_3': 100,
    'semana_4': 400
})

Database.add({
    'ciclo_id': 'ciclo_test2',
    'fecha': fecha_actual,
    'semana_1': 0,
    'semana_2': 1,
    'semana_3': 50,
    'semana_4': 3
})

Database.update(ciclo_id = 'ciclo_test2', dict_update= {'semana_4': 0})

Database.delete(ciclo_id = 'ciclo_test1')

print("Ultima session", Database.getLastId().ciclo_id, Database.getLastId().fecha)

## Create templates
app.mount("/static", StaticFiles(directory="modules/static"), name="static")
templates = Jinja2Templates(directory="modules/static/templates")

## Home page
@app.get("/LaMaria/home")
def home(request: Request):
    title = 'Finca La Marina'
    lastId = Database.getLastId()

    if lastId:
        result_dict = helpers.obj2dict(lastId)
        # Total
        total_ciclo = helpers.suma_total(result_dict)
        # Total
        datos_grafica = helpers.ajustar_grafica(result_dict)
    else:
        print("No hay resultados")
        result_dict["error"] = "No hay resultados"
        total_ciclo = 0
    return templates.TemplateResponse("main.html",{"request": request, "title": title, "datos_grafica": datos_grafica, "total_ciclo": total_ciclo})

## Ingreso Datos
@app.get("/LaMaria/ingresoDatos")
async def home(request: Request):
    print
    title = 'Finca La Marina'
    return templates.TemplateResponse("datos.html",{"request": request, "title": title})

