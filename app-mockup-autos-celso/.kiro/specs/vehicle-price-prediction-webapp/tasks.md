# Implementation Plan: Vehicle Price Prediction Webapp

## Overview

Este plan convierte el diseño técnico en tareas de codificación incrementales. El frontend React existente (mockup) se reorganiza en componentes modulares y se conecta a un backend FastAPI nuevo que consume el modelo Random Forest entrenado. Cada tarea construye sobre las anteriores, terminando con la integración completa y documentación.

**Lenguajes:** JavaScript (React 19 + Vite 8) para frontend, Python (FastAPI) para backend.

## Tasks

- [ ] 1. Configurar estructura del proyecto y dependencias base
  - [ ] 1.1 Crear estructura de carpetas del backend con archivos __init__.py
    - Crear directorio `backend/` con subdirectorios: `routes/`, `services/`, `models/`, `utils/`, `artifacts/`, `tests/`
    - Crear archivos `__init__.py` vacíos en cada subdirectorio
    - Crear `backend/requirements.txt` con dependencias: fastapi, uvicorn, pandas, scikit-learn, joblib, pydantic, python-dotenv, hypothesis, pytest
    - Copiar `model_encoding_map.csv` desde `../../data/processed/` a `backend/artifacts/`
    - _Requirements: 1.1, 1.4, 9.2_

  - [ ] 1.2 Reorganizar estructura del frontend con carpetas de componentes, servicios y utilidades
    - Crear directorios: `src/components/`, `src/services/`, `src/utils/`, `src/config/`, `src/__tests__/`
    - Crear archivo `src/config/env.js` que exporte `API_BASE_URL` desde `import.meta.env.VITE_API_BASE_URL`
    - Crear archivo `.env.example` con variables: `VITE_API_BASE_URL=http://localhost:8000`
    - _Requirements: 1.1, 1.4, 8.3_

  - [ ] 1.3 Instalar dependencias de testing en el frontend
    - Agregar a devDependencies: vitest, @testing-library/react, @testing-library/jest-dom, jsdom, fast-check
    - Configurar vitest en `vite.config.js` con environment jsdom
    - Crear archivo `src/__tests__/setup.js` con imports de @testing-library/jest-dom
    - _Requirements: 9.4_

- [ ] 2. Implementar backend: modelos de datos y utilidades
  - [ ] 2.1 Crear modelos Pydantic en `backend/models/schemas.py`
    - Definir `PredictionRequest` con campos: manufacturer (str), model (str), year (int, ge=1980, le=2024), odometer (int, ge=0, le=300000), fuel (str), transmission (str), type (str)
    - Definir `PredictionResponse` con campos: precio_clp (int), precio_usd (float), vehiculo (VehicleData), advertencias (list[str])
    - Definir `VehicleData`, `OptionsResponse`, `HealthResponse`, `ValidationErrorResponse`, `FieldError`
    - _Requirements: 5.1, 5.3, 9.5_

  - [ ] 2.2 Crear constantes de normalización en `backend/utils/constants.py`
    - Definir constantes: YEAR_MIN=1981, YEAR_MAX=2024, ODOMETER_MIN=1, ODOMETER_MAX=299999, PRICE_MIN=1000, PRICE_MAX=100000
    - Definir listas de categorías para one-hot encoding (manufacturers, fuels, transmissions, types, conditions) con drop_first
    - Definir DEFAULT_LAT y DEFAULT_LONG (promedios del dataset)
    - Definir EXCHANGE_RATE_USD_CLP (default 950)
    - _Requirements: 3.1, 3.3_

  - [ ] 2.3 Crear cargador de modelo en `backend/utils/model_loader.py`
    - Implementar función `load_model(path)` que cargue el archivo .pkl con joblib
    - Implementar función `load_encoding_map(path)` que lea el CSV y retorne un diccionario {modelo: valor_encoding}
    - Calcular y almacenar el promedio global del encoding map para modelos desconocidos
    - Manejar errores de carga con logging apropiado
    - _Requirements: 3.5, 8.6_

- [ ] 3. Implementar backend: motor de preprocesamiento
  - [ ] 3.1 Crear servicio de preprocesamiento en `backend/services/preprocessor.py`
    - Implementar función `preprocess(data: PredictionRequest, encoding_map: dict) -> np.ndarray`
    - Implementar normalización Min-Max para year y odometer usando constantes definidas
    - Implementar Target Encoding para model usando encoding_map (promedio global si no existe)
    - Implementar One-Hot Encoding con drop_first para manufacturer, fuel, transmission, type
    - Construir vector de características en el orden exacto esperado por el modelo (76 columnas)
    - Retornar advertencias si marca o modelo no reconocidos
    - _Requirements: 3.1, 3.2, 3.5, 3.6_

  - [ ]* 3.2 Escribir property test: Preprocesamiento produce vector válido (Property 4)
    - **Property 4: Preprocesamiento produce vector de características válido**
    - Usar Hypothesis para generar entradas válidas aleatorias
    - Verificar que year normalizado está en [0,1], odometer normalizado está en [0,1]
    - Verificar que exactamente una columna one-hot por categoría es 1
    - Verificar longitud exacta del vector de salida
    - **Validates: Requirements 3.1, 3.2**

  - [ ]* 3.3 Escribir property test: Round-trip normalización de precio (Property 5)
    - **Property 5: Round-trip de normalización de precio**
    - Usar Hypothesis para generar precios USD en [1000, 100000]
    - Verificar que normalizar y desnormalizar retorna el valor original (tolerancia 1e-6)
    - Verificar que cualquier valor predicho en [0,1] desnormaliza a [1000, 100000]
    - **Validates: Requirements 3.3**

  - [ ]* 3.4 Escribir property test: Modelo desconocido usa encoding promedio (Property 6)
    - **Property 6: Modelo desconocido usa encoding promedio**
    - Usar Hypothesis para generar strings aleatorios que no existan en el encoding map
    - Verificar que el valor asignado es igual al promedio aritmético del encoding map
    - **Validates: Requirements 3.5**

  - [ ]* 3.5 Escribir property test: Marca desconocida produce one-hot de ceros (Property 7)
    - **Property 7: Marca desconocida produce vector one-hot de ceros**
    - Usar Hypothesis para generar strings que no correspondan a marcas conocidas
    - Verificar que todas las columnas one-hot de manufacturer tienen valor 0
    - **Validates: Requirements 3.6**

- [ ] 4. Implementar backend: servicios y rutas
  - [ ] 4.1 Crear servicio de predicción en `backend/services/prediction.py`
    - Implementar función `predict(request, model, encoding_map) -> PredictionResponse`
    - Invocar preprocesamiento, ejecutar inferencia con el modelo, desnormalizar resultado
    - Convertir USD a CLP usando tasa de cambio configurable
    - Manejar errores de inferencia (valor fuera de [0,1], excepciones del modelo)
    - _Requirements: 3.3, 3.4, 3.7_

  - [ ] 4.2 Crear servicio de opciones en `backend/services/options_loader.py`
    - Implementar función que lea el encoding map y extraiga: lista de manufacturers, models agrupados por manufacturer, fuels, transmissions, types
    - Cachear resultado en memoria al primer llamado
    - _Requirements: 5.2_

  - [ ] 4.3 Crear rutas del backend: predict, options, health
    - Implementar `backend/routes/predict.py` con endpoint POST /api/v1/predict
    - Implementar `backend/routes/options.py` con endpoint GET /api/v1/options
    - Implementar `backend/routes/health.py` con endpoint GET /api/v1/health
    - Manejar errores de validación Pydantic con formato personalizado (422)
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 8.6_

  - [ ] 4.4 Crear punto de entrada `backend/main.py` con configuración CORS y carga del modelo
    - Configurar FastAPI app con título y versión
    - Configurar CORS middleware leyendo ALLOWED_ORIGINS de variable de entorno
    - Cargar modelo .pkl y encoding map al inicio del servidor (evento startup/lifespan)
    - Registrar routers con prefijo /api/v1
    - Incluir documentación Swagger en /docs
    - _Requirements: 1.3, 5.4, 5.5, 8.3_

  - [ ]* 4.5 Escribir property test: Validación backend retorna errores estructurados (Property 9)
    - **Property 9: Validación backend retorna errores estructurados**
    - Usar Hypothesis para generar requests con campos inválidos (año fuera de rango, km negativo, campos faltantes)
    - Verificar que retorna HTTP 422 con arreglo de errores conteniendo field y message
    - **Validates: Requirements 5.3**

- [ ] 5. Checkpoint - Verificar backend funcional
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implementar frontend: utilidades y servicios
  - [ ] 6.1 Crear utilidades de formateo en `src/utils/formatters.js`
    - Implementar `formatPriceCLP(number)` → string con formato "$12.500.000" (separador de miles con punto, sin decimales)
    - Implementar `formatKilometers(km)` → string con formato "120.000 km"
    - _Requirements: 4.1_

  - [ ] 6.2 Crear utilidades de validación en `src/utils/validators.js`
    - Implementar `validateForm(formData)` que retorne objeto de errores o null
    - Implementar `isValidYear(year)` → boolean (rango [1980, año actual])
    - Implementar `isValidOdometer(km)` → boolean (rango [0, 300000])
    - Validar que todos los campos obligatorios estén presentes
    - _Requirements: 2.4, 2.5, 2.6_

  - [ ] 6.3 Crear constantes del frontend en `src/utils/constants.js`
    - Definir LOADING_MESSAGES (array de al menos 3 mensajes)
    - Definir LOADING_INTERVAL (3000ms para rotación de mensajes)
    - Definir API_TIMEOUT (10000ms)
    - Definir YEAR_MIN, YEAR_MAX, ODOMETER_MAX
    - _Requirements: 4.3, 8.5_

  - [ ] 6.4 Crear servicio API client en `src/services/apiClient.js`
    - Implementar `getOptions()` → Promise<OptionsResponse> con timeout de 10s
    - Implementar `predict(data)` → Promise<PredictionResponse> con timeout de 10s
    - Implementar `healthCheck()` → Promise<boolean>
    - Usar `API_BASE_URL` desde config/env.js
    - Manejar errores de red y timeout con mensajes categorizados
    - _Requirements: 2.2, 2.8, 5.1, 8.5_

  - [ ]* 6.5 Escribir property test: Formateo de precio en CLP (Property 8)
    - **Property 8: Formateo de precio en CLP**
    - Usar fast-check para generar enteros positivos
    - Verificar que el resultado comienza con "$", usa punto como separador de miles, no tiene decimales
    - Verificar round-trip: parsear el string de vuelta produce el número original
    - **Validates: Requirements 4.1**

  - [ ]* 6.6 Escribir property tests: Validación de formulario (Properties 2 y 3)
    - **Property 2: Validación de formulario rechaza entradas inválidas**
    - **Property 3: Validación de rangos numéricos**
    - Usar fast-check para generar formularios con campos vacíos o valores fuera de rango
    - Verificar que validateForm retorna errores cuando hay campos inválidos
    - Verificar que isValidYear acepta solo [1980, añoActual] e isValidOdometer acepta solo [0, 300000]
    - **Validates: Requirements 2.4, 2.5, 2.6**

- [ ] 7. Implementar frontend: componentes React
  - [ ] 7.1 Crear componente `Header.jsx`
    - Extraer header del App.jsx actual a componente independiente
    - Incluir ícono, título "Predicción de Precios" y descripción
    - Mantener estilos existentes con variables CSS
    - _Requirements: 6.1, 9.1_

  - [ ] 7.2 Crear componentes auxiliares: `LoadingIndicator.jsx`, `ErrorMessage.jsx`, `WarningBanner.jsx`
    - `LoadingIndicator`: spinner animado con mensajes rotativos (props: messages, interval)
    - `ErrorMessage`: muestra error categorizado con botón reintentar (props: error, onRetry)
    - `WarningBanner`: banner amarillo con lista de advertencias (props: warnings)
    - Respetar prefers-reduced-motion para animaciones
    - _Requirements: 4.3, 4.4, 4.5, 6.4, 6.5_

  - [ ] 7.3 Crear componente `PredictionForm.jsx`
    - Formulario con campos: manufacturer, model, year, odometer, fuel, transmission, type
    - Poblar opciones desde props (obtenidas del backend via apiClient)
    - Filtrar modelos dinámicamente al seleccionar marca
    - Validación client-side usando validators.js antes de enviar
    - Mostrar errores inline por campo
    - Deshabilitar campo modelo hasta seleccionar marca
    - Estados: default, loading opciones, error carga opciones, enviando predicción
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 6.6_

  - [ ] 7.4 Crear componente `ResultPanel.jsx`
    - Mostrar precio formateado usando formatPriceCLP
    - Mostrar resumen del vehículo (todos los campos ingresados)
    - Integrar WarningBanner si hay advertencias
    - Estado placeholder cuando no hay resultado
    - Estado loading con LoadingIndicator
    - Botón "Nueva consulta" para resetear
    - _Requirements: 4.1, 4.2, 4.3, 4.5, 4.6_

  - [ ]* 7.5 Escribir property test: Filtrado de modelos por marca (Property 1)
    - **Property 1: Filtrado de modelos por marca**
    - Usar fast-check para generar selecciones de marca del conjunto de opciones
    - Verificar que los modelos mostrados pertenecen exclusivamente a la marca seleccionada
    - **Validates: Requirements 2.3**

  - [ ] 7.6 Refactorizar `App.jsx` como orquestador principal
    - Reemplazar lógica del mockup con componentes nuevos (Header, PredictionForm, ResultPanel)
    - Manejar estado global: options, loading, result, error
    - Cargar opciones al montar componente via apiClient.getOptions()
    - Manejar flujo: envío formulario → apiClient.predict() → mostrar resultado
    - Manejar errores de carga de opciones y predicción
    - _Requirements: 1.4, 9.1_

- [ ] 8. Checkpoint - Verificar frontend funcional
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Estilos CSS y diseño responsivo
  - [ ] 9.1 Actualizar `index.css` con variables CSS y estilos responsivos
    - Definir variables en :root: --primary (#1ED760), --background (#121212), tipografía, espaciados base 4px, border-radius 0px
    - Agregar estilos para nuevos componentes (WarningBanner, ErrorMessage, LoadingIndicator)
    - Implementar media queries para móvil (320px), tablet (768px), escritorio (1024px+)
    - Agregar transiciones CSS (100-300ms) para hover, focus, aparición de resultados
    - Implementar @media (prefers-reduced-motion: reduce) para desactivar animaciones
    - Definir estados visuales: default, hover, focus-visible, active, disabled
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [ ] 10. Preparación para despliegue
  - [ ] 10.1 Crear `backend/Dockerfile`
    - Base image Python 3.11-slim
    - Copiar requirements.txt e instalar dependencias
    - Copiar código del backend y artefactos
    - Exponer puerto configurable via variable de entorno (default 8000)
    - CMD: uvicorn main:app --host 0.0.0.0 --port $PORT
    - _Requirements: 8.2, 8.4_

  - [ ] 10.2 Configurar variables de entorno y archivos de despliegue
    - Crear `.env.example` completo con todas las variables: VITE_API_BASE_URL, ALLOWED_ORIGINS, MODEL_PATH, ENCODING_MAP_PATH, PORT, EXCHANGE_RATE_USD_CLP
    - Verificar que `vite.config.js` produce build estático compatible con Vercel
    - Crear `vercel.json` si es necesario para SPA routing
    - _Requirements: 8.1, 8.3_

- [ ] 11. Documentación técnica
  - [ ] 11.1 Crear documentación con diagramas Mermaid en `docs/`
    - Crear `docs/arquitectura.md` con diagrama Mermaid de arquitectura general (Frontend, Backend, Modelo ML, protocolos)
    - Crear `docs/flujo-prediccion.md` con diagrama Mermaid de secuencia del flujo completo
    - Crear `docs/estructura-proyecto.md` con listado de directorios y sus propósitos
    - Crear `docs/estrategia-despliegue.md` con plataformas, variables de entorno y pasos de despliegue
    - Cada documento en español con secciones: título, descripción general, contenido técnico, referencias
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

  - [ ] 11.2 Actualizar `README.md` del proyecto
    - Agregar secciones: descripción, requisitos previos (Node.js, Python), instalación, ejecución local (frontend y backend), variables de entorno, despliegue
    - _Requirements: 9.3_

- [ ] 12. Checkpoint final - Verificar sistema completo
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Las tareas marcadas con `*` son opcionales y pueden omitirse para un MVP más rápido
- Cada tarea referencia requisitos específicos para trazabilidad
- Los checkpoints aseguran validación incremental
- Los property tests validan propiedades universales de corrección definidas en el diseño
- Los unit tests validan ejemplos específicos y casos borde
- El modelo .pkl (~1.5GB) NO se copia al backend; se referencia via variable de entorno MODEL_PATH
- El encoding_map.csv SÍ se copia a backend/artifacts/ para independencia del backend
- Frontend usa JavaScript (React 19 + Vite 8), Backend usa Python (FastAPI)

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3"] },
    { "id": 1, "tasks": ["2.1", "2.2", "2.3", "6.1", "6.2", "6.3"] },
    { "id": 2, "tasks": ["3.1", "4.2", "6.4"] },
    { "id": 3, "tasks": ["3.2", "3.3", "3.4", "3.5", "4.1", "6.5", "6.6"] },
    { "id": 4, "tasks": ["4.3", "7.1", "7.2"] },
    { "id": 5, "tasks": ["4.4", "4.5", "7.3", "7.4"] },
    { "id": 6, "tasks": ["7.5", "7.6"] },
    { "id": 7, "tasks": ["9.1"] },
    { "id": 8, "tasks": ["10.1", "10.2"] },
    { "id": 9, "tasks": ["11.1", "11.2"] }
  ]
}
```
