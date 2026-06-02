# DEPLOYMENT_ANALYSIS.md
## Análisis de Despliegue — Backend con Modelo Random Forest

**Proyecto:** Predicción de Precios de Vehículos — Hito 2  
**Autor:** Celso Farías  
**Fecha:** Junio 2026

---

## 1. Análisis Técnico del Backend

### Características del Modelo

| Parámetro | Valor |
|-----------|-------|
| Archivo | `models/random_forest/model.pkl` |
| Tamaño en disco | **1,519.9 MB (~1.5 GB)** |
| Tiempo de carga (local, Ryzen 7 4800H) | **~30 segundos** |
| Estimadores (árboles) | 100 |
| Features de entrada | 91 columnas |
| RAM en runtime (estimada) | **~1.8 - 2.2 GB** |
| Framework | scikit-learn RandomForestRegressor |

### Requisitos del Backend

| Requisito | Valor mínimo |
|-----------|-------------|
| Python | 3.11+ |
| RAM | **2 GB** (mínimo absoluto) |
| Almacenamiento | **2 GB** (modelo + dependencias Python ~500 MB) |
| CPU | Sin requisitos especiales (inferencia ~50ms post-carga) |
| Red | Acceso HTTP en puertos 8000+ |
| Tiempo de inicio | ~30-60 segundos (carga del modelo) |

### Dependencias Python

```
fastapi, uvicorn, pydantic, scikit-learn, joblib, pandas, numpy, python-dotenv
```

Tamaño estimado del entorno virtual: ~500 MB

---

## 2. Análisis Comparativo de Plataformas

### Criterio crítico de filtrado

> Un modelo de **1.5 GB en RAM** descalifica automáticamente cualquier servicio con menos de 2 GB de RAM disponible.

---

### 2.1 Render (render.com)

| Aspecto | Detalle |
|---------|---------|
| **Plan gratuito RAM** | 512 MB |
| **Plan gratuito almacenamiento** | 0.1 GB (ephemeral) |
| **Costo plan viable** | $25/mes (2 GB RAM) |
| **FastAPI compatible** | ✅ Sí |
| **Modelo 1.5 GB viable** | ❌ Plan gratuito: NO. Plan pago: SÍ |
| **Dificultad** | Baja — deploy desde GitHub |
| **Riesgos** | Spin-down tras 15 min de inactividad (plan gratuito) |

**Veredicto:** El plan gratuito tiene solo 512 MB RAM — insuficiente. El plan de $25/mes es la opción más simple si se quiere pagar.

---

### 2.2 Railway (railway.app)

| Aspecto | Detalle |
|---------|---------|
| **Plan gratuito RAM** | Hasta 8 GB disponibles, pero **$5 USD de crédito/mes** |
| **Almacenamiento** | Efímero, sin persistencia |
| **Costo estimado** | ~$5-15/mes dependiendo del uso |
| **FastAPI compatible** | ✅ Sí |
| **Modelo 1.5 GB viable** | ⚠️ Técnicamente sí (RAM suficiente), pero el crédito gratuito se agota rápido con 2 GB de RAM |
| **Dificultad** | Baja |
| **Riesgos** | Costos variables, crédito gratuito limitado |

**Veredicto:** Técnicamente viable, pero el costo del crédito gratuito se consume rápidamente con una instancia de 2 GB. Para un proyecto académico temporal, podría funcionar dentro del crédito gratuito.

---

### 2.3 Fly.io (fly.io)

| Aspecto | Detalle |
|---------|---------|
| **Plan gratuito RAM** | 256 MB (shared) |
| **Almacenamiento** | 3 GB para Docker image |
| **Costo plan viable** | ~$12-20/mes (dedicated-cpu-1x, 2 GB RAM) |
| **FastAPI compatible** | ✅ Sí (via Dockerfile) |
| **Modelo 1.5 GB viable** | ❌ Plan gratuito: NO. Plan pago: SÍ |
| **Dificultad** | Media — requiere flyctl CLI |
| **Riesgos** | Curva de aprendizaje, billing complejo |

**Veredicto:** Técnicamente bueno pero más complejo que Render o Railway. El modelo no cabe en el plan gratuito.

---

### 2.4 Koyeb (koyeb.com)

| Aspecto | Detalle |
|---------|---------|
| **Plan gratuito RAM** | 512 MB |
| **Almacenamiento** | Efímero |
| **Costo plan viable** | $8.50/mes (nano: 512 MB → insuficiente) |
| **FastAPI compatible** | ✅ Sí |
| **Modelo 1.5 GB viable** | ❌ NO — ningún plan con 2 GB a precio razonable |
| **Dificultad** | Baja |
| **Riesgos** | RAM máxima disponible insuficiente para el modelo |

**Veredicto:** Descartado. No ofrece suficiente RAM a precio accesible.

---

### 2.5 Hugging Face Spaces (huggingface.co/spaces)

| Aspecto | Detalle |
|---------|---------|
| **Plan gratuito RAM** | 16 GB (con Gradio/Streamlit) |
| **Almacenamiento** | 50 GB (LFS para modelos grandes) |
| **Costo** | **$0 (gratuito para modelos < 50 GB)** |
| **FastAPI compatible** | ✅ Sí (via Docker Space) |
| **Modelo 1.5 GB viable** | ✅ **SÍ — el modelo entra con margen** |
| **Dificultad** | Media — requiere configuración Docker |
| **Riesgos** | Sleep tras inactividad (~15 min), CPU-only, arranque lento (~60s) |
| **Ideal para** | Demos académicas y portfolios |

**Veredicto:** La opción gratuita más poderosa para modelos grandes. 16 GB de RAM y soporte LFS para modelos pesados. Ideal para el contexto académico.

---

### 2.6 Oracle Cloud Free Tier (cloud.oracle.com)

| Aspecto | Detalle |
|---------|---------|
| **RAM gratuita** | 24 GB (ARM Ampere, 4 CPU) — **permanente** |
| **Almacenamiento** | 200 GB |
| **Costo** | **$0 permanente (Always Free)** |
| **FastAPI compatible** | ✅ Sí (VM completa, instala lo que quieras) |
| **Modelo 1.5 GB viable** | ✅ **SÍ — sobra RAM** |
| **Dificultad** | Alta — requiere configurar VM, red, firewall, IP pública |
| **Riesgos** | Verificación de tarjeta al registrarse, configuración compleja, puede ser reclamada si no se usa |

**Veredicto:** Técnicamente la mejor opción gratuita permanente. Sin embargo, la configuración es significativamente más compleja (VM Linux, seguridad de red, certificados SSL). Viable pero requiere tiempo.

---

### 2.7 Google Cloud Free Tier (cloud.google.com)

| Aspecto | Detalle |
|---------|---------|
| **Crédito inicial** | $300 USD por 90 días |
| **Always Free** | f1-micro (0.6 GB RAM) — insuficiente para el modelo |
| **Costo post-trial** | ~$30-50/mes para una instancia con 2 GB+ RAM |
| **FastAPI compatible** | ✅ Sí |
| **Modelo 1.5 GB viable** | ⚠️ Solo con el crédito de $300 |

**Veredicto:** El crédito de $300 permite desplegarlo temporalmente, pero no es sustentable. El Always Free es insuficiente.

---

### 2.8 AWS Free Tier (aws.amazon.com)

| Aspecto | Detalle |
|---------|---------|
| **Free Tier** | t2.micro (1 GB RAM) — insuficiente |
| **Costo para 2 GB** | t2.small ~$16/mes |
| **FastAPI compatible** | ✅ Sí |
| **Modelo 1.5 GB viable** | ❌ Free tier insuficiente |

**Veredicto:** Descartado para uso gratuito. La instancia gratuita tiene solo 1 GB RAM.

---

### 2.9 Backend local + Túnel (ngrok / Cloudflare Tunnel)

| Aspecto | Detalle |
|---------|---------|
| **Costo** | $0 |
| **RAM** | La de tu PC (16 GB según el informe del proyecto) |
| **Almacenamiento** | El de tu PC |
| **FastAPI compatible** | ✅ Sí |
| **Modelo 1.5 GB viable** | ✅ **SÍ — ya funciona localmente** |
| **Dificultad** | Baja (ngrok) / Media (Cloudflare Tunnel) |
| **Riesgos** | Depende de conexión a internet, PC debe estar encendida durante demos |
| **URL pública** | ✅ Sí (URL temporal o fija con plan) |

**ngrok:** URL pública generada instantáneamente. Plan gratuito tiene URL aleatoria que cambia cada sesión. Plan $8/mes tiene URL fija.  
**Cloudflare Tunnel:** URL fija y permanente, completamente gratis, más robusto que ngrok.

**Veredicto:** **La solución más pragmática para el contexto académico.** El modelo ya funciona, la PC tiene RAM suficiente, y Cloudflare Tunnel ofrece una URL pública permanente y gratuita.

---

## 3. Tabla Comparativa Resumida

| Plataforma | RAM disponible | Modelo viable | Costo | Dificultad | Recomendación |
|------------|---------------|---------------|-------|------------|---------------|
| Render | 512 MB (gratis) | ❌ | $25/mes | Baja | Solo si pagas |
| Railway | ~2 GB (crédito) | ⚠️ | ~$10/mes | Baja | Temporal |
| Fly.io | 256 MB (gratis) | ❌ | ~$15/mes | Media | Solo si pagas |
| Koyeb | 512 MB | ❌ | $8/mes | Baja | Descartado |
| **HuggingFace** | **16 GB** | **✅** | **$0** | Media | **✅ Mejor opción cloud gratuita** |
| Oracle Cloud | 24 GB | ✅ | $0 | Alta | ✅ Mejor largo plazo |
| Google Cloud | 0.6 GB (free) | ❌ | $30+/mes | Media | Solo con crédito |
| AWS | 1 GB (free) | ❌ | $16/mes | Alta | Descartado |
| **Cloudflare Tunnel** | **PC local (16 GB)** | **✅** | **$0** | Baja | **✅ Mejor para demo académica** |
| ngrok | PC local (16 GB) | ✅ | $0-8/mes | Muy baja | ✅ Prueba de concepto |

---

## 4. Conclusión y Recomendaciones

### Mejor opción gratuita en la nube
**Hugging Face Spaces (Docker)**  
16 GB RAM, 50 GB almacenamiento, $0. Soporta FastAPI via Docker. El modelo entra con margen. Ideal para portfolios y demos académicas.

### Mejor opción académica / demostración
**Cloudflare Tunnel + Backend Local**  
El backend ya funciona perfectamente en local con el modelo cargado. Cloudflare Tunnel expone una URL HTTPS pública y permanente sin costo. No depende de límites de RAM de servicios externos.

### Mejor opción para producción real
**Oracle Cloud Always Free (ARM)**  
24 GB RAM permanentes y gratuitos. Requiere configuración de VM Linux, pero es la única opción verdaderamente gratuita y estable a largo plazo.

### Mejor opción si se acepta pagar
**Railway o Render ($10-25/mes)**  
Deploy simple desde GitHub, gestión automática, HTTPS incluido.

---

## 5. Decisión Final para Este Proyecto

**Estrategia híbrida adoptada:**

1. **Frontend:** Vercel (ya desplegado) ✅
2. **Backend:** Cloudflare Tunnel sobre PC local como solución primaria
3. **Alternativa cloud:** Hugging Face Spaces (Docker) como opción secundaria documentada

**Justificación académica:**

El modelo de 1.5 GB es demasiado grande para los planes gratuitos de los servicios cloud convencionales. Forzar el despliegue en un servicio con RAM insuficiente resultaría en crashes o en la necesidad de reducir el modelo (perdiendo calidad).

La solución con Cloudflare Tunnel es:
- Técnicamente correcta
- Académicamente defendible
- Completamente gratuita
- Demuestra comprensión de las limitaciones reales de ML en producción
- Muestra capacidad de diseñar soluciones alternativas profesionales

> No es un fracaso técnico. Es una decisión arquitectónica fundamentada en restricciones reales de recursos, que cualquier ingeniero de datos enfrentaría al desplegar modelos grandes.
