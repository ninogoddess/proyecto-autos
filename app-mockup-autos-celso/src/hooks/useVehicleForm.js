/**
 * Hook personalizado para manejo del formulario de predicción.
 * Encapsula el estado, validación y construcción del payload.
 * Los componentes solo consumen la interfaz expuesta.
 */

import { useState, useEffect } from 'react';
import { FORM_DEFAULTS } from '../constants/translations';

export function useVehicleForm(options) {
  const [formData, setFormData] = useState(FORM_DEFAULTS);
  const [customManufacturer, setCustomManufacturer] = useState('');
  const [customModel, setCustomModel] = useState('');
  const [errors, setErrors] = useState({});
  const [warnings, setWarnings] = useState([]);
  const [availableModels, setAvailableModels] = useState([]);

  // Actualizar modelos disponibles cuando cambia la marca
  useEffect(() => {
    if (
      formData.manufacturer &&
      formData.manufacturer !== '__other__' &&
      options?.models_by_manufacturer
    ) {
      const models = options.models_by_manufacturer[formData.manufacturer] || [];
      setAvailableModels(models);
    } else {
      setAvailableModels([]);
    }
  }, [formData.manufacturer, options]);

  // Actualizar warnings cuando cambia marca o modelo
  useEffect(() => {
    const newWarnings = [];
    if (formData.manufacturer === '__other__') {
      newWarnings.push(
        'Marca no encontrada en los datos históricos. La predicción podría ser menos precisa.'
      );
    }
    if (formData.model === '__other__') {
      newWarnings.push(
        'Modelo no encontrado en los datos históricos. La predicción podría ser menos precisa.'
      );
    }
    setWarnings(newWarnings);
  }, [formData.manufacturer, formData.model]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === 'manufacturer') {
      // Resetear modelo al cambiar marca
      setFormData(prev => ({ ...prev, manufacturer: value, model: '' }));
      setCustomModel('');
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }

    // Limpiar error del campo modificado
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.manufacturer) {
      newErrors.manufacturer = 'Selecciona una marca';
    } else if (formData.manufacturer === '__other__' && !customManufacturer.trim()) {
      newErrors.manufacturer = 'Ingresa el nombre de la marca';
    }

    if (!formData.model) {
      newErrors.model = 'Selecciona o ingresa un modelo';
    } else if (formData.model === '__other__' && !customModel.trim()) {
      newErrors.model = 'Ingresa el nombre del modelo';
    }

    if (!formData.year) {
      newErrors.year = 'Selecciona un año';
    }

    if (!formData.odometer) {
      newErrors.odometer = 'Ingresa el kilometraje';
    } else {
      const km = parseInt(formData.odometer);
      if (isNaN(km) || km < 1 || km > 299999) {
        newErrors.odometer = 'Kilometraje debe estar entre 1 y 299.999';
      }
    }

    if (!formData.fuel) newErrors.fuel = 'Selecciona tipo de combustible';
    if (!formData.transmission) newErrors.transmission = 'Selecciona transmisión';
    if (!formData.type) newErrors.type = 'Selecciona tipo de vehículo';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /** Construye el payload para el backend a partir del estado del formulario */
  const buildPayload = () => ({
    manufacturer:
      formData.manufacturer === '__other__'
        ? customManufacturer.trim().toLowerCase()
        : formData.manufacturer,
    model:
      formData.model === '__other__'
        ? customModel.trim().toLowerCase()
        : formData.model,
    year: parseInt(formData.year),
    odometer: parseInt(formData.odometer),
    fuel: formData.fuel,
    transmission: formData.transmission,
    type: formData.type,
    condition: formData.condition,
  });

  return {
    formData,
    customManufacturer,
    customModel,
    errors,
    warnings,
    availableModels,
    handleChange,
    setCustomManufacturer,
    setCustomModel,
    validate,
    buildPayload,
  };
}
