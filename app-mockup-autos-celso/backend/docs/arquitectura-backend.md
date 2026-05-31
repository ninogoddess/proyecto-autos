# Arquitectura del Backend

## Descripción General

El backend es una API REST construida con FastAPI que expone un modelo de Machine Learning (Random Forest) para predicción de precios de vehículos usados. Sigue una arquitectura modular con separación clara de responsabilidades.

## Diagrama de Arquitectura

```mermaid
graph TB
    subgraph Cliente["Cliente (Frontend React)"]
        FE[Aplicación Web]
    end

    subgraph API["FastAPI Backend"]
        MW[Middleware CORS]
        R1[Router /health]
        R2[Router /options]
        R3[Router /predict]
        
        subgraph Services["Capa de Servicios"]
            PS[Prediction Service]
            PP[Preprocessor]
            OS[Options Service]
        end
        
        subgraph Utils["Utilidades"]
            ML[Model Loader]
            CFG[Settings]
        end
    end

    subgraph Artifacts["Artefactos ML"]
        MODEL[model.pkl ~1.5GB]
        EMAP[model_encoding_map.csv]
    end

    FE -->|HTTP REST| MW
    MW --> R1
    MW --> R2
    MW --> R3
    R3 --> PS
    PS --> PP
    PP --> ML
    R2 --> OS
    ML -->|joblib.load| MODEL
    ML -->|pd.read_csv| EMAP
    R1 --> ML
```

## Flujo de una Predicción

```mermaid
sequenceDiagram
    participant C as Cliente
    participant API as FastAPI
    participant V as Pydantic Validator
    participant PP as Preprocessor
    participant ML as Random Forest

    C->>API: POST /api/v1/predict (JSON)
    API->>V: Validar datos de entrada
    
    alt Datos inválidos
        V-->>API: ValidationError
        API-->>C: 422 {detail: [{field, message}]}
    end
    
    V->>PP: VehicleInput validado
    PP->>PP: Target Encoding (model)
    PP->>PP: One-Hot Encoding (categóricas)
    PP->>PP: Construir vector 91 features
    PP->>ML: numpy array [1, 91]
    ML->>PP: valor predicho (escala StandardScaler)
    PP->>API: Desnormalizar → USD → CLP
    API-->>C: 200 {predicted_price_clp, warnings}
```

## Decisiones de Diseño

### 1. Carga del modelo al startup (Lazy Loading)
- **Problema:** El modelo pesa ~1.5 GB
- **Solución:** Se carga una sola vez al iniciar el servidor usando el evento `lifespan`
- **Beneficio:** Cada request toma <1s en lugar de 10-30s

### 2. StandardScaler sin parámetros guardados
- **Problema:** El scaler no fue serializado junto al modelo
- **Solución:** Random Forest es invariante a escala (usa umbrales, no distancias). Se aproximan los parámetros con estadísticas conocidas del dataset.
- **Riesgo:** Predicciones pueden tener offset. Se mitiga con validación de rangos.

### 3. Separación de responsabilidades
- **Routers:** Solo manejan HTTP (request/response)
- **Services:** Lógica de negocio (predicción, preprocesamiento)
- **Utils:** Infraestructura (carga de archivos, configuración)
- **Schemas:** Contratos de datos (Pydantic)

### 4. Manejo de valores desconocidos
- **Modelo no reconocido:** Se usa el promedio global del encoding map + advertencia
- **Marca no reconocida:** Todas las columnas one-hot en 0 + advertencia
- **El usuario siempre recibe una predicción** (aunque sea menos precisa)

## Consideraciones de Despliegue

| Aspecto | Requisito |
|---------|-----------|
| RAM mínima | 2 GB (modelo ~1.5 GB + overhead) |
| Tiempo de inicio | 10-30 segundos |
| Concurrencia | Limitada por GIL de Python (usar workers) |
| Escalabilidad | Horizontal con múltiples instancias |
| Health check | GET /api/v1/health para load balancers |

## Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [scikit-learn RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)
- Notebook de entrenamiento: `notebooks/02_preprocesamiento_Primer_avance_CD_autos.ipynb`
- Script de encoding: `src/encode_dataset.py`
