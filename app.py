from fastapi import FastAPI, Request, File, UploadFile, Form, status, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from pathlib import Path
import logging

import warnings
warnings.filterwarnings("ignore")

## Create directorys necessary
# Path('temp').mkdir(parents=True, exist_ok=True)
Path('logs').mkdir(parents=True, exist_ok=True)
# Path('modules/backend/db').mkdir(parents=True, exist_ok=True)
# Path('modules/backend/models').mkdir(parents=True, exist_ok=True)

## Create database
# db.create_db()

# Configure logging
logging.basicConfig(filename = 'logs/lamaria.log')
logger = logging.getLogger('ai_app')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', '%d-%m-%Y %I:%M:%S %p')
console_handler = logging.StreamHandler()

# Crete app
app = FastAPI()
logging.info('Iniciando App')

## Create templates

app.mount("/static", StaticFiles(directory="modules/static"), name="static")
templates = Jinja2Templates(directory="modules/static/templates")

## Home page
@app.get("/LaMaria/home")
def home(request: Request):
    title = 'Finca La Marina'
    return templates.TemplateResponse("main.html",{"request": request, "title": title})