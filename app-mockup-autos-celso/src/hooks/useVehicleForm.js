/**
 * Hook para el formulario de predicción.
 * Auto-detecta el tipo de vehículo desde el modelo seleccionado.
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
  const [detectedType, setDetectedType] = useState(null);

  // Modelos disponibles según marca
  useEffect(() => {
    if (formData.manufacturer && formData.manufacturer !== '__other__' && options?.models_by_manufacturer) {
      setAvailableModels(options.models_by_manufacturer[formData.manufacturer] || []);
    } else {
      setAvailableModels([]);
    }
  }, [formData.manufacturer, options]);

  // Auto-detectar tipo de vehículo cuando cambia el modelo
  useEffect(() => {
    const modelName = formData.model === '__other__' ? customModel : formData.model;
    if (!modelName || !options?.model_type_map) {
      setDetectedType(null);
      return;
    }
    const type = options.model_type_map[modelName.toLowerCase().trim()];
    setDetectedType(type || null);
    // Actualizar formData.type con el detectado
    if (type) {
      setFormData(prev => ({ ...prev, type }));
    }
  }, [formData.model, customModel, options]);

  // Warnings por marca/modelo "Otro"
  useEffect(() => {
    const newWarnings = [];
    if (formData.manufacturer === '__other__') {
      newWarnings.push('Marca no encontrada en los datos históricos. La predicción podría ser menos precisa.');
    }
    if (formData.model === '__other__') {
      newWarnings.push('Modelo no encontrado en los datos históricos. La predicción podría ser menos precisa.');
    }
    setWarnings(newWarnings);
  }, [formData.manufacturer, formData.model]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'manufacturer') {
      setFormData(prev => ({ ...prev, manufacturer: value, model: '', type: '' }));
      setCustomModel('');
      setDetectedType(null);
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.manufacturer) newErrors.manufacturer = 'Selecciona una marca';
    else if (formData.manufacturer === '__other__' && !customManufacturer.trim())
      newErrors.manufacturer = 'Ingresa el nombre de la marca';

    if (!formData.model) newErrors.model = 'Selecciona o ingresa un modelo';
    else if (formData.model === '__other__' && !customModel.trim())
      newErrors.model = 'Ingresa el nombre del modelo';

    if (!formData.year) newErrors.year = 'Selecciona un año';

    if (!formData.odometer) {
      newErrors.odometer = 'Ingresa el kilometraje';
    } else {
      const km = parseInt(formData.odometer);
      if (isNaN(km) || km < 1 || km > 299999)
        newErrors.odometer = 'Debe estar entre 1 y 299.999';
    }

    if (!formData.fuel) newErrors.fuel = 'Selecciona combustible';
    if (!formData.transmission) newErrors.transmission = 'Selecciona transmisión';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const buildPayload = () => {
    const resolvedModel = formData.model === '__other__' ? customModel.trim().toLowerCase() : formData.model;
    const resolvedType = detectedType || formData.type || 'other';
    return {
      manufacturer: formData.manufacturer === '__other__' ? customManufacturer.trim().toLowerCase() : formData.manufacturer,
      model: resolvedModel,
      year: parseInt(formData.year),
      odometer: parseInt(formData.odometer),
      fuel: formData.fuel,
      transmission: formData.transmission,
      type: resolvedType,
      condition: formData.condition,
    };
  };

  return {
    formData,
    customManufacturer,
    customModel,
    errors,
    warnings,
    availableModels,
    detectedType,
    handleChange,
    setCustomManufacturer,
    setCustomModel,
    validate,
    buildPayload,
  };
}
