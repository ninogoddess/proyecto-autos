"""
Router para el endpoint de predicción de precios.
Recibe datos del vehículo y retorna el precio estimado.
"""

import logging

from fastapi import APIRouter, HTTPException

from ..schemas.vehicle import VehicleInput, PredictionResponse, ErrorResponse
from ..services.prediction import predict_price

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Predicción"])


@router.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        422: {"description": "Datos de entrada inválidos"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
        503: {"model": ErrorResponse, "description": "Modelo no disponible"},
    },
    summary="Predecir precio de un vehículo",
    description=(
        "Recibe las características de un vehículo y retorna una estimación "
        "de precio basada en el modelo Random Forest entrenado. "
        "Los campos obligatorios son: manufacturer, model, year, odometer, "
        "fuel, transmission y type."
    ),
)
def predict(vehicle: VehicleInput) -> PredictionResponse:
    """
    Endpoint principal de predicción.
    
    Flujo:
    1. Validación automática por Pydantic (422 si falla)
    2. Preprocesamiento (replica pipeline de entrenamiento)
    3. Inferencia con Random Forest
    4. Desnormalización del precio
    5. Conversión USD → CLP
    """
    try:
        result = predict_price(vehicle)
        return result

    except RuntimeError as e:
        # Modelo no cargado o error de inferencia
        logger.error(f"Error de predicción: {e}")
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )

    except Exception as e:
        # Error inesperado
        logger.exception(f"Error inesperado en predicción: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor. La predicción no pudo completarse.",
        )
