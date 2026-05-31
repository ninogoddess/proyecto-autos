"""
Script para extraer los parámetros del StandardScaler usado en el entrenamiento.

CONTEXTO:
El script original (src/encode_dataset.py) aplicó StandardScaler a las columnas
numéricas no binarias del dataset, pero NO guardó los parámetros del scaler.
Este script replica EXACTAMENTE el mismo pipeline para recuperar esos parámetros.

EJECUCIÓN:
    cd proyecto-autos/app-mockup-autos-celso/backend
    python scripts/extract_scaler_params.py

RESULTADO:
    Genera app/artifacts/scaler_params.json con mean y scale por columna.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Configuración de rutas (relativas al directorio del proyecto)
SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent.parent  # proyecto-autos/

INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "vehicles_processed.csv"
OUTPUT_PATH = BACKEND_DIR / "app" / "artifacts" / "scaler_params.json"


def main():
    print("=" * 60)
    print("EXTRACCIÓN DE PARÁMETROS DEL STANDARDSCALER")
    print("=" * 60)

    # =========================================================
    # CARGA DE DATOS
    # =========================================================
    print(f"\n1. Cargando dataset desde: {INPUT_PATH}")
    if not INPUT_PATH.exists():
        print(f"ERROR: No se encontró el archivo: {INPUT_PATH}")
        sys.exit(1)

    df = pd.read_csv(INPUT_PATH)
    print(f"   Shape inicial: {df.shape}")

    # =========================================================
    # REPLICAR PIPELINE DE encode_dataset.py
    # =========================================================

    # Eliminar 'state'
    print("\n2. Eliminando columna 'state'...")
    if "state" in df.columns:
        df = df.drop(columns=["state"])

    # Target Encoding para 'model'
    print("3. Aplicando target encoding a 'model'...")
    if "model" in df.columns:
        model_price_map = df.groupby("model")["price"].mean()
        df["model_encoded"] = df["model"].map(model_price_map)
        df = df.drop(columns=["model"])

    # Transformación de 'cylinders'
    print("4. Procesando 'cylinders'...")
    if "cylinders" in df.columns:
        df["cylinders"] = (
            df["cylinders"]
            .astype(str)
            .str.extract(r"(\d+)")
            .astype(float)
        )

    # One-Hot Encoding
    print("5. Aplicando One-Hot Encoding...")
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    print(f"   Columnas categóricas: {categorical_cols}")
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Rellenar NaN
    print("6. Rellenando NaN con 0...")
    df = df.fillna(0)

    print(f"   Shape después de transformaciones: {df.shape}")

    # =========================================================
    # APLICAR STANDARDSCALER (igual que encode_dataset.py)
    # =========================================================
    print("\n7. Aplicando StandardScaler...")

    # Detectar columnas numéricas no binarias (MISMO criterio que el original)
    numeric_cols = df.select_dtypes(include=["number"]).columns
    non_binary_cols = [
        col for col in numeric_cols
        if not set(df[col].unique()).issubset({0, 1})
    ]

    print(f"   Columnas escaladas ({len(non_binary_cols)}):")
    for col in non_binary_cols:
        print(f"     - {col}")

    scaler = StandardScaler()
    scaler.fit(df[non_binary_cols])

    # =========================================================
    # EXTRAER Y GUARDAR PARÁMETROS
    # =========================================================
    print("\n8. Extrayendo parámetros del scaler...")

    scaler_params = {
        "columns": non_binary_cols,
        "mean": {col: float(mean) for col, mean in zip(non_binary_cols, scaler.mean_)},
        "scale": {col: float(scale) for col, scale in zip(non_binary_cols, scaler.scale_)},
        "description": (
            "Parámetros del StandardScaler aplicado durante el preprocesamiento. "
            "Para escalar un valor: (valor - mean) / scale. "
            "Para desescalar: valor * scale + mean."
        ),
    }

    # Mostrar parámetros
    print("\n   Parámetros extraídos:")
    print(f"   {'Columna':<20} {'Media':<15} {'Desv. Std':<15}")
    print(f"   {'-'*50}")
    for col in non_binary_cols:
        print(f"   {col:<20} {scaler_params['mean'][col]:<15.4f} {scaler_params['scale'][col]:<15.4f}")

    # Guardar como JSON
    os.makedirs(OUTPUT_PATH.parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(scaler_params, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Parámetros guardados en: {OUTPUT_PATH}")
    print(f"   Archivo size: {OUTPUT_PATH.stat().st_size} bytes")
    print("\n" + "=" * 60)
    print("EXTRACCIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()
