/**
 * Servicio centralizado para comunicación con la API de predicción.
 * Todas las llamadas HTTP pasan por aquí — los componentes no usan Axios directamente.
 */

import axios from 'axios';

// URL base desde variable de entorno (soporta dev, staging, producción)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000, // 15 segundos
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Obtiene las opciones válidas para el formulario desde el backend.
 * @returns {Promise<Object>} Opciones: manufacturers, models, fuels, etc.
 */
export async function getOptions() {
  try {
    const response = await api.get('/api/v1/options');
    return response.data;
  } catch (error) {
    throw parseError(error);
  }
}

/**
 * Envía datos del vehículo y obtiene la predicción de precio.
 * @param {Object} vehicleData - Datos del vehículo según schema del backend
 * @returns {Promise<Object>} Predicción: predicted_price_usd, predicted_price_clp, warnings
 */
export async function predictPrice(vehicleData) {
  try {
    const response = await api.post('/api/v1/predict', vehicleData);
    return response.data;
  } catch (error) {
    throw parseError(error);
  }
}

/**
 * Verifica el estado del backend.
 * @returns {Promise<Object>} Health: status, model_loaded, version
 */
export async function checkHealth() {
  try {
    const response = await api.get('/api/v1/health');
    return response.data;
  } catch (error) {
    throw parseError(error);
  }
}

/**
 * Parsea errores de Axios en mensajes legibles para el usuario.
 * Nunca expone detalles técnicos internos.
 */
function parseError(error) {
  if (error.response) {
    // El servidor respondió con un código de error
    const status = error.response.status;
    const data = error.response.data;

    if (status === 422) {
      // Error de validación
      const details = data.detail || [];
      const messages = details.map(d => `${d.field}: ${d.message}`).join('. ');
      return new Error(messages || 'Datos inválidos. Verifica los campos del formulario.');
    }
    if (status === 503) {
      return new Error('El servicio de predicción no está disponible en este momento. Intenta más tarde.');
    }
    if (status >= 500) {
      return new Error('Error interno del servidor. Intenta nuevamente en unos momentos.');
    }
    return new Error(data.detail || 'Error inesperado del servidor.');
  }

  if (error.request) {
    // No hubo respuesta (timeout, red caída, backend apagado)
    if (error.code === 'ECONNABORTED') {
      return new Error('La solicitud tardó demasiado. Verifica tu conexión e intenta nuevamente.');
    }
    return new Error('No se pudo conectar con el servidor. Verifica que el backend esté activo.');
  }

  // Error de configuración
  return new Error('Error inesperado. Intenta nuevamente.');
}
