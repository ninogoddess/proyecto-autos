"""
Schemas Pydantic para validación y sanitización de datos de entrada y salida.
Los field_validators normalizan los strings antes de la lógica de negocio.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


# Valores válidos para campos categóricos
_VALID_FUELS = {"gas", "diesel", "electric", "hybrid", "other"}
_VALID_TRANSMISSIONS = {"automatic", "manual", "other"}
_VALID_CONDITIONS = {"excellent", "good", "fair", "like new", "new", "salvage", "unknown"}
_VALID_TITLE_STATUSES = {"clean", "lien", "missing", "parts only", "rebuilt", "salvage"}
_VALID_DRIVES = {"4wd", "fwd", "rwd", "unknown"}


class VehicleInput(BaseModel):
    """
    Datos del vehículo para predicción de precio.
    Los strings se normalizan automáticamente (strip + lowercase).
    """

    manufacturer: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Marca del vehículo (ej: toyota, ford, chevrolet)",
        json_schema_extra={"example": "toyota"},
    )
    model: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Modelo específico del vehículo (ej: camry, f-150)",
        json_schema_extra={"example": "camry"},
    )
    year: int = Field(
        ...,
        ge=1981,
        le=2024,
        description="Año de fabricación del vehículo (entre 1981 y 2024)",
        json_schema_extra={"example": 2018},
    )
    odometer: int = Field(
        ...,
        ge=1,
        le=299999,
        description="Kilometraje del vehículo (entre 1 y 299.999 km)",
        json_schema_extra={"example": 45000},
    )
    fuel: str = Field(
        ...,
        description=f"Tipo de combustible. Valores válidos: {sorted(_VALID_FUELS)}",
        json_schema_extra={"example": "gas"},
    )
    transmission: str = Field(
        ...,
        description=f"Tipo de transmisión. Valores válidos: {sorted(_VALID_TRANSMISSIONS)}",
        json_schema_extra={"example": "automatic"},
    )
    type: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Tipo de carrocería (sedan, SUV, truck, pickup, etc.)",
        json_schema_extra={"example": "sedan"},
    )
    condition: str = Field(
        default="unknown",
        description=f"Condición del vehículo. Valores válidos: {sorted(_VALID_CONDITIONS)}",
        json_schema_extra={"example": "good"},
    )
    cylinders: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Cilindros del motor (ej: '4 cylinders'). Opcional.",
        json_schema_extra={"example": "4 cylinders"},
    )
    title_status: str = Field(
        default="clean",
        description=f"Estado del título. Valores válidos: {sorted(_VALID_TITLE_STATUSES)}",
        json_schema_extra={"example": "clean"},
    )
    drive: str = Field(
        default="unknown",
        description=f"Tipo de tracción. Valores válidos: {sorted(_VALID_DRIVES)}",
        json_schema_extra={"example": "fwd"},
    )
    paint_color: str = Field(
        default="unknown",
        max_length=20,
        description="Color de pintura del vehículo",
        json_schema_extra={"example": "white"},
    )

    # ── Sanitización automática ────────────────────────────────────────────────

    @field_validator("manufacturer", "model", "type", "paint_color", mode="before")
    @classmethod
    def normalize_string(cls, v: str) -> str:
        """Elimina espacios al inicio/fin y convierte a minúsculas."""
        if not isinstance(v, str):
            raise ValueError("Debe ser un texto")
        normalized = v.strip().lower()
        if not normalized:
            raise ValueError("El campo no puede estar vacío o contener solo espacios")
        return normalized

    @field_validator("fuel", mode="before")
    @classmethod
    def validate_fuel(cls, v: str) -> str:
        normalized = v.strip().lower() if isinstance(v, str) else ""
        if normalized not in _VALID_FUELS:
            raise ValueError(f"Combustible inválido. Opciones: {sorted(_VALID_FUELS)}")
        return normalized

    @field_validator("transmission", mode="before")
    @classmethod
    def validate_transmission(cls, v: str) -> str:
        normalized = v.strip().lower() if isinstance(v, str) else ""
        if normalized not in _VALID_TRANSMISSIONS:
            raise ValueError(f"Transmisión inválida. Opciones: {sorted(_VALID_TRANSMISSIONS)}")
        return normalized

    @field_validator("condition", mode="before")
    @classmethod
    def validate_condition(cls, v: str) -> str:
        normalized = v.strip().lower() if isinstance(v, str) else "unknown"
        if normalized not in _VALID_CONDITIONS:
            return "unknown"  # fallback seguro
        return normalized

    @field_validator("title_status", mode="before")
    @classmethod
    def validate_title_status(cls, v: str) -> str:
        normalized = v.strip().lower() if isinstance(v, str) else "clean"
        if normalized not in _VALID_TITLE_STATUSES:
            return "clean"  # fallback seguro
        return normalized

    @field_validator("drive", mode="before")
    @classmethod
    def validate_drive(cls, v: str) -> str:
        normalized = v.strip().lower() if isinstance(v, str) else "unknown"
        if normalized not in _VALID_DRIVES:
            return "unknown"  # fallback seguro
        return normalized

    @field_validator("cylinders", mode="before")
    @classmethod
    def sanitize_cylinders(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not isinstance(v, str):
            return None
        return v.strip() or None


class PredictionResponse(BaseModel):
    """Respuesta exitosa con el precio predicho."""

    predicted_price_usd: float = Field(
        ..., description="Precio predicho en USD"
    )
    predicted_price_clp: int = Field(
        ..., description="Precio predicho en CLP"
    )
    vehicle_data: dict = Field(
        ..., description="Datos del vehículo consultado"
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Advertencias sobre la predicción",
    )


class HealthResponse(BaseModel):
    """Respuesta del endpoint de salud."""

    status: str = Field(..., description="Estado del servicio: ok | degraded")
    model_loaded: bool = Field(..., description="Si el modelo está cargado en memoria")
    version: str = Field(..., description="Versión de la API")


class ErrorResponse(BaseModel):
    """Respuesta de error genérica."""

    detail: str = Field(..., description="Mensaje de error descriptivo")


class ValidationErrorDetail(BaseModel):
    """Detalle de un error de validación por campo."""

    field: str = Field(..., description="Campo con error")
    message: str = Field(..., description="Descripción del error")
