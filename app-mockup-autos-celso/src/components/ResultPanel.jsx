import { useState, useEffect } from 'react';
import { Sparkles, DollarSign, Loader2, AlertTriangle, RefreshCw } from 'lucide-react';
import { LOADING_MESSAGES } from '../constants/translations';

/**
 * Panel de resultados con animaciones y estados visuales.
 */
export default function ResultPanel({ loading, result, error, onReset }) {
  const [loadingText, setLoadingText] = useState(LOADING_MESSAGES[0]);
  const [animatedPrice, setAnimatedPrice] = useState(0);
  const [showResult, setShowResult] = useState(false);

  // Rotación de mensajes de carga
  useEffect(() => {
    if (!loading) return;
    let index = 0;
    setLoadingText(LOADING_MESSAGES[0]);
    const interval = setInterval(() => {
      index = (index + 1) % LOADING_MESSAGES.length;
      setLoadingText(LOADING_MESSAGES[index]);
    }, 2000);
    return () => clearInterval(interval);
  }, [loading]);

  // Animación del precio (contador)
  useEffect(() => {
    if (!result) {
      setShowResult(false);
      setAnimatedPrice(0);
      return;
    }

    setShowResult(false);
    const target = result.predicted_price_clp;
    const duration = 1200; // ms
    const steps = 30;
    const increment = target / steps;
    let current = 0;
    let step = 0;

    // Pequeño delay antes de mostrar
    const showTimeout = setTimeout(() => {
      setShowResult(true);
      const interval = setInterval(() => {
        step++;
        current = Math.min(Math.round(increment * step), target);
        setAnimatedPrice(current);
        if (step >= steps) {
          clearInterval(interval);
          setAnimatedPrice(target);
        }
      }, duration / steps);
    }, 200);

    return () => clearTimeout(showTimeout);
  }, [result]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-CL', {
      style: 'currency',
      currency: 'CLP',
      maximumFractionDigits: 0
    }).format(price);
  };

  const formatPriceUSD = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(price);
  };

  // Calcular rango estimado (±10%)
  const getRange = () => {
    if (!result) return null;
    const price = result.predicted_price_clp;
    return {
      min: Math.round(price * 0.9),
      max: Math.round(price * 1.1),
    };
  };

  // Determinar nivel de confianza basado en warnings
  const getConfidence = () => {
    if (!result) return null;
    if (result.warnings.length === 0) return { level: 'Alta', color: 'var(--primary)' };
    if (result.warnings.length === 1) return { level: 'Media', color: 'var(--warning)' };
    return { level: 'Baja', color: 'var(--danger)' };
  };

  return (
    <section className="glass-card result-section">
      <h2 className="card-title">
        <Sparkles size={24} color="var(--warning)" />
        Resultado de Estimación
      </h2>

      <div className="result-container">
        {/* Estado vacío */}
        {!loading && !result && !error && (
          <div className="result-placeholder fade-in">
            <DollarSign size={64} />
            <p>Ingresa los datos del vehículo y haz clic en "Estimar Precio" para ver la valoración.</p>
          </div>
        )}

        {/* Estado de carga */}
        {loading && (
          <div className="loading-state fade-in">
            <Loader2 className="spinner" size={64} />
            <p className="loading-text">{loadingText}</p>
          </div>
        )}

        {/* Error */}
        {!loading && error && (
          <div className="error-state fade-in">
            <AlertTriangle size={48} color="var(--danger)" />
            <p className="error-text">{error}</p>
            <button className="btn-retry" onClick={onReset}>
              <RefreshCw size={16} />
              Intentar nuevamente
            </button>
          </div>
        )}

        {/* Resultado exitoso */}
        {!loading && result && showResult && (
          <div className="price-result fade-in">
            {/* Precio principal */}
            <div className="price-label">Precio Estimado (CLP)</div>
            <div className="price-value">{formatPrice(animatedPrice)}</div>

            {/* Precio USD */}
            <div className="price-usd">
              ≈ {formatPriceUSD(result.predicted_price_usd)}
            </div>

            {/* Confianza */}
            {getConfidence() && (
              <div className="confidence-badge" style={{ borderColor: getConfidence().color }}>
                <span style={{ color: getConfidence().color }}>●</span>
                Confianza: {getConfidence().level}
              </div>
            )}

            {/* Rango estimado */}
            {getRange() && (
              <div className="price-range">
                Rango esperado: {formatPrice(getRange().min)} — {formatPrice(getRange().max)}
              </div>
            )}

            {/* Warnings del modelo */}
            {result.warnings.length > 0 && (
              <div className="result-warnings">
                {result.warnings.map((w, i) => (
                  <div key={i} className="warning-item">
                    <AlertTriangle size={14} />
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Detalles del vehículo */}
            <div className="price-details">
              <div className="detail-row">
                <span className="detail-label">Marca/Modelo:</span>
                <span className="detail-value">
                  {result.vehicle_data.manufacturer} {result.vehicle_data.model}
                </span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Año:</span>
                <span className="detail-value">{result.vehicle_data.year}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Kilometraje:</span>
                <span className="detail-value">
                  {new Intl.NumberFormat('es-CL').format(result.vehicle_data.odometer)} km
                </span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Combustible:</span>
                <span className="detail-value">{result.vehicle_data.fuel}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Transmisión:</span>
                <span className="detail-value">{result.vehicle_data.transmission}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Tipo:</span>
                <span className="detail-value">{result.vehicle_data.type}</span>
              </div>
            </div>

            {/* Botón nueva consulta */}
            <button className="btn-new-query" onClick={onReset}>
              <RefreshCw size={16} />
              Nueva consulta
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
