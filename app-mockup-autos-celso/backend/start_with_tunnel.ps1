# start_with_tunnel.ps1
# Inicia el backend FastAPI y opcionalmente el tunel de Cloudflare
# Uso: .\start_with_tunnel.ps1 [-WithTunnel]
#
# REQUISITOS:
#   - Entorno virtual activado (servidor-autos)
#   - cloudflared instalado (para el tunel)

param(
    [switch]$WithTunnel = $false
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Backend - Prediccion de Precios" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Verificar que el entorno virtual esta activo
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "ERROR: Python no encontrado. Activa el entorno virtual primero:" -ForegroundColor Red
    Write-Host "  .\servidor-autos\Scripts\Activate.ps1" -ForegroundColor Yellow
    exit 1
}

# Verificar que fastapi esta instalado
$fastapiCheck = python -c "import fastapi" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: FastAPI no instalado. Ejecuta:" -ForegroundColor Red
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Iniciando backend en http://localhost:8000" -ForegroundColor Green
Write-Host "Swagger UI: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

if ($WithTunnel) {
    # Iniciar backend en background y tunel en foreground
    Write-Host "Modo tunel activado. Iniciando backend en segundo plano..." -ForegroundColor Cyan
    $backendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
    }

    Write-Host "Esperando 35s para que el modelo cargue..." -ForegroundColor Yellow
    Start-Sleep -Seconds 35

    Write-Host ""
    Write-Host "Iniciando tunel Cloudflare..." -ForegroundColor Cyan
    Write-Host "Copia la URL HTTPS generada y configurala en Vercel como VITE_API_URL" -ForegroundColor Yellow
    Write-Host ""
    cloudflared tunnel --url http://localhost:8000
} else {
    # Solo backend
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}
