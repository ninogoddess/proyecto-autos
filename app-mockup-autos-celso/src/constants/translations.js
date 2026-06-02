/**
 * Traducciones de opciones inglés → español para la UI.
 * Los valores internos se envían en inglés al backend.
 * Solo los labels visibles al usuario están en español.
 */

export const TRANSLATIONS = {
  fuels: {
    diesel: 'Diésel',
    electric: 'Eléctrico',
    gas: 'Gasolina',
    hybrid: 'Híbrido',
    other: 'Otro',
  },
  transmissions: {
    automatic: 'Automática',
    manual: 'Manual',
    other: 'Otra',
  },
  types: {
    SUV: 'SUV',
    bus: 'Bus',
    convertible: 'Convertible',
    coupe: 'Coupé',
    hatchback: 'Hatchback',
    'mini-van': 'Minivan',
    offroad: 'Todo terreno',
    other: 'Otro',
    pickup: 'Pickup',
    sedan: 'Sedán',
    truck: 'Camioneta',
    unknown: 'No especificado',
    van: 'Van',
    wagon: 'Station Wagon',
  },
  conditions: {
    excellent: 'Excelente',
    fair: 'Regular',
    good: 'Bueno',
    'like new': 'Como nuevo',
    new: 'Nuevo',
    salvage: 'Salvamento',
    unknown: 'No especificado',
  },
};

/** Años válidos para el formulario (más reciente primero) */
export const AVAILABLE_YEARS = Array.from({ length: 44 }, (_, i) => 2024 - i);

/** Valores iniciales del formulario */
export const FORM_DEFAULTS = {
  manufacturer: '',
  model: '',
  year: '',
  odometer: '',
  fuel: 'gas',
  transmission: 'automatic',
  type: '',
  condition: 'good',
};

/** Mensajes de loading rotativos */
export const LOADING_MESSAGES = [
  'Analizando datos del vehículo...',
  'Consultando modelo predictivo...',
  'Procesando características...',
  'Calculando estimación final...',
];
