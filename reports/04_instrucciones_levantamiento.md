# 04_instrucciones_levantamiento.md
### Proyecto de Regresión de Precios de Vehículos

**Autor:** Celso Farías  
**Fecha:** 04 de Junio de 2026

---

## Descripción General

Este documento describe el procedimiento completo para levantar el sistema de predicción de precios de vehículos en un entorno local. El sistema está compuesto por dos componentes independientes que deben ejecutarse simultáneamente:

- **Backend:** API REST desarrollada con FastAPI con Python
- **Frontend:** Aplicación web desarrollada con React + Vite con JavaScript

Ambos componentes se comunican a través de HTTP. El backend expone el modelo de Machine Learning y el frontend provee la interfaz de usuario.

---

## Requisitos Previos

Antes de comenzar, verificar que el equipo cuente con lo siguiente:

### Software necesario

| Software | Versión mínima | Verificación |
|----------|---------------|-------------|
| Python | 3.11+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Git | cualquiera | `git --version` |

### Hardware recomendado

| Recurso | Mínimo | Motivo |
|---------|--------|--------|
| RAM | 4 GB | El modelo Random Forest ocupa ~1.5 GB en memoria |
| Almacenamiento libre | 3 GB | Modelo + dependencias Python + dependencias Node |

### Archivos necesarios, no incluidos en el repositorio por tamaño

Los siguientes archivos deben estar presentes en su ubicación correcta:

```
proyecto-autos/
├── models/
│   └── random_forest/
│       └── model.pkl        ← Modelo entrenado (~1.5 GB)
└── data/
    └── processed/
        ├── vehicles_processed.csv
        └── model_encoding_map.csv
```

Modelo descargable en: 

https://uandresbelloedu-my.sharepoint.com/:u:/g/personal/c_farasaraya1_uandresbello_edu/IQAJguXk5NHRSobkVJO9NPs-AdwxkTtYyQC6ArIhTL6Sfzk?e=5Mw6PF

> Si no se dispone de estos archivos, contactar al autor del proyecto o generarlos ejecutando los notebooks en orden; `notebooks/01_EDA...`, `notebooks/02_preprocesamiento...`, scripts en `src/`; siguiendo las instrucciones de los demas reportes y notebooks, son totalmente reproducibles.

---

## PARTE 1: Levantamiento del Backend con FastAPI

### Paso 1 — Navegar a la carpeta del backend

```powershell
cd "D:\ruta\a\proyecto-autos\app-mockup-autos-celso\backend"
```

Ajustar la ruta según la ubicación del proyecto en tu equipo.

---

### Paso 2 — Crear el entorno virtual Python

Solo se realiza la primera vez. Si ya existe el entorno, saltar al Paso 3.

```powershell
python -m venv venv
```

Esto crea una carpeta `venv/` dentro de `backend/` con un intérprete Python aislado.

> El entorno virtual garantiza que las dependencias del proyecto no interfieran con otras instalaciones de Python en el sistema.

---

### Paso 3 — Activar el entorno virtual

**Windows con PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows con CMD:**
```cmd
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

Al activarse correctamente, el prompt de la terminal mostrará el nombre del entorno entre paréntesis:
```
(venv) PS D:\...\backend>
```

> Si PowerShell rechaza la ejecución del script con un error de política, ejecutar primero: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

### Paso 4 — Instalar dependencias Python

Solo se realiza la primera vez o cuando cambien las dependencias.

```powershell
pip install -r requirements.txt
```

Esto instalará: FastAPI, Uvicorn, scikit-learn, pandas, numpy, joblib, pydantic y python-dotenv.

> La instalación puede tardar varios minutos dependiendo de la conexión a internet.

---

### Paso 5 — Configurar variables de entorno, solo primera vez

Copiar el archivo de ejemplo y ajustar si es necesario:

```powershell
copy .env.example .env
```

El archivo `.env` no se incluye en el repositorio. Debe crearse e incluir la siguiente ruta para que el frontend y el backend puedan comunicarse.

Variable en `.env`:

```env
VITE_API_URL=http://localhost:8000
```

---

### Paso 6 — Levantar el servidor backend

Con el entorno virtual activo:

```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Indicadores de inicio exitoso:**

```
INFO | Iniciando API de Predicción de Precios de Vehículos
INFO | Cargando modelo (1520 MB). Esto puede tomar 10-30 segundos...
INFO | Encoding map cargado: 20533 modelos.
INFO | Parámetros del scaler cargados: 7 columnas
INFO | Modelo cargado en 29.6s. Features: 91
INFO | ✅ Servidor listo — modelo cargado en memoria
INFO | Application startup complete.
```

> La primera vez puede tardar hasta 60 segundos por la carga del modelo de 1.5 GB.

**URLs disponibles:**
- API: `http://localhost:8000`
- Documentación Swagger: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/api/v1/health`

---

## PARTE 2: Levantamiento del Frontend (React + Vite)

Abrir una **nueva terminal**, el backend debe seguir corriendo.

### Paso 7 — Navegar a la carpeta del frontend

```powershell
cd "D:\ruta\a\proyecto-autos\app-mockup-autos-celso"
```

---

### Paso 8 — Instalar dependencias Node.js

Solo se realiza la primera vez o cuando cambien las dependencias.

```powershell
npm install
```

Esto instalará React, Vite, Axios y demás dependencias listadas en `package.json`.

---

### Paso 9 — Configurar variable de entorno del frontend

Verificar que existe el archivo `.env` en la raíz del frontend (`app-mockup-autos-celso/.env`):

```env
VITE_API_URL=http://localhost:8000
```

Si no existe, crearlo:

```powershell
echo VITE_API_URL=http://localhost:8000 > .env
```

---

### Paso 10 — Levantar el servidor de desarrollo

```powershell
npm run dev
```

**Indicador de inicio exitoso:**
```
  VITE v8.x.x  ready in 800ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

La aplicación estará disponible en: `http://localhost:5173`

---

## Resumen de comandos de inicio diario

Una vez que el entorno está configurado; Pasos 1–5 ya realizados; el sistema se levanta con:

**Terminal 1 — Backend:**
```powershell
cd "ruta\a\backend"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Frontend:**
```powershell
cd "ruta\a\app-mockup-autos-celso"
npm run dev
```

Navegar a: `http://localhost:5173`

---

## Verificación del sistema completo

Una vez levantados ambos componentes, verificar con los siguientes pasos:

### 1. Verificar backend (health check)

Abrir en el navegador: `http://localhost:8000/api/v1/health`

Respuesta esperada:
```json
{
  "status": "ok",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### 2. Verificar opciones del formulario

Abrir en el navegador: `http://localhost:8000/api/v1/options`

Debe retornar un JSON con marcas, modelos, combustibles, etc.

### 3. Verificar predicción desde Swagger

Abrir `http://localhost:8000/docs`, expandir `POST /api/v1/predict` y ejecutar con el ejemplo:

```json
{
  "manufacturer": "toyota",
  "model": "camry",
  "year": 2018,
  "odometer": 45000,
  "fuel": "gas",
  "transmission": "automatic",
  "type": "sedan",
  "condition": "good"
}
```

Respuesta esperada: precio predicho en USD y CLP.

### 4. Verificar frontend

Abrir `http://localhost:5173`, completar el formulario y ejecutar una predicción. El resultado debe mostrarse en el panel derecho.

---

## Resolución de Problemas Comunes

### "No module named fastapi"
El entorno virtual no está activado.
```powershell
.\venv\Scripts\Activate.ps1
```

### "uvicorn: comando no reconocido"
Usar el módulo de Python directamente:
```powershell
python -m uvicorn app.main:app --port 8000
```

### Error al cargar el modelo (.pkl)
Verificar que el archivo existe en la ruta configurada en `.env`:
```powershell
Test-Path "..\..\models\random_forest\model.pkl"
```
Debe retornar `True`.

### Frontend muestra "No se pudo conectar con el servidor"
- Verificar que el backend está corriendo en el puerto 8000.
- Verificar que `.env` del frontend contiene `VITE_API_URL=http://localhost:8000`.
- Esperar a que el backend termine de cargar el modelo (~30 segundos).

### Error de política de ejecución en PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Puerto 8000 ya está en uso
```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :8000

# Usar un puerto diferente
python -m uvicorn app.main:app --port 8001
# Y actualizar .env del frontend: VITE_API_URL=http://localhost:8001
```
