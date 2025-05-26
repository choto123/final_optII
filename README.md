# Predicción de precios de bicicletas
 
Explicación del proyecto y su funcionamiento.
/bike_prices
|
|-- main.py
|-- data/
|   |-- Libro1.csv(contiene base de datos de usuarios del metro de medellin)
|-- model/
|   |-- model.pkl
|-- templates/
|   |-- index.html
|-- static/
|   |-- style.css
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- model_builder.py
|-- model_manager.py
 

## Ejecución del proyecto
 
1. Clonar el repositorio `git remote add origin https://github.com/choto123/final_optII.git
git branch -M main
git push -u origin main`
```bash
git clone
```
 
2. Crear un entorno virtual:
 
```bash
python -m venv .venv
```
 
3. Activar el entorno virtual:
 
```bash
.venv\Scripts\activate
```
 
4. Instalar las dependencias:
 
```bash
pip install -r requirements.txt
```
 
5. Lanzar la aplicación:
 
```bash
uvicorn main:app --reload
```
 
6. Abrir el navegador y acceder a `http://localhost:8000`
 
 ## Importante
 Para poder crear el "model.pkl" es necesario ejecutar el "model_builder.py" con este se creara el archivo.

 1. ejecutar el model_builder.py
 2. ejecutar el main.py
 3. lanzar el entorno vitual