from fastapi import FastAPI, Request, File, UploadFile, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import os
from pathlib import Path
from datetime import datetime
import logging
import warnings

warnings.filterwarnings("ignore")

from models.Ciclo import Ciclo
from models.Precios import Precios
from models.Gramos import Gramos
from models import query
from models import db
from modules import helpers

Path('logs').mkdir(parents=True, exist_ok=True)

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

dict_normalzate = {
    "grsemana": "gr acumulados",
    "precioseman": "Precio promedio",
    "semana": "No. semana"
}

## Create templates
app.mount("/static", StaticFiles(directory="modules/static"), name="static")
templates = Jinja2Templates(directory="modules/static/templates")

## Home page
@app.get("/LaMaria/home")
def home(request: Request):
    title = 'Finca La Marina'
    lastId = Ciclo.getLastActive()
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
            _ , prom_precio = helpers.suma_y_promedio(result_dict_pr)

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
    
    print(datos_grafica)
    return templates.TemplateResponse("main.html",{"request": request, "title": title, 
                                                   "datos_grafica": datos_grafica, "total_gr": total_gr,
                                                   "prom_precio": round(prom_precio,2),
                                                   "gr_faltante": gr_faltantes,
                                                   "vendido": round(vendido,2),
                                                   "relacion_gr": relacion_gr})

## Ingreso Datos
@app.get("/LaMaria/ingresoDatos")
async def datos(request: Request):
    title = 'Finca La Marina'
    return templates.TemplateResponse("datos.html",{"request": request, "title": title})


@app.post("/LaMaria/ingresoDatos/actualizarSemana")
async def actalizarSemana(request: Request, valores: dict): # int = Form(...), precioseman: float = Form(...), semana: int = Form(...)):
    print(valores)
    for val in valores:
        if valores[val] == "":
            err = f"Falta el parametro: {dict_normalzate[val]}"
            raise HTTPException(status_code=400, detail=str(err))

    grsemana = valores["grsemana"]
    precioseman = valores["precioseman"]
    semana = valores["semana"]

    print("Gr Acumulados:", grsemana)
    print("Precio Promedio:", precioseman)
    print("Número de Semana:", semana)
    
    lastId = Ciclo.getLastActive()
    if lastId:
        id = lastId.ciclo_id

        objPrecios = Precios.getById(id)
        print(objPrecios)
        if objPrecios: 
            dictPrecios = helpers.obj2dict(objPrecios)
            valuesSemana = []

            for key, value in dictPrecios.items():
                if key == f"semana_{semana}":
                    break
                elif "semana" in key and value is None:
                    valuesSemana.append(key.split("_")[1])

            
            if valuesSemana != []:
                txt = " ".join(valuesSemana)
                err = f"Falta información de las semanas {txt}; antes de ingresar la semana {semana}"
                raise HTTPException(status_code=400, detail=str(err))
            

            try:
                Precios.update(ciclo_id = id, dict_update = {
                    f"semana_{semana}": precioseman
                })
            except Exception as e:
                print(e)
                err = "En la actualización de datos. Por favor intentelo de nuevo"
                print(err)
                raise HTTPException(status_code=400, detail=str(err))

            try:
                Gramos.update(ciclo_id = id, dict_update = {
                    f"semana_{semana}": round(float(grsemana) * (1000 / 80000), 2 )
                })
                
                txt = f"Actualizacion correcta de la semana {semana} del clcio: {id}"
                print(txt)

            except Exception as e:
                print(e)
                err = "En la actualización de datos. Por favor intentelo de nuevo"
                print(err)
                raise HTTPException(status_code=400, detail=str(err))
            
        else:
            
            if semana != "1":
                err = f"El ciclo {id} debe iniciar con la semana 1 para continuar"
                print(err)
                raise HTTPException(status_code=400, detail=str(err))


            try:
                Precios.add({
                    "precio_owner_id": id,
                    f"semana_1": precioseman
                })
            except Exception as e:
                print(e)
                print("Error guardado bd precio")
                err = "En la actualización de datos. Por favor intentelo de nuevo"
                print(err)
                raise HTTPException(status_code=400, detail=str(err))

            try:
                Gramos.add({
                    "id" : db.session.query(Precios).filter_by(precio_owner_id=id).first().id,
                    "gramos_owner_id": id,
                    f"semana_1": grsemana
                })
                
                txt = f"Actualizacion correcta de la semana {semana} del clcio: {id}"
                print(txt)
            except Exception as e:
                print(e)
                err = "En la actualización de datos. Por favor intentelo de nuevo"
                print(err)
                raise HTTPException(status_code=400, detail=str(err))

    
    else:
        err = "En la actualización de datos. Por favor intentelo de nuevo"
        print(err)
        raise HTTPException(status_code=400, detail=str(err))

    return {"success": True, "message": txt}

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

        txt = f"Se creo correctamente el ciclo con fecha de inicio {date}"
        print(txt)
        return {"success": True, "message": txt}     

@app.post("/LaMaria/ingresoDatos/FinalizarCiclo")
async def enviar_booleano_endpoint2(request: Request, valor: dict):
    valor_booleano = valor 
    print(f"Valor booleano recibido en el Endpoint 2: {valor_booleano}")
    
    lastId = Ciclo.getLastActive()
    if lastId:
        id = lastId.ciclo_id        
        try:
            Ciclo.update(ciclo_id=id, dict_update= {
                "activa": False,
                "fecha_final": datetime.now().date()
            })
            txt = f"Actualizacion correcta del clcio: {id }"
            print(txt)
            return {"success": True, "message": txt} 
        except Exception as e:
            err = "Error en la actualizacion. Por favor intentelo de nuevo"
            raise HTTPException(status_code=400, detail=str(err))

    else:
        err = "No existe un ciclo en curso"
        print(err)
        raise HTTPException(status_code=400, detail=str(err))

    

