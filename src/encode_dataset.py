import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler  # 👈 NUEVO

# =========================================================
# CONFIGURACIÓN DE RUTAS
# =========================================================
INPUT_PATH = "data/processed/vehicles_processed.csv"
OUTPUT_PATH = "data/processed/vehicles_processed_nums.csv"

# =========================================================
# CARGA DE DATOS
# =========================================================
print("Cargando dataset...")
df = pd.read_csv(INPUT_PATH)

# =========================================================
# JUSTIFICACIÓN GENERAL DEL PROCESAMIENTO
# =========================================================
"""
Este proceso tiene como objetivo transformar el dataset en una representación
100% numérica, necesaria para el correcto funcionamiento de modelos de regresión.

Decisiones clave:
1. Las variables categóricas deben convertirse a formato numérico.
2. Se evita el uso de One-Hot Encoding en variables de alta cardinalidad.
3. Se preserva la información relevante mediante técnicas más eficientes.
4. Se eliminan variables irrelevantes para el contexto del problema.
5. Se normalizan variables numéricas continuas para mejorar el rendimiento del modelo.
"""

# =========================================================
# ELIMINACIÓN DE VARIABLE 'state'
# =========================================================
if "state" in df.columns:
    print("Eliminando columna 'state'...")
    df = df.drop(columns=["state"])

# =========================================================
# TARGET ENCODING PARA 'model'
# =========================================================
if "model" in df.columns:
    print("Aplicando target encoding a 'model'...")

    model_price_map = df.groupby("model")["price"].mean()

    df["model_encoded"] = df["model"].map(model_price_map)

    df = df.drop(columns=["model"])

    model_price_map.to_csv("data/processed/model_encoding_map.csv")

# =========================================================
# TRANSFORMACIÓN DE 'cylinders'
# =========================================================
if "cylinders" in df.columns:
    print("Procesando 'cylinders'...")

    df["cylinders"] = (
        df["cylinders"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(float)
    )

# =========================================================
# IDENTIFICACIÓN DE VARIABLES CATEGÓRICAS
# =========================================================
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

print("Columnas categóricas detectadas:")
print(categorical_cols)

# =========================================================
# ONE-HOT ENCODING
# =========================================================
print("Aplicando One-Hot Encoding...")
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# =========================================================
# MANEJO DE VALORES NULOS
# =========================================================
print("Rellenando valores NaN...")
df = df.fillna(0)

# =========================================================
# NORMALIZACIÓN DE VARIABLES NUMÉRICAS CONTINUAS
# =========================================================
"""
JUSTIFICACIÓN:
Las variables numéricas pueden estar en distintas escalas, lo que afecta
negativamente a modelos de regresión lineal y regularizados.

Se aplica StandardScaler para:
- Centrar los datos en media 0
- Escalar a desviación estándar 1

IMPORTANTE:
No se escalan variables binarias (one-hot), ya que ya están en escala adecuada (0-1).
"""

print("Aplicando normalización (StandardScaler)...")

# Detectar columnas numéricas reales (excluyendo binarias)
numeric_cols = df.select_dtypes(include=["number"]).columns

# Filtrar columnas binarias (solo 0 y 1)
non_binary_cols = [
    col for col in numeric_cols
    if not set(df[col].unique()).issubset({0, 1})
]

scaler = StandardScaler()
df[non_binary_cols] = scaler.fit_transform(df[non_binary_cols])

# =========================================================
# VERIFICACIÓN FINAL
# =========================================================
print("Verificando que todo sea numérico...")
non_numeric = df.select_dtypes(exclude=["number"]).columns

if len(non_numeric) > 0:
    print("Columnas NO numéricas encontradas:")
    print(non_numeric)
else:
    print("Dataset completamente numérico ✔")

# =========================================================
# GUARDADO DEL DATASET
# =========================================================
os.makedirs("data/processed", exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print("Dataset guardado en:")
print(OUTPUT_PATH)

print(f"Shape final del dataset: {df.shape}")