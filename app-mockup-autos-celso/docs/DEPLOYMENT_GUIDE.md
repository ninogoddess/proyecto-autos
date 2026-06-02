# DEPLOYMENT_GUIDE.md
## Guía de Despliegue — Sistema de Predicción de Precios de Vehículos

**Proyecto:** Hito 2 — Ciencia de Datos, UNAB  
**Fecha:** Junio 2026

---

## Arquitectura de Despliegue

```
┌─────────────────────────────────────────────────────────┐
│                    INTERNET                             │
└────────────────┬────────────────────────────────────────┘
                 │
     ┌──────────┴──────────┐
     │                     │
     ▼                     ▼
┌─────────┐         ┌──────────────────────┐
│ Vercel  │         │  Cloudflare Tunnel   │
│(Frontend│         │  (URL pública HTTPS) │
│  React) │         └──────────┬───────────┘
└────┬────┘                    │ túnel seguro
     │                         ▼
     │                ┌─────────────────┐
     │ VITE_API_URL   │  Tu PC (local)  │
     └───────────────►│  FastAPI :8000  │
                      │  + Modelo 1.5GB │
                      └─────────────────┘
```

---

## PARTE 1: Frontend en Vercel

### Estado actual
El frontend ya está desplegado en Vercel. Solo falta configurar la variable de entorno `VITE_API_URL` para que apunte al backend.

### Configurar variable de entorno en Vercel

1. Ir a [vercel.com/dashboard](https://vercel.com/dashboard)
2. Seleccionar el proyecto del frontend
3. Settings → Environment Variables
4. Agregar:

```
Name:  VITE_API_URL
Value: https://TU-SUBDOMINIO.trycloudflare.com
```

> ⚠️ El valor depende de la URL que genere Cloudflare Tunnel (ver Parte 2).

5. Hacer un nuevo deploy (o Redeploy) para que tome efecto.

---

## PARTE 2: Backend con Cloudflare Tunnel

### ¿Qué es Cloudflare Tunnel?

Cloudflare Tunnel crea un túnel seguro entre tu PC y los servidores de Cloudflare, exponiéndolo con una URL HTTPS pública sin necesidad de abrir puertos en el router ni tener IP fija.

**Ventajas:**
- 100% gratuito
- HTTPS automático
- URL persistente con cuenta gratuita
- Sin configuración de firewall
- Protección DDoS incluida

### Instalación de cloudflared (Windows)

```powershell
# Opción A: Descarga directa
# Ir a: https://github.com/cloudflare/cloudflared/releases
# Descargar: cloudflared-windows-amd64.msi
# Instalar el .msi

# Verificar instalación
cloudflared --version
```

### Uso rápido (URL temporal, sin cuenta)

Si solo necesitas una URL temporal para una demo:

```powershell
# 1. Iniciar el backend normalmente
cd "D:\tareas antiguas\CdeDatos\proyecto-autos\app-mockup-autos-celso\backend"
.\servidor-autos\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. En otra terminal, iniciar el túnel
cloudflared tunnel --url http://localhost:8000
```

Cloudflared mostrará una URL como:
```
https://random-words-here.trycloudflare.com
```

Esa es tu URL pública. **Copia esta URL** y úsala como `VITE_API_URL` en Vercel.

> ⚠️ Esta URL cambia cada vez que reinicias cloudflared. Para una URL fija, usar el método con cuenta (ver abajo).

### Uso con URL fija (cuenta gratuita de Cloudflare)

```powershell
# 1. Crear cuenta en cloudflare.com (gratis)
# 2. Autenticar cloudflared
cloudflared tunnel login

# 3. Crear un túnel con nombre
cloudflared tunnel create autos-celso-backend

# 4. Crear archivo de configuración
# Guardar como: C:\Users\Admin\.cloudflared\config.yml
```

Contenido del archivo `config.yml`:
```yaml
tunnel: autos-celso-backend
credentials-file: C:\Users\Admin\.cloudflared\<TU-TUNNEL-ID>.json

ingress:
  - hostname: autos-celso.tu-dominio.workers.dev
    service: http://localhost:8000
  - service: http_status:404
```

```powershell
# 5. Iniciar el túnel
cloudflared tunnel run autos-celso-backend
```

---

## PARTE 3: Alternativa — Hugging Face Spaces

Si prefieres desplegar en la nube (requiere subir el modelo de 1.5 GB):

### Pasos

1. Crear cuenta en [huggingface.co](https://huggingface.co)
2. Crear un nuevo Space: New Space → Docker
3. Subir el modelo vía Git LFS:

```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git add models/random_forest/model.pkl
git commit -m "Add model"
git push
```

4. Crear `Dockerfile` en la raíz del Space:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY app/artifacts/ ./app/artifacts/

ENV MODEL_PATH=/app/models/random_forest/model.pkl
ENV ENCODING_MAP_PATH=/app/data/model_encoding_map.csv
ENV PORT=7860
ENV ALLOWED_ORIGINS=https://tu-frontend.vercel.app

EXPOSE 7860
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

> ⚠️ La primera carga del modelo tardará ~60 segundos. Hugging Face pone el Space en sleep tras 15 min de inactividad.

---

## PARTE 4: Configurar CORS para producción

Cuando el backend esté expuesto públicamente, hay que agregar la URL del frontend de Vercel a los orígenes CORS permitidos.

### Opción A: Variable de entorno en backend local

En el archivo `backend/.env`:
```env
ALLOWED_ORIGINS=http://localhost:5173,https://TU-PROYECTO.vercel.app
```

### Opción B: Variable en Cloudflare / Hugging Face

Al iniciar el backend, inyectar la variable:
```powershell
$env:ALLOWED_ORIGINS = "https://TU-PROYECTO.vercel.app,http://localhost:5173"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## PARTE 5: Verificación del sistema completo

### Checklist de verificación

```
□ Backend corriendo en localhost:8000
□ cloudflared corriendo y mostrando URL pública
□ GET https://TU-URL/api/v1/health → {"status":"ok","model_loaded":true}
□ GET https://TU-URL/api/v1/options → lista de opciones del formulario
□ POST https://TU-URL/api/v1/predict → precio predicho
□ VITE_API_URL configurado en Vercel con la URL del túnel
□ Frontend en Vercel conecta con el backend
□ Flujo completo: formulario → predicción → resultado
```

### Comandos de verificación rápida

```powershell
# Verificar health del backend local
curl http://localhost:8000/api/v1/health

# Verificar health del backend público
curl https://TU-URL.trycloudflare.com/api/v1/health

# Test de predicción completo
curl -X POST https://TU-URL.trycloudflare.com/api/v1/predict `
  -H "Content-Type: application/json" `
  -d '{"manufacturer":"toyota","model":"camry","year":2018,"odometer":45000,"fuel":"gas","transmission":"automatic","type":"sedan","condition":"good"}'
```

---

## PARTE 6: Procedimiento de inicio diario (demo)

Para presentaciones o demostraciones:

```powershell
# Terminal 1: Iniciar backend
cd "D:\tareas antiguas\CdeDatos\proyecto-autos\app-mockup-autos-celso\backend"
.\servidor-autos\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
# Esperar ~30s hasta ver: "✅ Servidor listo — modelo cargado en memoria"

# Terminal 2: Iniciar túnel
cloudflared tunnel --url http://localhost:8000
# Copiar la URL generada → actualizar VITE_API_URL en Vercel si cambió
```

---

## Troubleshooting

### Error: "No se pudo conectar con el servidor"
- Verificar que el backend está corriendo en localhost:8000
- Verificar que cloudflared está activo y mostrando la URL
- Verificar que `VITE_API_URL` en Vercel apunta a la URL actual del túnel

### Error: "CORS policy blocked"
- Agregar la URL del frontend de Vercel a `ALLOWED_ORIGINS` en el backend
- Reiniciar el backend y cloudflared

### El backend tarda en responder la primera vez
- Normal. El modelo tarda ~30 segundos en cargar al iniciar el servidor
- Una vez cargado, las predicciones demoran <1 segundo

### Cloudflare Tunnel muestra error de conexión
- Verificar que el backend está corriendo ANTES de iniciar el túnel
- Verificar que el puerto 8000 no está bloqueado por firewall local

---

## Evidencia para el Informe

### Capturas sugeridas

1. `GET /api/v1/health` → `{"status":"ok","model_loaded":true}` en Postman o browser
2. `GET /api/v1/options` → lista de marcas/modelos en Postman
3. `POST /api/v1/predict` → respuesta con precio en Postman/Swagger
4. Frontend en Vercel cargado y mostrando el formulario
5. Formulario completo con predicción exitosa
6. Terminal con logs del backend mostrando requests entrantes
7. Terminal con cloudflared mostrando la URL pública
8. Panel de Vercel con la variable `VITE_API_URL` configurada

### URL públicas esperadas

- **Frontend:** `https://app-mockup-autos-celso.vercel.app` (o tu URL en Vercel)
- **Backend API Docs:** `https://TU-URL.trycloudflare.com/docs`
- **Health Check:** `https://TU-URL.trycloudflare.com/api/v1/health`
