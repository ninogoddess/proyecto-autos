"""
Servicio de opciones del formulario.
Expone las categorías válidas extraídas del dataset de entrenamiento.
Modelos agrupados por marca (limpios, sin basura).
"""

import json
from pathlib import Path

from ..services.preprocessor import (
    MANUFACTURERS,
    FUELS,
    TRANSMISSIONS,
    TYPES,
    CONDITIONS,
    TITLE_STATUSES,
    DRIVES,
    PAINT_COLORS,
)

_artifacts_dir = Path(__file__).resolve().parent.parent / "artifacts"

# Cargar modelos por marca
_MODELS_BY_MANUFACTURER: dict[str, list[str]] = {}
_models_path = _artifacts_dir / "models_by_manufacturer.json"
if _models_path.exists():
    with open(_models_path, "r", encoding="utf-8") as f:
        _MODELS_BY_MANUFACTURER = json.load(f)

# Cargar mapeo modelo → tipo de vehículo
_MODEL_TYPE_MAP: dict[str, str] = {}
_type_map_path = _artifacts_dir / "model_type_map.json"
if _type_map_path.exists():
    with open(_type_map_path, "r", encoding="utf-8") as f:
        _MODEL_TYPE_MAP = json.load(f)


def get_options() -> dict:
    """
    Retorna las opciones válidas para los campos del formulario.
    Los modelos están agrupados por marca (limpios y filtrados).
    """
    all_manufacturers = sorted(["acura"] + MANUFACTURERS)
    all_fuels = sorted(["diesel"] + FUELS)
    all_transmissions = sorted(["automatic"] + TRANSMISSIONS)
    all_types = sorted(["SUV"] + TYPES)
    all_conditions = sorted(["excellent"] + CONDITIONS)
    all_title_statuses = sorted(["clean"] + TITLE_STATUSES)
    all_drives = sorted(["4wd"] + DRIVES)
    all_paint_colors = sorted(["black"] + PAINT_COLORS)

    return {
        "manufacturers": all_manufacturers,
        "models_by_manufacturer": _MODELS_BY_MANUFACTURER,
        "model_type_map": _MODEL_TYPE_MAP,
        "fuels": all_fuels,
        "transmissions": all_transmissions,
        "types": all_types,
        "conditions": all_conditions,
        "title_statuses": all_title_statuses,
        "drives": all_drives,
        "paint_colors": all_paint_colors,
    }
