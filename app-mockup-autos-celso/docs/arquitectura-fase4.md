# Arquitectura Técnica — Fase 4: Seguridad y Buenas Prácticas

## Descripción General

Esta fase eleva el nivel técnico del proyecto sin agregar nuevas funcionalidades de negocio. Se enfoca en robustez, trazabilidad, mantenibilidad y preparación para despliegue.

## Cambios Implementados

### Backend

#### 1. Carga de Variables de Entorno con `python-dotenv`
`settings.py` ahora carga automáticamente el archivo `.env` al iniciar, usando `load_dotenv()`. En producción, las variables se inyectan directamente en el entorno del contenedor sin necesidad del archivo.

#### 2. `LOG_LEVEL` Configurable
Se agrega la variable `LOG_LEVEL` (DEBUG|INFO|WARNING|ERROR|CRITICAL). En desarrollo se recomienda `DEBUG`. En producción, `WARNING` o `ERROR` para reducir ruido.

#### 3. Middleware de Request Logging
Cada request HTTP es registrado con:
- ID único de request (8 caracteres)
- Método y ruta
- Código de respuesta
- Tiempo de respuesta en ms

Ejemplo de log:
```
→ [a3f1bc20] POST /api/v1/predict
← [a3f1bc20] 200 (342.5ms)
```

#### 4. Manejador Global de Excepciones
Se agrega un handler para `Exception` que captura errores no controlados y retorna un 500 genérico sin exponer detalles internos. Evita caídas totales del servidor.

#### 5. Sanitización de Inputs con `field_validator`
`VehicleInput` ahora incluye validadores que:
- Normalizan strings: strip + lowercase antes de procesar
- Validan enum values: fuel, transmission, condition, title_status, drive
- Usan fallback seguro para campos opcionales (condition → "unknown", drive → "unknown")
- Rechazan strings vacíos o solo espacios

#### 6. Handler 422 Robusto
El manejador de errores de validación ahora usa `RequestValidationError` explícitamente (en lugar de manejo genérico), garantizando formato consistente.

#### 7. Limpieza de Imports
Se eliminó `import pandas as pd` no utilizado en `preprocessor.py`. Se movió `import re` al top del archivo.

### Frontend

#### 8. Constantes Centralizadas
Se crea `src/constants/translations.js` con:
- `TRANSLATIONS`: diccionario inglés → español para la UI
- `AVAILABLE_YEARS`: años válidos (estático, calculado una vez)
- `FORM_DEFAULTS`: valores iniciales del formulario
- `LOADING_MESSAGES`: mensajes rotativos de carga

Antes estas constantes estaban duplicadas dentro de los componentes.

#### 9. Hook `useVehicleForm`
Se extrae la lógica del formulario a `src/hooks/useVehicleForm.js`:
- Estado del formulario y campos custom
- Cálculo de modelos disponibles por marca
- Warnings automáticos por marca/modelo "Otro"
- Validación con mensajes por campo
- Construcción del payload para el backend

`PredictionForm.jsx` ahora solo se encarga de la UI, delegando toda la lógica al hook.

#### 10. `.gitignore` Actualizado
Se agrega:
- `backend/.env` y `backend/venv/` (entorno virtual)
- `**/__pycache__/` y `*.pyc` (archivos compilados Python)
- `.env` (variables de entorno del frontend)

## Estructura Final

```
app-mockup-autos-celso/
├── .env                        ← Variables de entorno (NO commitear)
├── .env.production             ← Variables para producción
├── .gitignore                  ← Actualizado
├── src/
│   ├── App.jsx                 ← Orquestador
│   ├── components/
│   │   ├── PredictionForm.jsx  ← UI del formulario (usa hook)
│   │   ├── ResultPanel.jsx     ← Panel de resultados
│   │   └── SearchableSelect.jsx← Select con búsqueda
│   ├── hooks/
│   │   └── useVehicleForm.js   ← Lógica del formulario (NUEVO)
│   ├── constants/
│   │   └── translations.js     ← Constantes centralizadas (NUEVO)
│   └── services/
│       └── predictionService.js← Capa HTTP (Axios)
├── backend/
│   ├── .env.example            ← Plantilla de variables (ACTUALIZADO)
│   ├── app/
│   │   ├── main.py             ← Logging, CORS, handlers (ACTUALIZADO)
│   │   ├── config/
│   │   │   └── settings.py     ← Carga dotenv, LOG_LEVEL (ACTUALIZADO)
│   │   ├── schemas/
│   │   │   └── vehicle.py      ← Sanitización field_validators (ACTUALIZADO)
│   │   └── services/
│   │       └── preprocessor.py ← Imports limpios (ACTUALIZADO)
│   └── docs/
│       └── arquitectura-backend.md
└── docs/
    ├── frontend-integracion.md
    └── arquitectura-fase4.md   ← Este documento
```

## Variables de Entorno — Referencia Completa

### Backend (`backend/.env`)
| Variable | Default | Descripción |
|----------|---------|-------------|
| `MODEL_PATH` | `../../models/random_forest/model.pkl` | Ruta al modelo |
| `ENCODING_MAP_PATH` | `../../data/processed/model_encoding_map.csv` | Ruta al encoding map |
| `HOST` | `0.0.0.0` | Host del servidor |
| `PORT` | `8000` | Puerto del servidor |
| `ALLOWED_ORIGINS` | `http://localhost:5173,...` | Orígenes CORS |
| `EXCHANGE_RATE_USD_CLP` | `950` | Tasa de cambio |
| `LOG_LEVEL` | `INFO` | Nivel de logging |

### Frontend (`.env`)
| Variable | Default | Descripción |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000` | URL del backend |

## Consideraciones de Seguridad

- Los archivos `.env` están en `.gitignore` y NUNCA deben ser commiteados
- El handler global de errores evita exponer stack traces al cliente
- Los inputs del usuario son sanitizados antes de procesamiento
- CORS está configurado explícitamente (no `allow_origins=["*"]`)
- El logging no registra datos sensibles de los vehículos

## Preparación para Despliegue

- Sin rutas absolutas en el código
- Variables de entorno para toda configuración variable
- `Dockerfile` existente en `backend/`
- Frontend compatible con Vercel (`npm run build`)
- Backend compatible con cualquier plataforma que soporte contenedores Python
