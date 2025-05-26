import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

# --- CONFIGURACIÓN ---
horas = ['4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00',
         '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
         '19:00', '20:00', '21:00', '22:00']

# --- CARGAR DATOS ---
df = pd.read_csv('data/Libro1.csv', encoding='latin1', sep=';')

# --- PROCESAMIENTO DE FECHAS ---
df['Día'] = pd.to_datetime(df['Día'], dayfirst=True, errors='coerce')
df = df.dropna(subset=['Día'])

df['dia'] = df['Día'].dt.day
df['mes'] = df['Día'].dt.month
df['dia_semana'] = df['Día'].dt.dayofweek  # lunes=0, domingo=6

# --- COMPLETAR VALORES NULOS EN HORAS ---
df[horas] = df[horas].apply(pd.to_numeric, errors='coerce')
df[horas] = df.groupby('Línea de servicio')[horas].transform(lambda x: x.fillna(x.mean()))
df = df.dropna(subset=horas)

# --- SELECCIONAR VARIABLES ---
X = df[['dia', 'mes', 'dia_semana', 'Línea de servicio']]
y = df[horas]

# --- MODELO ---
# Codificar la línea de servicio
preprocesador = ColumnTransformer([
    ('linea', OneHotEncoder(drop='first'), ['Línea de servicio'])
], remainder='passthrough')

modelo = Pipeline([
    ('preprocesador', preprocesador),
    ('regresor', MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42)))
])

# --- ENTRENAR ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
modelo.fit(X_train, y_train)

# --- EVALUACIÓN ---
y_pred = modelo.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"✅ RMSE: {rmse:.2f}")

# --- GUARDAR MODELO ---
with open("model/mejor_modelo_pasajeros.pkl", "wb") as f:
    pickle.dump(modelo, f)

print("✅ Modelo de predicción de pasajeros guardado exitosamente.")
