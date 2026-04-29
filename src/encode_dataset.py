import pandas as pd
import numpy as np
import os

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

Esto permite:
- Evitar errores en sklearn (que no acepta strings)
- Mejorar la eficiencia computacional
- Reducir el riesgo de sobreajuste
"""

# =========================================================
# ELIMINACIÓN DE VARIABLE 'state'
# =========================================================
"""
JUSTIFICACIÓN:
La variable 'state' representa estados de EE.UU., lo cual no es relevante
para el contexto del problema, orientado a un sistema de predicción aplicable en Chile.

Mantener esta variable introduciría ruido geográfico irrelevante
y podría afectar negativamente el aprendizaje del modelo.
"""

if "state" in df.columns:
    print("Eliminando columna 'state'...")
    df = df.drop(columns=["state"])

# =========================================================
# TARGET ENCODING PARA 'model'
# =========================================================
"""
JUSTIFICACIÓN:
La variable 'model' es altamente relevante para predecir el precio,
pero posee una cardinalidad muy alta (muchos valores únicos).

Aplicar One-Hot Encoding generaría miles de columnas, lo que:
- Aumenta drásticamente la dimensionalidad
- Genera sobreajuste
- Aumenta el costo computacional

SOLUCIÓN:
Se aplica Target Encoding:
Cada modelo se reemplaza por el precio promedio asociado a ese modelo.
"""

if "model" in df.columns:
    print("Aplicando target encoding a 'model'...")

    model_price_map = df.groupby("model")["price"].mean()

    df["model_encoded"] = df["model"].map(model_price_map)

    df = df.drop(columns=["model"])

    # Guardar mapping de modelos
    model_price_map.to_csv("data/processed/model_encoding_map.csv")

# =========================================================
# TRANSFORMACIÓN DE 'cylinders'
# =========================================================
"""
JUSTIFICACIÓN:
La variable 'cylinders' está en formato texto (ej: "8 cylinders"),
pero representa una magnitud numérica real.
"""

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