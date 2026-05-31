"""
Carga del modelo Random Forest y artefactos asociados.

ESTRATEGIA PARA MODELO GRANDE (~1.5 GB):
- Carga diferida (lazy loading) al inicio del servidor
- El modelo se carga UNA sola vez y se mantiene en memoria
- Si la carga falla, el servidor arranca pero marca el modelo como no disponible
- El endpoint /health reporta el estado de carga del modelo
"""

import json
import logging
import time
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class ModelArtifacts:
    """
    Contenedor para el modelo y artefactos necesarios para inferencia.
    Implementa carga diferida con manejo robusto de errores.
    """

    def __init__(self):
        self.model = None
        self.encoding_map: dict[str, float] = {}
        self.encoding_map_mean: float = 0.0
        self.scaler_mean: dict[str, float] = {}
        self.scaler_scale: dict[str, float] = {}
        self.scaler_columns: list[str] = []
        self.is_loaded: bool = False
        self.load_error: Optional[str] = None
        self.feature_columns: list[str] = []

    def load(self, model_path: str, encoding_map_path: str) -> None:
        """
        Carga el modelo y el encoding map desde disco.
        
        Args:
            model_path: Ruta al archivo .pkl del modelo
            encoding_map_path: Ruta al CSV del encoding map
        """
        try:
            # Cargar encoding map primero (es pequeño y rápido)
            self._load_encoding_map(encoding_map_path)

            # Cargar parámetros del scaler
            self._load_scaler_params()

            # Cargar modelo (operación pesada ~1.5 GB)
            self._load_model(model_path)

            self.is_loaded = True
            self.load_error = None
            logger.info("✅ Modelo y artefactos cargados exitosamente")

        except Exception as e:
            self.is_loaded = False
            self.load_error = str(e)
            logger.error(f"❌ Error cargando modelo: {e}")

    def _load_model(self, model_path: str) -> None:
        """Carga el modelo .pkl con joblib."""
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Modelo no encontrado en: {model_path}. "
                f"Verifica la variable de entorno MODEL_PATH."
            )

        file_size_mb = path.stat().st_size / (1024 * 1024)
        logger.info(
            f"Cargando modelo ({file_size_mb:.0f} MB). "
            f"Esto puede tomar 10-30 segundos..."
        )

        start = time.time()
        self.model = joblib.load(model_path)
        elapsed = time.time() - start

        # Extraer nombres de features del modelo
        if hasattr(self.model, 'feature_names_in_'):
            self.feature_columns = list(self.model.feature_names_in_)
        else:
            logger.warning(
                "El modelo no tiene feature_names_in_. "
                "Se usará el orden de columnas del dataset de entrenamiento."
            )

        logger.info(f"Modelo cargado en {elapsed:.1f}s. Features: {len(self.feature_columns)}")

    def _load_encoding_map(self, encoding_map_path: str) -> None:
        """Carga el CSV de target encoding para la columna 'model'."""
        path = Path(encoding_map_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Encoding map no encontrado en: {encoding_map_path}. "
                f"Verifica la variable de entorno ENCODING_MAP_PATH."
            )

        df = pd.read_csv(encoding_map_path)
        self.encoding_map = dict(zip(df["model"], df["price"]))
        self.encoding_map_mean = float(np.mean(list(self.encoding_map.values())))

        logger.info(
            f"Encoding map cargado: {len(self.encoding_map)} modelos. "
            f"Promedio global: {self.encoding_map_mean:.4f}"
        )

    def _load_scaler_params(self) -> None:
        """Carga los parámetros del StandardScaler desde el JSON de artefactos."""
        artifacts_dir = Path(__file__).resolve().parent.parent / "artifacts"
        scaler_path = artifacts_dir / "scaler_params.json"

        if not scaler_path.exists():
            logger.warning(
                f"⚠️ Parámetros del scaler no encontrados en: {scaler_path}. "
                f"Las predicciones pueden ser menos precisas."
            )
            return

        with open(scaler_path, "r", encoding="utf-8") as f:
            params = json.load(f)

        self.scaler_columns = params["columns"]
        self.scaler_mean = params["mean"]
        self.scaler_scale = params["scale"]

        logger.info(
            f"Parámetros del scaler cargados: {len(self.scaler_columns)} columnas"
        )


# Instancia global (singleton)
artifacts = ModelArtifacts()
