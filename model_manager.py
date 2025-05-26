import os
import pickle

def load_model(model_path: str = "models/mejor_modelo_pasajeros.pkl"):
    """
    Carga un modelo de predicción desde un archivo pickle.

    Parámetros:
    - model_path (str): Ruta del archivo del modelo.

    Retorna:
    - object: El modelo cargado (pipeline de sklearn) o None si falla.
    """
    if not os.path.exists(model_path):
        print(f"❌ El archivo del modelo no existe en la ruta: {model_path}")
        return None

    try:
        with open(model_path, "rb") as file:
            modelo = pickle.load(file)
        print(f"✅ Modelo cargado exitosamente desde: {model_path}")
        return modelo
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
        return None
