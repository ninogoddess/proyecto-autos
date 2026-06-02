"""
Configuración centralizada del backend.
Carga variables de entorno desde .env (desarrollo) o del sistema (producción).
Todos los valores tienen defaults razonables para desarrollo local.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Cargar .env si existe (desarrollo local)
# En producción, las variables se inyectan directamente en el entorno
_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_FILE, override=False)

# ── Rutas base ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent.parent  # proyecto-autos/

# ── Artefactos ML ───────────────────────────────────────────────────────────
MODEL_PATH: str = os.getenv(
    "MODEL_PATH",
    str(PROJECT_ROOT / "models" / "random_forest" / "model.pkl")
)

ENCODING_MAP_PATH: str = os.getenv(
    "ENCODING_MAP_PATH",
    str(PROJECT_ROOT / "data" / "processed" / "model_encoding_map.csv")
)

# ── Servidor ─────────────────────────────────────────────────────────────────
PORT: int = int(os.getenv("PORT", "8000"))
HOST: str = os.getenv("HOST", "0.0.0.0")

# ── CORS ─────────────────────────────────────────────────────────────────────
ALLOWED_ORIGINS: list[str] = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
).split(",")

# ── Parámetros de negocio ────────────────────────────────────────────────────
EXCHANGE_RATE_USD_CLP: float = float(os.getenv("EXCHANGE_RATE_USD_CLP", "950"))

# ── Logging ──────────────────────────────────────────────────────────────────
# Valores válidos: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

# ── Metadatos de la API ──────────────────────────────────────────────────────
API_VERSION: str = "1.0.0"
API_TITLE: str = "API de Predicción de Precios de Vehículos"
API_DESCRIPTION: str = """
API REST para predicción de precios de vehículos usados mediante
un modelo Random Forest entrenado con datos de Craigslist (EE.UU.).

Proyecto universitario — Ciencia de Datos, UNAB.
"""
