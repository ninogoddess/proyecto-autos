# 03_ajustes_backend.md
### Proyecto de Regresión de Precios de Vehículos

**Autor:** Celso Farías  
**Fecha:** 31 de mayo

---

# Ajustes al Backend para Inferencia en Producción

Cuando un modelo se entrena, vive en un mundo controlado.
Cuando se despliega, debe enfrentarse a la realidad.

Y la realidad, como siempre, no perdona las omisiones del pasado.

Este documento registra los ajustes técnicos realizados al backend de predicción durante la fase de integración del sistema web. Cada ajuste responde a un problema concreto detectado al intentar conectar el modelo entrenado con el mundo exterior.

---

## 1. Recuperación de Parámetros del StandardScaler

### Problema

Durante el entrenamiento, el script `encode_dataset.py` aplicó un `StandardScaler` a las variables numéricas continuas del dataset. Este scaler transforma los datos centrándolos en media 0 y desviación estándar 1.

Sin embargo, los parámetros del scaler (`mean_` y `scale_` por columna) **no fueron serializados** junto al modelo. Solo se guardó:

* `model.pkl` — el Random Forest entrenado
* `model_encoding_map.csv` — el mapeo de Target Encoding

Sin estos parámetros, el backend no puede replicar la transformación aplicada durante el entrenamiento, y las predicciones serían incorrectas.

### Solución

Se creó un script de recuperación (`extract_scaler_params.py`) que replica **exactamente** el mismo pipeline del entrenamiento sobre el dataset original:

1. Elimina `state`
2. Aplica Target Encoding a `model`
3. Extrae número de `cylinders`
4. Aplica One-Hot Encoding con `drop_first=True`
5. Rellena NaN con 0
6. Aplica `StandardScaler` a las columnas numéricas no binarias
7. Extrae y guarda `mean_` y `scale_` como JSON

### Resultado

Archivo generado: `backend/app/artifacts/scaler_params.json`

```json
{
  "columns": ["price", "year", "cylinders", "odometer", "lat", "long", "model_encoded"],
  "mean": {
    "price": 0.1864,
    "year": 0.7620,
    "cylinders": 3.4977,
    "odometer": 0.3079,
    "lat": 38.1690,
    "long": -93.2896,
    "model_encoded": 0.1864
  },
  "scale": {
    "price": 0.1422,
    "year": 0.1498,
    "cylinders": 3.1596,
    "odometer": 0.2041,
    "lat": 6.9018,
    "long": 20.1160,
    "model_encoded": 0.1144
  }
}
```

### Justificación matemática

La recuperación es **idéntica** a haber guardado el scaler durante el entrenamiento, dado que:

* Se usa el mismo dataset de entrada
* Se aplican las mismas transformaciones en el mismo orden
* `StandardScaler.fit()` es determinista para un mismo dataset

No hay aproximación. Los parámetros son exactos.

### Lección

> Guardar el modelo no es suficiente.
> Hay que guardar todo lo que el modelo necesita para hablar con el mundo.

---

## 2. Extracción de Modelos por Marca

### Problema

El `model_encoding_map.csv` contiene más de 20,000 entradas de modelos de vehículos. Estos modelos provienen directamente del campo de texto libre del dataset de Craigslist, lo que significa que incluyen:

* Textos de anuncios: `"$362.47, $1000 down, oac, 2.9%apr"`
* Emojis y caracteres especiales: `"* vmi * ♿"`
* Duplicados con variaciones: `"f-150"`, `"f150"`, `"f150 4x4"`, `"f-150 xlt 4wd"`
* Modelos sin marca asociada
* Basura pura: `".. ect."`, `"-"`, `"/ accord"`

Servir esta lista completa al frontend generaba un menú inutilizable con miles de opciones mezcladas entre todas las marcas.

### Solución

Se creó un script (`extract_models_by_manufacturer.py`) que:

1. Carga el dataset `vehicles_processed.csv`
2. Reconstruye la marca de cada registro desde las columnas one-hot
3. Agrupa los modelos por marca
4. Aplica filtros de limpieza:
   * Longitud entre 2 y 40 caracteres
   * Sin emojis ni caracteres fuera de ASCII
   * Sin signos de dólar ni textos de financiamiento
   * Sin caracteres especiales al inicio
   * Debe contener al menos una letra
   * Sin múltiples comas (indicador de anuncio)
5. Elimina duplicados por marca
6. Guarda el resultado como JSON

### Resultado

Archivo generado: `backend/app/artifacts/models_by_manufacturer.json`

| Métrica | Valor |
|---------|-------|
| Marcas con modelos | 41 |
| Modelos válidos totales | 19,845 |
| Modelos filtrados (basura) | 955 |
| Tamaño del archivo | 490 KB |

Ejemplo de estructura:

```json
{
  "toyota": ["4runner", "avalon", "camry", "celica", "corolla", "highlander", ...],
  "ford": ["bronco", "edge", "escape", "expedition", "explorer", "f-150", ...],
  "chevrolet": ["blazer", "camaro", "colorado", "corvette", "cruze", ...]
}
```

### Impacto en el frontend

Ahora, al seleccionar una marca en el formulario:

* Solo se muestran los modelos de **esa** marca
* No hay mezcla entre marcas (no más "chevrolet / mustang")
* Los modelos basura fueron eliminados
* Se incluye opción "Otro" para modelos no listados

### Nota sobre duplicados

Aún existen variaciones del mismo modelo (ej: `"f-150"`, `"f-150 xlt"`, `"f-150 lariat"`). Esto es intencional: cada variación tiene un valor de Target Encoding diferente en el modelo entrenado, por lo que representan predicciones distintas. Eliminarlos perdería información predictiva.

Se implementó una barra de búsqueda en el frontend para que el usuario pueda encontrar rápidamente su modelo entre las opciones disponibles.

---

## 3. Pipeline Completo de Inferencia

### Descubrimiento

El análisis reveló que el pipeline de preprocesamiento tiene **dos etapas de normalización**, no una:

1. **Notebook 02** (`02_preprocesamiento`): Aplica `MinMaxScaler` a `[price, year, odometer]` → rango [0, 1]
2. **Script** (`encode_dataset.py`): Aplica `StandardScaler` a todas las columnas numéricas no binarias (incluyendo las ya normalizadas por MinMax)

Esto significa que para inferencia, el backend debe:

1. Aplicar MinMax a `year` y `odometer` (con los rangos del filtrado original)
2. Luego aplicar StandardScaler (con los parámetros recuperados)
3. Para desnormalizar el precio predicho: invertir StandardScaler, luego invertir MinMax

### Parámetros de MinMax (del filtrado original)

| Variable | Mínimo | Máximo |
|----------|--------|--------|
| price | 1,000 USD | 100,000 USD |
| year | 1981 | 2024 |
| odometer | 1 | 299,999 |

### Fórmula de desnormalización del precio

```
precio_minmax = predicción_raw × scale_price + mean_price
precio_usd = precio_minmax × (100000 - 1000) + 1000
precio_clp = precio_usd × tasa_cambio
```

---

## 4. Reflexión

Cada uno de estos ajustes nació de una omisión durante el entrenamiento.
No por negligencia, sino por la naturaleza iterativa del proceso.

Cuando se entrena un modelo, el foco está en las métricas.
Cuando se despliega, el foco cambia: ahora importa todo lo que rodea al modelo.

> El modelo es el corazón.
> Pero sin arterias, sin venas, sin el sistema que lo conecta al mundo...
> el corazón late en el vacío.

Estos ajustes son las arterias.

---
