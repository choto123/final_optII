from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import pandas as pd
from model_manager import load_model

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Lista de horas (asegúrate de que coincidan con las columnas del modelo)
HORAS = ['4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00',
         '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
         '19:00', '20:00', '21:00', '22:00']


@app.get("/", response_class=HTMLResponse)
async def form_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/calcular_pasajeros", response_class=HTMLResponse)
async def calcular_pasajeros(
    request: Request,
    fecha: str = Form(...),
    linea_servicio: str = Form(...)
):
    try:
        # Procesar fecha
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        dia = fecha_dt.day
        mes = fecha_dt.month
        dia_semana = fecha_dt.weekday()

        # Preparar datos para predicción
        entrada = pd.DataFrame([{
            "dia": dia,
            "mes": mes,
            "dia_semana": dia_semana,
            "Línea de servicio": linea_servicio
        }])

        # Cargar el modelo y predecir
        modelo = load_model("model/mejor_modelo_pasajeros.pkl")
        if modelo is None:
            raise Exception("No se pudo cargar el modelo.")

        predicciones = modelo.predict(entrada)[0]  # Extraer array plano

        # Juntar resultados por hora
        resultado = list(zip(HORAS, map(lambda x: round(x), predicciones)))

        return templates.TemplateResponse("index.html", {
            "request": request,
            "resultado": resultado,
            "fecha": fecha,
            "linea": linea_servicio
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "resultado": [],
            "error": str(e)
        })
    