from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import pandas as pd
from model_manager import load_model
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Lista de horas para las predicciones
HORAS = ['4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00',
         '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
         '19:00', '20:00', '21:00', '22:00']

# Función compartida para procesar predicciones
async def procesar_prediccion(fecha: str, linea_servicio: str):
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
    dia = fecha_dt.day
    mes = fecha_dt.month
    dia_semana = fecha_dt.weekday()

    entrada = pd.DataFrame([{
        "dia": dia,
        "mes": mes,
        "dia_semana": dia_semana,
        "Linea de servicio": linea_servicio
    }])

    modelo = load_model("model/mejor_modelo_pasajeros.pkl")
    if modelo is None:
        raise Exception("No se pudo cargar el modelo.")

    predicciones = modelo.predict(entrada)[0]
    return list(zip(HORAS, map(lambda x: round(x), predicciones)))

# Endpoint para formulario HTML tradicional
@app.post("/calcular_pasajeros", response_class=HTMLResponse)
async def calcular_pasajeros(
    request: Request,
    fecha: str = Form(...),
    linea_servicio: str = Form(...)
):
    try:
        resultado = await procesar_prediccion(fecha, linea_servicio)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "resultado": resultado,
            "fecha": fecha,
            "linea": linea_servicio
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })

# Endpoint para API JSON
@app.post("/calcular_pasajeros_json")
async def calcular_pasajeros_json(request: Request):
    try:
        data = await request.json()
        fecha = data.get("fecha")
        linea_servicio = data.get("linea_servicio")
        
        if not fecha or not linea_servicio:
            return {"error": "Faltan campos requeridos: fecha, linea_servicio"}
        
        resultado = await procesar_prediccion(fecha, linea_servicio)
        
        # Formato de respuesta para JSON
        return {
            "fecha": fecha,
            "linea_servicio": linea_servicio,
            "predicciones": [{"hora": hora, "pasajeros": pasajeros} for hora, pasajeros in resultado],
            "status": "success"
        }
    except ValueError as e:
        return {"error": f"Formato de fecha inválido: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

# Endpoint raíz
@app.get("/", response_class=HTMLResponse)
async def form_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})