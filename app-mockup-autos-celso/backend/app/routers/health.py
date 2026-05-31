"""
Router para el endpoint de salud del servicio.
Permite verificar que la API está operativa y el modelo cargado.
"""

from fastapi import APIRouter

from ..config.settings import API_VERSION
from ..schemas.vehicle import HealthResponse
from ..utils.model_loader import artifacts

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Verificar estado del servicio",
    description="Retorna el estado de la API y si el modelo ML está cargado en memoria.",
)
def health_check() -> HealthResponse:
    """Endpoint de salud para monitoreo y verificación."""
    return HealthResponse(
        status="ok" if artifacts.is_loaded else "degraded",
        model_loaded=artifacts.is_loaded,
        version=API_VERSION,
    )
