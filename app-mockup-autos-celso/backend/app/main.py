"""
Punto de entrada principal de la API FastAPI.
Configura logging, CORS, carga el modelo y registra los routers.
"""

import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config.settings import (
    ALLOWED_ORIGINS,
    API_DESCRIPTION,
    API_TITLE,
    API_VERSION,
    ENCODING_MAP_PATH,
    LOG_LEVEL,
    MODEL_PATH,
)
from .routers import health, options, predict
from .utils.model_loader import artifacts

# ── Configurar logging ────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Ciclo de vida del servidor ────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el modelo al iniciar y libera recursos al apagar."""
    logger.info("=" * 60)
    logger.info("🚀 Iniciando API de Predicción de Precios de Vehículos")
    logger.info(f"   Versión   : {API_VERSION}")
    logger.info(f"   Log Level : {LOG_LEVEL}")
    logger.info(f"   CORS      : {ALLOWED_ORIGINS}")
    logger.info(f"   Modelo    : {MODEL_PATH}")
    logger.info("=" * 60)

    artifacts.load(MODEL_PATH, ENCODING_MAP_PATH)

    if artifacts.is_loaded:
        logger.info("✅ Servidor listo — modelo cargado en memoria")
    else:
        logger.warning(f"⚠️  Servidor iniciado SIN modelo. Error: {artifacts.load_error}")

    yield

    logger.info("🛑 Apagando servidor...")


# ── Aplicación FastAPI ────────────────────────────────────────────────────────
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middleware CORS ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


# ── Middleware de request logging ─────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Registra cada request con método, ruta y tiempo de respuesta."""
    request_id = str(uuid.uuid4())[:8]
    start = time.time()

    logger.info(f"→ [{request_id}] {request.method} {request.url.path}")

    response = await call_next(request)
    elapsed_ms = (time.time() - start) * 1000

    logger.info(
        f"← [{request_id}] {response.status_code} "
        f"({elapsed_ms:.1f}ms)"
    )
    return response


# ── Manejador de errores de validación (422) ──────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Formatea errores de validación Pydantic en estructura legible.
    Siempre retorna un array de {field, message} consistente.
    """
    errors = []
    for error in exc.errors():
        # Extraer campo ignorando el prefijo "body"
        loc = error.get("loc", [])
        field = " → ".join(str(l) for l in loc if l != "body")
        errors.append({
            "field": field or "desconocido",
            "message": error.get("msg", "Valor inválido"),
        })

    logger.warning(f"Validación fallida en {request.url.path}: {len(errors)} error(es)")

    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )


# ── Manejador de errores inesperados (500) ────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Captura excepciones no controladas para evitar caídas completas."""
    logger.exception(f"Error no controlado en {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor. Intenta nuevamente."},
    )


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(health.router, prefix="/api/v1")
app.include_router(options.router, prefix="/api/v1")
app.include_router(predict.router, prefix="/api/v1")


# ── Endpoint raíz ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    """Información básica de la API."""
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health",
    }
