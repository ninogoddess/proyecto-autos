"""
Extrae modelos LIMPIOS agrupados por marca desde el dataset de entrenamiento.

Filtra modelos basura (anuncios, emojis, caracteres especiales, textos largos)
y genera un JSON con modelos legítimos por marca.

EJECUCIÓN:
    cd proyecto-autos/app-mockup-autos-celso/backend
    python scripts/extract_models_by_manufacturer.py
"""

import json
import re
import os
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent.parent

INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "vehicles_processed.csv"
OUTPUT_PATH = BACKEND_DIR / "app" / "artifacts" / "models_by_manufacturer.json"


def is_valid_model(model_name: str) -> bool:
    """
    Filtra modelos basura. Un modelo válido:
    - Tiene entre 2 y 40 caracteres
    - No contiene emojis ni caracteres especiales raros
    - No contiene signos de dólar ($) ni precios
    - No contiene URLs ni emails
    - No empieza con caracteres especiales
    - Contiene al menos una letra
    """
    if not model_name or not isinstance(model_name, str):
        return False

    model = model_name.strip()

    # Longitud razonable
    if len(model) < 2 or len(model) > 40:
        return False

    # No contiene $, precios, o textos de anuncios
    if '$' in model or '%' in model or '♿' in model:
        return False

    # No contiene emojis (caracteres fuera de ASCII extendido básico)
    if any(ord(c) > 127 for c in model):
        return False

    # No empieza con caracteres especiales
    if model[0] in '/-*&.!@#()[]{}':
        return False

    # Debe contener al menos una letra
    if not re.search(r'[a-zA-Z]', model):
        return False

    # No contiene "down", "month", "oac", "apr" (textos de financiamiento)
    financing_keywords = ['down', 'month', 'oac', 'apr', 'miles!', 'only $', 'luxury']
    if any(kw in model.lower() for kw in financing_keywords):
        return False

    # No contiene comas seguidas de espacios y más texto largo (anuncios)
    if model.count(',') > 1:
        return False

    return True


def main():
    print("=" * 60)
    print("EXTRACCIÓN DE MODELOS POR MARCA")
    print("=" * 60)

    print(f"\nCargando dataset: {INPUT_PATH}")
    
    # Cargar solo las columnas necesarias
    df = pd.read_csv(INPUT_PATH)
    print(f"Shape: {df.shape}")

    # Reconstruir 'manufacturer' desde columnas one-hot
    mfr_cols = [c for c in df.columns if c.startswith('manufacturer_')]
    print(f"Columnas one-hot de manufacturer: {len(mfr_cols)}")

    # La categoría base (drop_first=True) es la primera alfabéticamente: "acura"
    # Si todas las columnas manufacturer_* son False/0, la marca es "acura"
    def get_manufacturer(row):
        for col in mfr_cols:
            if row[col] == True or row[col] == 1:
                return col.replace('manufacturer_', '')
        return 'acura'  # categoría base

    print("Reconstruyendo marca desde one-hot (esto puede tomar unos segundos)...")
    df['manufacturer'] = df[mfr_cols].apply(
        lambda row: next(
            (col.replace('manufacturer_', '') for col in mfr_cols if row[col]),
            'acura'
        ), axis=1
    )

    print(f"Marcas únicas: {df['manufacturer'].nunique()}")
    print(f"Modelos únicos (sin filtrar): {df['model'].nunique()}")

    # Agrupar modelos por marca y filtrar
    models_by_manufacturer = {}
    total_valid = 0
    total_filtered = 0

    for manufacturer in sorted(df['manufacturer'].unique()):
        mfr_models = df[df['manufacturer'] == manufacturer]['model'].unique()
        valid_models = sorted(set(
            m.strip().lower() for m in mfr_models
            if is_valid_model(str(m))
        ))
        
        filtered_count = len(mfr_models) - len(valid_models)
        total_valid += len(valid_models)
        total_filtered += filtered_count

        if valid_models:
            models_by_manufacturer[manufacturer] = valid_models
            print(f"  {manufacturer}: {len(valid_models)} modelos válidos ({filtered_count} filtrados)")

    print(f"\n--- Resumen ---")
    print(f"Marcas con modelos: {len(models_by_manufacturer)}")
    print(f"Modelos válidos totales: {total_valid}")
    print(f"Modelos filtrados (basura): {total_filtered}")

    # Guardar
    os.makedirs(OUTPUT_PATH.parent, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(models_by_manufacturer, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Guardado en: {OUTPUT_PATH}")
    print(f"   Tamaño: {OUTPUT_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
