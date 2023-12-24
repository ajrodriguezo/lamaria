from fastapi import FastAPI, Request, File, UploadFile, Form, status, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import os
from pathlib import Path
import logging
import warnings
warnings.filterwarnings("ignore")

from config.database import SessionLocal, engine, Base
from modules.orm import Database
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
    os.remove("tmp.db")
except: pass

# Crete app
app = FastAPI()
logging.info('Iniciando App')

## Create database
Base.metadata.create_all(bind = engine)

# Example
Session = SessionLocal
session = Session()

new_row = Database(ciclo_id='ciclo_test1', ciclo_1=10, ciclo_2=100, ciclo_3=100, ciclo_4 = 400,)
session.add(new_row)

new_row = Database(ciclo_id='ciclo_test2', ciclo_1=0, ciclo_2=150, ciclo_3=500, ciclo_4 = 300,)
session.add(new_row)
session.commit()

## Create templates

app.mount("/static", StaticFiles(directory="modules/static"), name="static")
templates = Jinja2Templates(directory="modules/static/templates")

## Home page
@app.get("/LaMaria/home")
def home(request: Request):
    title = 'Finca La Marina'
    return templates.TemplateResponse("main.html",{"request": request, "title": title})

## Ingreso Datos
@app.get("/LaMaria/ingresoDatos")
async def home(request: Request):
    print
    title = 'Finca La Marina'
    return templates.TemplateResponse("datos.html",{"request": request, "title": title})


session.close()