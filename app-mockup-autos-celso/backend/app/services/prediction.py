"""
Servicio de predicción de precios.
Orquesta el preprocesamiento, la inferencia y la desnormalización.

PIPELINE DE NORMALIZACIÓN (descubierto del análisis):
1. El notebook 02 aplicó MinMaxScaler a [price, odometer, year] → rango [0,1]
2. El script encode_dataset.py aplicó StandardScaler a las columnas numéricas no binarias
3. El modelo fue entrenado con datos en escala StandardScaler

Para inferencia:
- Primero aplicamos MinMax a year y odometer (rangos conocidos del filtrado)
- Luego aplicamos StandardScaler con los parámetros recuperados
- La predicción sale en escala StandardScaler del price
- Desnormalizamos: pred * scale_price + mean_price → valor MinMax [0,1]
- Luego invertimos MinMax: valor * (max - min) + min → USD
"""

import logging
import numpy as np

from ..config.settings import EXCHANGE_RATE_USD_CLP
from ..schemas.vehicle import VehicleInput, PredictionResponse
from ..utils.model_loader import artifacts
from .preprocessor import preprocess

logger = logging.getLogger(__name__)

# Parámetros del MinMaxScaler original (del notebook 02)
# Filtros aplicados: price > 1000 & price < 100000
PRICE_MIN_USD = 1000
PRICE_MAX_USD = 100000
# year > 1980 & year <= 2024
YEAR_MIN = 1981
YEAR_MAX = 2024
# odometer > 0 & odometer < 300000
ODOMETER_MIN = 1
ODOMETER_MAX = 299999


def predict_price(vehicle: VehicleInput) -> PredictionResponse:
    """
    Ejecuta la predicción completa: preprocesamiento → inferencia → desnormalización.
    
    Args:
        vehicle: Datos del vehículo validados
        
    Returns:
        PredictionResponse con precio estimado y advertencias
        
    Raises:
        RuntimeError: Si el modelo no está cargado o la inferencia falla
    """
    if not artifacts.is_loaded or artifacts.model is None:
        raise RuntimeError(
            "El modelo de predicción no está disponible. "
            "Verifica que el archivo del modelo existe y es accesible."
        )

    # 1. Preprocesamiento (construye vector con MinMax + StandardScaler)
    feature_vector, warnings = preprocess(vehicle)
    logger.debug(f"Vector de features: shape={feature_vector.shape}")

    # 2. Inferencia
    try:
        raw_prediction = artifacts.model.predict(feature_vector)[0]
    except Exception as e:
        logger.error(f"Error en inferencia del modelo: {e}")
        raise RuntimeError(
            "La predicción no pudo completarse. Error interno del modelo."
        )

    # 3. Desnormalizar el precio predicho
    # El modelo predice en escala StandardScaler
    # Paso 1: Invertir StandardScaler → obtener valor MinMax [0,1]
    price_mean = artifacts.scaler_mean.get("price", 0.1864)
    price_scale = artifacts.scaler_scale.get("price", 0.1422)
    price_minmax = raw_prediction * price_scale + price_mean

    # Paso 2: Invertir MinMax → obtener precio en USD
    predicted_price_usd = price_minmax * (PRICE_MAX_USD - PRICE_MIN_USD) + PRICE_MIN_USD

    # Validar que el precio sea razonable
    if predicted_price_usd < 0:
        predicted_price_usd = float(PRICE_MIN_USD)
        warnings.append(
            "El precio predicho fue negativo y se ajustó al mínimo. "
            "La predicción puede no ser confiable para esta combinación de datos."
        )
    elif predicted_price_usd > PRICE_MAX_USD * 1.5:
        warnings.append(
            "El precio predicho es inusualmente alto. "
            "La predicción puede no ser confiable para esta combinación de datos."
        )

    # 4. Conversión a CLP
    predicted_price_clp = int(predicted_price_usd * EXCHANGE_RATE_USD_CLP)

    # 5. Construir respuesta
    vehicle_data = {
        "manufacturer": vehicle.manufacturer,
        "model": vehicle.model,
        "year": vehicle.year,
        "odometer": vehicle.odometer,
        "fuel": vehicle.fuel,
        "transmission": vehicle.transmission,
        "type": vehicle.type,
        "condition": vehicle.condition,
    }

    return PredictionResponse(
        predicted_price_usd=round(predicted_price_usd, 2),
        predicted_price_clp=predicted_price_clp,
        vehicle_data=vehicle_data,
        warnings=warnings,
    )
