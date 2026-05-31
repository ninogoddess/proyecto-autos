"""
Configuración centralizada del backend.
Usa variables de entorno con valores por defecto para desarrollo local.
"""

import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent.parent  # proyecto-autos/

# Modelo ML
MODEL_PATH = os.getenv(
    "MODEL_PATH",
    str(PROJECT_ROOT / "models" / "random_forest" / "model.pkl")
)

# Encoding map para target encoding de la columna 'model'
ENCODING_MAP_PATH = os.getenv(
    "ENCODING_MAP_PATH",
    str(PROJECT_ROOT / "data" / "processed" / "model_encoding_map.csv")
)

# Servidor
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

# CORS
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
).split(",")

# Tasa de cambio USD → CLP (configurable)
EXCHANGE_RATE_USD_CLP = float(os.getenv("EXCHANGE_RATE_USD_CLP", "950"))

# Versión de la API
API_VERSION = "1.0.0"
API_TITLE = "API de Predicción de Precios de Vehículos"
API_DESCRIPTION = """
API REST para predicción de precios de vehículos usados mediante
un modelo Random Forest entrenado con datos de Craigslist.

Proyecto universitario - Ciencia de Datos, UNAB.
"""
