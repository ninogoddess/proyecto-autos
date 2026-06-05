import { useState, useEffect } from 'react';
import { Car } from 'lucide-react';
import PredictionForm from './components/PredictionForm';
import ResultPanel from './components/ResultPanel';
import { getOptions, predictPrice } from './services/predictionService';
import './index.css';

/**
 * Componente raíz — orquesta el flujo de predicción.
 * Carga opciones al montar, maneja estado global de la app.
 */
function App() {
  // Estado de opciones del formulario
  const [options, setOptions] = useState(null);
  const [optionsLoading, setOptionsLoading] = useState(true);
  const [optionsError, setOptionsError] = useState(null);

  // Estado de predicción
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Cargar opciones al montar
  useEffect(() => {
    loadOptions();
  }, []);

  const loadOptions = async () => {
    setOptionsLoading(true);
    setOptionsError(null);
    try {
      const data = await getOptions();
      setOptions(data);
    } catch (err) {
      setOptionsError(err.message);
    } finally {
      setOptionsLoading(false);
    }
  };

  // Enviar predicción
  const handleSubmit = async (vehicleData) => {
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const prediction = await predictPrice(vehicleData);
      setResult(prediction);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Reset para nueva consulta
  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-icon">
          <Car size={36} color="var(--primary)" />
        </div>
        <h1>Predicción de Precios de Vehículos</h1>
        <p>Valoración instantánea con modelo de Machine Learning</p>
      </header>

      <main className="dashboard-layout">
        <PredictionForm
          options={options}
          optionsLoading={optionsLoading}
          optionsError={optionsError}
          onSubmit={handleSubmit}
          loading={loading}
          onRetryOptions={loadOptions}
        />

        <ResultPanel
          loading={loading}
          result={result}
          error={error}
          onReset={handleReset}
        />
      </main>
    </div>
  );
}

export default App;
