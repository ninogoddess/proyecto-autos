"""
Punto de entrada principal de la API FastAPI.
Configura CORS, carga el modelo al inicio y registra los routers.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config.settings import (
    ALLOWED_ORIGINS,
    API_DESCRIPTION,
    API_TITLE,
    API_VERSION,
    ENCODING_MAP_PATH,
    MODEL_PATH,
)
from .routers import health, options, predict
from .utils.model_loader import artifacts

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Evento de ciclo de vida del servidor.
    Carga el modelo al inicio (una sola vez).
    """
    logger.info("🚀 Iniciando servidor...")
    logger.info(f"   Modelo: {MODEL_PATH}")
    logger.info(f"   Encoding map: {ENCODING_MAP_PATH}")
    logger.info(f"   CORS origins: {ALLOWED_ORIGINS}")

    # Carga del modelo (operación pesada, ~10-30s para 1.5GB)
    artifacts.load(MODEL_PATH, ENCODING_MAP_PATH)

    if artifacts.is_loaded:
        logger.info("✅ Servidor listo para recibir solicitudes")
    else:
        logger.warning(
            f"⚠️ Servidor iniciado SIN modelo cargado. "
            f"Error: {artifacts.load_error}"
        )

    yield  # El servidor está corriendo

    # Cleanup al apagar
    logger.info("🛑 Apagando servidor...")


# Crear aplicación FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Registrar routers con prefijo /api/v1
app.include_router(health.router, prefix="/api/v1")
app.include_router(options.router, prefix="/api/v1")
app.include_router(predict.router, prefix="/api/v1")


# Manejador global de errores de validación (formato personalizado)
@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    """Formatea errores de validación Pydantic en formato legible."""
    errors = []
    if hasattr(exc, "errors"):
        for error in exc.errors():
            field = " → ".join(str(loc) for loc in error.get("loc", []))
            errors.append({
                "field": field,
                "message": error.get("msg", "Error de validación"),
            })
    else:
        errors.append({
            "field": "unknown",
            "message": str(exc),
        })

    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )


# Endpoint raíz
@app.get("/", tags=["Root"])
def root():
    """Endpoint raíz con información básica de la API."""
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health",
    }
