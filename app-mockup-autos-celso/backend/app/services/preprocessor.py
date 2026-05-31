"""
Motor de preprocesamiento para inferencia.

Replica EXACTAMENTE el pipeline de entrenamiento:
1. MinMaxScaler para year y odometer (notebook 02)
2. Target Encoding para 'model' (precio promedio por modelo)
3. Extracción numérica de 'cylinders'
4. One-Hot Encoding con drop_first para categóricas
5. Relleno de NaN con 0
6. StandardScaler para variables numéricas continuas (encode_dataset.py)

PIPELINE COMPLETO DESCUBIERTO:
- Notebook 02: MinMax a [price, year, odometer] → [0,1]
- encode_dataset.py: Target Encoding model, extraer cylinders, OHE categóricas, fillna(0)
- encode_dataset.py: StandardScaler a columnas numéricas no binarias
  (price, year, cylinders, odometer, lat, long, model_encoded)

Para inferencia replicamos:
1. year → MinMax → StandardScaler
2. odometer → MinMax → StandardScaler
3. cylinders → extraer número → StandardScaler
4. lat/long → valores por defecto → StandardScaler
5. model → Target Encoding → StandardScaler
6. Categóricas → One-Hot (sin escalar)
"""

import logging
import numpy as np
import pandas as pd
from typing import Optional

from ..schemas.vehicle import VehicleInput
from ..utils.model_loader import artifacts

logger = logging.getLogger(__name__)

# Columnas one-hot esperadas por el modelo (extraídas del dataset de entrenamiento)
# Estas son las categorías con drop_first=True

MANUFACTURERS = [
    "alfa-romeo", "aston-martin", "audi", "bmw", "buick", "cadillac",
    "chevrolet", "chrysler", "datsun", "dodge", "ferrari", "fiat",
    "ford", "gmc", "harley-davidson", "honda", "hyundai", "infiniti",
    "jaguar", "jeep", "kia", "land rover", "lexus", "lincoln", "mazda",
    "mercedes-benz", "mercury", "mini", "mitsubishi", "nissan", "pontiac",
    "porsche", "ram", "rover", "saturn", "subaru", "tesla", "toyota",
    "volkswagen", "volvo"
]
# La primera categoría (drop_first) es "acura" (no aparece en las columnas)

FUELS = ["electric", "gas", "hybrid", "other"]
# drop_first: "diesel"

TRANSMISSIONS = ["manual", "other"]
# drop_first: "automatic"

TYPES = [
    "bus", "convertible", "coupe", "hatchback", "mini-van", "offroad",
    "other", "pickup", "sedan", "truck", "unknown", "van", "wagon"
]
# drop_first: "SUV"

CONDITIONS = ["fair", "good", "like new", "new", "salvage", "unknown"]
# drop_first: "excellent"

TITLE_STATUSES = ["lien", "missing", "parts only", "rebuilt", "salvage"]
# drop_first: "clean"

DRIVES = ["fwd", "rwd", "unknown"]
# drop_first: "4wd"

PAINT_COLORS = [
    "blue", "brown", "custom", "green", "grey", "orange",
    "purple", "red", "silver", "unknown", "white", "yellow"
]
# drop_first: "black"


def preprocess(vehicle: VehicleInput) -> tuple[np.ndarray, list[str]]:
    """
    Transforma los datos de entrada del usuario al formato esperado por el modelo.
    
    Pipeline:
    1. Variables numéricas: MinMax → StandardScaler
    2. model: Target Encoding → StandardScaler
    3. Categóricas: One-Hot Encoding (sin escalar)
    
    Args:
        vehicle: Datos del vehículo validados por Pydantic
        
    Returns:
        Tupla de (vector de features como numpy array, lista de advertencias)
    """
    warnings: list[str] = []

    # Parámetros MinMax (del notebook 02, filtros aplicados al dataset)
    YEAR_MIN = 1981
    YEAR_MAX = 2024
    ODOMETER_MIN = 1
    ODOMETER_MAX = 299999

    # Construir DataFrame con una fila (replica la estructura del entrenamiento)
    features: dict[str, float] = {}

    # --- Variables numéricas: MinMax → StandardScaler ---

    # Year: MinMax primero
    year_minmax = (vehicle.year - YEAR_MIN) / (YEAR_MAX - YEAR_MIN)
    # Luego StandardScaler
    year_mean = artifacts.scaler_mean.get("year", 0.7620)
    year_scale = artifacts.scaler_scale.get("year", 0.1498)
    features["year"] = (year_minmax - year_mean) / year_scale

    # Odometer: MinMax primero
    odometer_minmax = (vehicle.odometer - ODOMETER_MIN) / (ODOMETER_MAX - ODOMETER_MIN)
    # Luego StandardScaler
    odo_mean = artifacts.scaler_mean.get("odometer", 0.3079)
    odo_scale = artifacts.scaler_scale.get("odometer", 0.2041)
    features["odometer"] = (odometer_minmax - odo_mean) / odo_scale

    # Cylinders: extraer número, luego StandardScaler
    cylinders_val = _parse_cylinders(vehicle.cylinders)
    cyl_mean = artifacts.scaler_mean.get("cylinders", 3.4977)
    cyl_scale = artifacts.scaler_scale.get("cylinders", 3.1596)
    features["cylinders"] = (cylinders_val - cyl_mean) / cyl_scale

    # Lat/Long: usar valores por defecto, luego StandardScaler
    lat_raw = 38.0  # Promedio aproximado
    long_raw = -96.0  # Promedio aproximado
    lat_mean = artifacts.scaler_mean.get("lat", 38.1690)
    lat_scale = artifacts.scaler_scale.get("lat", 6.9018)
    long_mean = artifacts.scaler_mean.get("long", -93.2896)
    long_scale = artifacts.scaler_scale.get("long", 20.1160)
    features["lat"] = (lat_raw - lat_mean) / lat_scale
    features["long"] = (long_raw - long_mean) / long_scale

    # --- Target Encoding para 'model' → StandardScaler ---
    model_name = vehicle.model.lower().strip()
    if model_name in artifacts.encoding_map:
        model_encoded_raw = artifacts.encoding_map[model_name]
    else:
        model_encoded_raw = artifacts.encoding_map_mean
        warnings.append(
            f"El modelo '{vehicle.model}' no fue reconocido en los datos de entrenamiento. "
            f"Se usó el valor promedio. La predicción puede ser menos precisa."
        )

    # StandardScaler al model_encoded
    me_mean = artifacts.scaler_mean.get("model_encoded", 0.1864)
    me_scale = artifacts.scaler_scale.get("model_encoded", 0.1144)
    features["model_encoded"] = (model_encoded_raw - me_mean) / me_scale

    # --- One-Hot Encoding: manufacturer ---
    manufacturer = vehicle.manufacturer.lower().strip()
    manufacturer_found = False
    for m in MANUFACTURERS:
        col_name = f"manufacturer_{m}"
        if manufacturer == m:
            features[col_name] = 1.0
            manufacturer_found = True
        else:
            features[col_name] = 0.0

    if not manufacturer_found and manufacturer != "acura":
        warnings.append(
            f"La marca '{vehicle.manufacturer}' no fue reconocida. "
            f"Se asignaron ceros a todas las columnas de fabricante."
        )

    # --- One-Hot Encoding: fuel ---
    fuel = vehicle.fuel.lower().strip()
    for f in FUELS:
        features[f"fuel_{f}"] = 1.0 if fuel == f else 0.0

    # --- One-Hot Encoding: transmission ---
    transmission = vehicle.transmission.lower().strip()
    for t in TRANSMISSIONS:
        features[f"transmission_{t}"] = 1.0 if transmission == t else 0.0

    # --- One-Hot Encoding: type ---
    vtype = vehicle.type.lower().strip()
    for tp in TYPES:
        features[f"type_{tp}"] = 1.0 if vtype == tp else 0.0

    # --- One-Hot Encoding: condition ---
    condition = vehicle.condition.lower().strip()
    for c in CONDITIONS:
        features[f"condition_{c}"] = 1.0 if condition == c else 0.0

    # --- One-Hot Encoding: title_status ---
    title_status = vehicle.title_status.lower().strip()
    for ts in TITLE_STATUSES:
        features[f"title_status_{ts}"] = 1.0 if title_status == ts else 0.0

    # --- One-Hot Encoding: drive ---
    drive = vehicle.drive.lower().strip()
    for d in DRIVES:
        features[f"drive_{d}"] = 1.0 if drive == d else 0.0

    # --- One-Hot Encoding: paint_color ---
    paint_color = vehicle.paint_color.lower().strip()
    for pc in PAINT_COLORS:
        features[f"paint_color_{pc}"] = 1.0 if paint_color == pc else 0.0

    # --- Construir vector en el orden exacto del modelo ---
    if artifacts.feature_columns:
        # Usar el orden de features del modelo entrenado
        vector = []
        for col in artifacts.feature_columns:
            vector.append(features.get(col, 0.0))
        return np.array([vector]), warnings
    else:
        # Fallback: usar el orden del dataset de entrenamiento
        ordered_features = _get_ordered_features(features)
        return np.array([ordered_features]), warnings


def _parse_cylinders(cylinders_str: Optional[str]) -> float:
    """Extrae el número de cilindros del texto (ej: '4 cylinders' → 4.0)."""
    if not cylinders_str:
        return 0.0
    import re
    match = re.search(r"(\d+)", cylinders_str)
    return float(match.group(1)) if match else 0.0


def _get_ordered_features(features: dict[str, float]) -> list[float]:
    """
    Ordena las features según el orden del dataset de entrenamiento.
    Este es el orden de columnas en vehicles_processed_nums.csv (sin 'price').
    """
    # Orden exacto extraído del header del CSV de entrenamiento
    column_order = [
        "year", "cylinders", "odometer", "lat", "long",
        # manufacturer (40 columnas)
        *[f"manufacturer_{m}" for m in MANUFACTURERS],
        # fuel (4 columnas)
        *[f"fuel_{f}" for f in FUELS],
        # transmission (2 columnas)
        *[f"transmission_{t}" for t in TRANSMISSIONS],
        # type (13 columnas)
        *[f"type_{tp}" for tp in TYPES],
        # condition (6 columnas)
        *[f"condition_{c}" for c in CONDITIONS],
        # model_encoded (1 columna)
        "model_encoded",
        # title_status (5 columnas)
        *[f"title_status_{ts}" for ts in TITLE_STATUSES],
        # drive (3 columnas)
        *[f"drive_{d}" for d in DRIVES],
        # paint_color (12 columnas)
        *[f"paint_color_{pc}" for pc in PAINT_COLORS],
    ]

    return [features.get(col, 0.0) for col in column_order]
