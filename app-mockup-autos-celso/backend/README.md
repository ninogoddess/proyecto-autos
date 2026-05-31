# Backend API — Predicción de Precios de Vehículos

API REST construida con FastAPI para predicción de precios de vehículos usados mediante un modelo Random Forest.

## Requisitos Previos

- Python 3.11+
- pip
- Modelo Random Forest entrenado (`models/random_forest/model.pkl`)
- Encoding map (`data/processed/model_encoding_map.csv`)

## Instalación

```bash
# Desde la carpeta backend/
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Copiar el archivo de ejemplo y ajustar:

```bash
copy .env.example .env
```

Variables de entorno disponibles:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `MODEL_PATH` | Ruta al archivo .pkl del modelo | `../../models/random_forest/model.pkl` |
| `ENCODING_MAP_PATH` | Ruta al CSV de encoding map | `../../data/processed/model_encoding_map.csv` |
| `PORT` | Puerto del servidor | `8000` |
| `HOST` | Host del servidor | `0.0.0.0` |
| `ALLOWED_ORIGINS` | Orígenes CORS (separados por coma) | `http://localhost:5173,...` |
| `EXCHANGE_RATE_USD_CLP` | Tasa de cambio USD → CLP | `950` |

## Ejecución Local

```bash
# Desde la carpeta backend/
uvicorn app.main:app --reload --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

**Nota:** La primera carga toma 10-30 segundos por el tamaño del modelo (~1.5 GB).

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Información básica de la API |
| GET | `/api/v1/health` | Estado del servicio y modelo |
| GET | `/api/v1/options` | Opciones válidas para el formulario |
| POST | `/api/v1/predict` | Predicción de precio |
| GET | `/docs` | Documentación Swagger interactiva |
| GET | `/redoc` | Documentación ReDoc |

### POST /api/v1/predict

**Request Body:**
```json
{
  "manufacturer": "toyota",
  "model": "camry",
  "year": 2018,
  "odometer": 45000,
  "fuel": "gas",
  "transmission": "automatic",
  "type": "sedan",
  "condition": "good",
  "cylinders": "4 cylinders",
  "title_status": "clean",
  "drive": "fwd",
  "paint_color": "white"
}
```

**Response (200):**
```json
{
  "predicted_price_usd": 18500.00,
  "predicted_price_clp": 17575000,
  "vehicle_data": {
    "manufacturer": "toyota",
    "model": "camry",
    "year": 2018,
    "odometer": 45000,
    "fuel": "gas",
    "transmission": "automatic",
    "type": "sedan",
    "condition": "good"
  },
  "warnings": []
}
```

**Response (422 - Datos inválidos):**
```json
{
  "detail": [
    {
      "field": "body → year",
      "message": "Input should be greater than or equal to 1981"
    }
  ]
}
```

### GET /api/v1/health

```json
{
  "status": "ok",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### GET /api/v1/options

```json
{
  "manufacturers": ["acura", "alfa-romeo", "aston-martin", ...],
  "models": ["1 series", "1 series 128i", ...],
  "fuels": ["diesel", "electric", "gas", "hybrid", "other"],
  "transmissions": ["automatic", "manual", "other"],
  "types": ["SUV", "bus", "convertible", ...],
  "conditions": ["excellent", "fair", "good", ...],
  "title_statuses": ["clean", "lien", "missing", ...],
  "drives": ["4wd", "fwd", "rwd", "unknown"],
  "paint_colors": ["black", "blue", "brown", ...]
}
```

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada FastAPI
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py      # Configuración centralizada
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py        # GET /api/v1/health
│   │   ├── options.py       # GET /api/v1/options
│   │   └── predict.py       # POST /api/v1/predict
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── vehicle.py       # Modelos Pydantic
│   ├── services/
│   │   ├── __init__.py
│   │   ├── options.py       # Lógica de opciones
│   │   ├── prediction.py    # Lógica de predicción
│   │   └── preprocessor.py  # Pipeline de preprocesamiento
│   └── utils/
│       ├── __init__.py
│       └── model_loader.py  # Carga del modelo ML
├── .env.example
├── requirements.txt
└── README.md
```

## Troubleshooting

### El modelo no carga
- Verifica que `MODEL_PATH` apunta al archivo correcto
- Asegúrate de tener al menos 2 GB de RAM libre
- Revisa que la versión de scikit-learn sea compatible (1.5.x)

### Error "could not convert string to float"
- El modelo espera datos numéricos. El preprocesador se encarga de la conversión.
- Verifica que los campos categóricos tengan valores válidos.

### CORS bloqueado
- Agrega el origen del frontend a `ALLOWED_ORIGINS` en `.env`

### Predicciones imprecisas
- El modelo fue entrenado con datos de EE.UU. (Craigslist)
- Los precios se convierten a CLP con una tasa configurable
- Modelos o marcas no reconocidos usan valores promedio (ver advertencias)
