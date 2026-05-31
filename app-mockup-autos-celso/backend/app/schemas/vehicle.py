"""
Schemas Pydantic para validación de datos de entrada y salida.
Definen el contrato de la API con tipos estrictos.
"""

from pydantic import BaseModel, Field
from typing import Optional


class VehicleInput(BaseModel):
    """
    Datos del vehículo para predicción de precio.
    Todos los campos son obligatorios y validados.
    """
    manufacturer: str = Field(
        ...,
        min_length=1,
        description="Marca del vehículo (ej: toyota, ford, chevrolet)",
        json_schema_extra={"example": "toyota"}
    )
    model: str = Field(
        ...,
        min_length=1,
        description="Modelo específico del vehículo (ej: camry, f-150)",
        json_schema_extra={"example": "camry"}
    )
    year: int = Field(
        ...,
        ge=1981,
        le=2024,
        description="Año del vehículo (entre 1981 y 2024)",
        json_schema_extra={"example": 2018}
    )
    odometer: int = Field(
        ...,
        ge=1,
        le=299999,
        description="Kilometraje del vehículo (entre 1 y 299999)",
        json_schema_extra={"example": 45000}
    )
    fuel: str = Field(
        ...,
        min_length=1,
        description="Tipo de combustible (gas, diesel, electric, hybrid, other)",
        json_schema_extra={"example": "gas"}
    )
    transmission: str = Field(
        ...,
        min_length=1,
        description="Tipo de transmisión (automatic, manual, other)",
        json_schema_extra={"example": "automatic"}
    )
    type: str = Field(
        ...,
        min_length=1,
        description="Tipo de vehículo (sedan, SUV, truck, pickup, etc.)",
        json_schema_extra={"example": "sedan"}
    )
    condition: str = Field(
        default="unknown",
        description="Condición del vehículo (excellent, good, fair, like new, new, salvage, unknown)",
        json_schema_extra={"example": "good"}
    )
    cylinders: Optional[str] = Field(
        default=None,
        description="Cilindros del motor (ej: '4 cylinders', '6 cylinders'). Si no se proporciona, se usa 0.",
        json_schema_extra={"example": "4 cylinders"}
    )
    title_status: str = Field(
        default="clean",
        description="Estado del título (clean, lien, missing, parts only, rebuilt, salvage)",
        json_schema_extra={"example": "clean"}
    )
    drive: str = Field(
        default="unknown",
        description="Tipo de tracción (4wd, fwd, rwd, unknown)",
        json_schema_extra={"example": "fwd"}
    )
    paint_color: str = Field(
        default="unknown",
        description="Color de pintura del vehículo",
        json_schema_extra={"example": "white"}
    )


class PredictionResponse(BaseModel):
    """Respuesta exitosa con el precio predicho."""
    predicted_price_usd: float = Field(
        ...,
        description="Precio predicho en USD (desnormalizado)"
    )
    predicted_price_clp: int = Field(
        ...,
        description="Precio predicho en CLP (convertido con tasa de cambio)"
    )
    vehicle_data: dict = Field(
        ...,
        description="Datos del vehículo consultado"
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Advertencias sobre la predicción (modelo/marca no reconocidos, etc.)"
    )


class HealthResponse(BaseModel):
    """Respuesta del endpoint de salud."""
    status: str = Field(..., description="Estado del servicio")
    model_loaded: bool = Field(..., description="Si el modelo ML está cargado en memoria")
    version: str = Field(..., description="Versión de la API")


class ErrorResponse(BaseModel):
    """Respuesta de error genérica."""
    detail: str = Field(..., description="Mensaje de error descriptivo")


class ValidationErrorDetail(BaseModel):
    """Detalle de un error de validación por campo."""
    field: str = Field(..., description="Nombre del campo con error")
    message: str = Field(..., description="Descripción del error")
