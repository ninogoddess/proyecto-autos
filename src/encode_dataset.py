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

Esto permite:
- Evitar errores en sklearn (que no acepta strings)
- Mejorar la eficiencia computacional
- Reducir el riesgo de sobreajuste
"""

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

Esto permite:
- Mantener la información predictiva
- Reducir dimensionalidad
- Mejorar el rendimiento del modelo
"""

if "model" in df.columns:
    print("Aplicando target encoding a 'model'...")

    # Crear mapa: modelo → precio promedio
    model_price_map = df.groupby("model")["price"].mean()

    # Aplicar encoding
    df["model_encoded"] = df["model"].map(model_price_map)

    # Eliminar columna original
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

Transformarla a número permite:
- Preservar su significado ordinal
- Facilitar el aprendizaje del modelo
"""

if "cylinders" in df.columns:
    print("Procesando 'cylinders'...")

    df["cylinders"] = (
        df["cylinders"]
        .astype(str)
        .str.extract(r"(\d+)")  # extrae el número
        .astype(float)
    )

# =========================================================
# IDENTIFICACIÓN DE VARIABLES CATEGÓRICAS
# =========================================================
"""
Se identifican automáticamente todas las columnas tipo texto
para aplicar codificación.
"""

categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

print("Columnas categóricas detectadas:")
print(categorical_cols)

# =========================================================
# ONE-HOT ENCODING
# =========================================================
"""
JUSTIFICACIÓN:
Para variables categóricas de baja o media cardinalidad,
se aplica One-Hot Encoding.

Esto permite:
- Evitar introducir relaciones ordinales falsas
- Representar correctamente categorías independientes

Se usa drop_first=True para evitar multicolinealidad.
"""

print("Aplicando One-Hot Encoding...")
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# =========================================================
# MANEJO DE VALORES NULOS
# =========================================================
"""
JUSTIFICACIÓN:
Los modelos de sklearn no aceptan valores NaN.

Se reemplazan por 0 como solución simple y consistente.
(En versiones más avanzadas se podría usar imputación más sofisticada)
"""

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

