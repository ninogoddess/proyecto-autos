import { Settings2, Loader2, Calculator, AlertTriangle } from 'lucide-react';
import SearchableSelect from './SearchableSelect';
import { useVehicleForm } from '../hooks/useVehicleForm';
import { TRANSLATIONS, AVAILABLE_YEARS } from '../constants/translations';

/**
 * Formulario de predicción de precios.
 * Usa el hook useVehicleForm para manejo de estado y validación.
 */
export default function PredictionForm({ options, optionsLoading, optionsError, onSubmit, loading, onRetryOptions }) {
  const {
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
  } = useVehicleForm(options);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate() || loading) return;
    onSubmit(buildPayload());
  };

  const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);

  // Estado de carga de opciones
  if (optionsLoading) {
    return (
      <section className="glass-card form-section">
        <div className="loading-state" style={{ minHeight: '300px' }}>
          <Loader2 className="spinner" size={48} />
          <p className="loading-text">Cargando opciones del formulario...</p>
        </div>
      </section>
    );
  }

  if (optionsError) {
    return (
      <section className="glass-card form-section">
        <div className="error-state">
          <AlertTriangle size={48} color="var(--danger)" />
          <p style={{ color: 'var(--danger)', marginTop: '1rem' }}>{optionsError}</p>
          <button className="btn-submit" onClick={onRetryOptions} style={{ marginTop: '1rem', maxWidth: '200px' }}>
            Reintentar
          </button>
        </div>
      </section>
    );
  }

  return (
    <section className="glass-card form-section">
      <h2 className="card-title">
        <Settings2 size={24} color="var(--primary)" />
        Datos del Vehículo
      </h2>

      {/* Warnings */}
      {warnings.length > 0 && (
        <div className="warning-banner">
          {warnings.map((w, i) => (
            <div key={i} className="warning-item">
              <AlertTriangle size={16} />
              <span>{w}</span>
            </div>
          ))}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Marca */}
        <div className="form-group">
          <label className="form-label" htmlFor="manufacturer">Marca</label>
          <select
            id="manufacturer"
            name="manufacturer"
            className="form-select"
            value={formData.manufacturer}
            onChange={handleChange}
          >
            <option value="">Seleccione marca...</option>
            {options?.manufacturers?.map(m => (
              <option key={m} value={m}>{capitalize(m)}</option>
            ))}
            <option value="__other__">Otro (no está en la lista)</option>
          </select>
          {formData.manufacturer === '__other__' && (
            <input
              type="text"
              className="form-input"
              placeholder="Ingresa la marca..."
              value={customManufacturer}
              onChange={(e) => setCustomManufacturer(e.target.value)}
              style={{ marginTop: '8px' }}
              aria-label="Marca personalizada"
            />
          )}
          {errors.manufacturer && <span className="form-error">{errors.manufacturer}</span>}
        </div>

        {/* Modelo */}
        <div className="form-group">
          <label className="form-label" htmlFor="model">Modelo</label>
          {formData.manufacturer && formData.manufacturer !== '__other__' ? (
            <>
              <SearchableSelect
                id="model"
                name="model"
                options={availableModels}
                value={formData.model}
                onChange={handleChange}
                placeholder="Busca o selecciona modelo..."
                includeOther={true}
                otherLabel="Otro (no está en la lista)"
              />
              {formData.model === '__other__' && (
                <input
                  type="text"
                  className="form-input"
                  placeholder="Ingresa el modelo..."
                  value={customModel}
                  onChange={(e) => setCustomModel(e.target.value)}
                  style={{ marginTop: '8px' }}
                  aria-label="Modelo personalizado"
                />
              )}
            </>
          ) : formData.manufacturer === '__other__' ? (
            <input
              type="text"
              id="model"
              name="model"
              className="form-input"
              placeholder="Ingresa el modelo..."
              value={customModel}
              onChange={(e) => {
                setCustomModel(e.target.value);
                setFormData(prev => ({ ...prev, model: '__other__' }));
              }}
              aria-label="Modelo personalizado"
            />
          ) : (
            <select id="model" name="model" className="form-select" disabled>
              <option value="">Primero selecciona una marca...</option>
            </select>
          )}
          {errors.model && <span className="form-error">{errors.model}</span>}
        </div>

        {/* Año */}
        <div className="form-group">
          <label className="form-label" htmlFor="year">Año</label>
          <select
            id="year"
            name="year"
            className="form-select"
            value={formData.year}
            onChange={handleChange}
          >
            <option value="">Seleccione año...</option>
            {AVAILABLE_YEARS.map(y => (
              <option key={y} value={y}>{y}</option>
            ))}
          </select>
          {errors.year && <span className="form-error">{errors.year}</span>}
        </div>

        {/* Kilometraje */}
        <div className="form-group">
          <label className="form-label" htmlFor="odometer">Kilometraje</label>
          <input
            type="number"
            id="odometer"
            name="odometer"
            className="form-input"
            placeholder="Ej: 45000"
            min="1"
            max="299999"
            value={formData.odometer}
            onChange={handleChange}
          />
          {errors.odometer && <span className="form-error">{errors.odometer}</span>}
        </div>

        {/* Combustible */}
        <div className="form-group">
          <label className="form-label" htmlFor="fuel">Combustible</label>
          <select
            id="fuel"
            name="fuel"
            className="form-select"
            value={formData.fuel}
            onChange={handleChange}
          >
            {options?.fuels?.map(f => (
              <option key={f} value={f}>{TRANSLATIONS.fuels[f] || f}</option>
            ))}
          </select>
          {errors.fuel && <span className="form-error">{errors.fuel}</span>}
        </div>

        {/* Transmisión */}
        <div className="form-group">
          <label className="form-label" htmlFor="transmission">Transmisión</label>
          <select
            id="transmission"
            name="transmission"
            className="form-select"
            value={formData.transmission}
            onChange={handleChange}
          >
            {options?.transmissions?.map(t => (
              <option key={t} value={t}>{TRANSLATIONS.transmissions[t] || t}</option>
            ))}
          </select>
          {errors.transmission && <span className="form-error">{errors.transmission}</span>}
        </div>

        {/* Tipo de vehículo */}
        <div className="form-group">
          <label className="form-label" htmlFor="type">Tipo de Vehículo</label>
          <select
            id="type"
            name="type"
            className="form-select"
            value={formData.type}
            onChange={handleChange}
          >
            <option value="">Seleccione tipo...</option>
            {options?.types?.map(t => (
              <option key={t} value={t}>{TRANSLATIONS.types[t] || t}</option>
            ))}
          </select>
          {errors.type && <span className="form-error">{errors.type}</span>}
        </div>

        {/* Condición */}
        <div className="form-group">
          <label className="form-label" htmlFor="condition">Condición</label>
          <select
            id="condition"
            name="condition"
            className="form-select"
            value={formData.condition}
            onChange={handleChange}
          >
            {options?.conditions?.map(c => (
              <option key={c} value={c}>{TRANSLATIONS.conditions[c] || c}</option>
            ))}
          </select>
        </div>

        {/* Botón submit */}
        <button
          type="submit"
          className="btn-submit"
          disabled={loading}
        >
          {loading ? (
            <>
              <Loader2 className="spinner" size={24} />
              Calculando...
            </>
          ) : (
            <>
              <Calculator size={24} />
              Estimar Precio
            </>
          )}
        </button>
      </form>
    </section>
  );
}
