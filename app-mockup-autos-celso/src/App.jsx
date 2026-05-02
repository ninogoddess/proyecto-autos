import { useState, useEffect } from 'react';
import { Car, Settings2, Calendar, Gauge, Sparkles, Loader2, DollarSign, Calculator } from 'lucide-react';
import './index.css';

const MARCAS_MODELOS = {
  Toyota: ['Corolla', 'Yaris', 'Hilux', 'RAV4'],
  Chevrolet: ['Spark', 'Sail', 'Tracker', 'Colorado'],
  Hyundai: ['Accent', 'Tucson', 'Santa Fe', 'Elantra'],
  Kia: ['Rio', 'Sportage', 'Sorento', 'Cerato'],
  Nissan: ['Versa', 'Sentra', 'Kicks', 'Navara'],
  Ford: ['Fiesta', 'Focus', 'Ranger', 'Escape']
};

const AJUSTES_MARCA = {
  Toyota: 1000000,
  Hyundai: 500000,
  Kia: 400000,
  Chevrolet: 200000,
  Nissan: 300000,
  Ford: 350000
};

const LOADING_MESSAGES = [
  "Analizando datos del vehículo...",
  "Consultando mercado actual...",
  "Aplicando modelo predictivo...",
  "Calculando estimación final..."
];

function App() {
  const [formData, setFormData] = useState({
    marca: '',
    modelo: '',
    anio: '',
    km: ''
  });
  
  const [errors, setErrors] = useState({});
  const [modelosDisponibles, setModelosDisponibles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState("");
  const [resultado, setResultado] = useState(null);

  const currentYear = new Date().getFullYear();
  const anios = Array.from({ length: 25 }, (_, i) => currentYear - i); // 2000 to current

  useEffect(() => {
    if (formData.marca) {
      setModelosDisponibles(MARCAS_MODELOS[formData.marca] || []);
      setFormData(prev => ({ ...prev, modelo: '' }));
    } else {
      setModelosDisponibles([]);
    }
  }, [formData.marca]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.marca) newErrors.marca = "Selecciona una marca";
    if (!formData.modelo) newErrors.modelo = "Selecciona un modelo";
    if (!formData.anio) newErrors.anio = "Selecciona un año";
    
    if (!formData.km) {
      newErrors.km = "Ingresa el kilometraje";
    } else if (isNaN(formData.km) || parseInt(formData.km) < 0) {
      newErrors.km = "Ingresa un kilometraje válido";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const calcularPrecio = () => {
    const km = parseInt(formData.km);
    const anio = parseInt(formData.anio);
    const marca = formData.marca;

    let precio = 3000000; // Precio base
    
    // Ajuste por año (más nuevo -> más caro)
    precio += (anio - 2000) * 180000;
    
    // Ajuste por km (más km -> más barato)
    precio -= (km * 8);
    
    // Ajuste por marca
    precio += (AJUSTES_MARCA[marca] || 0);

    // Variación aleatoria ±5%
    const variacion = 0.95 + (Math.random() * 0.1);
    precio *= variacion;

    // Nunca menor a 0 (aunque con esta lógica base y años 2000+ es difícil, pero por seguridad)
    precio = Math.max(500000, precio); // Mínimo absoluto 500k

    return Math.round(precio);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    setResultado(null);
    
    // Simular carga dinámica
    let messageIndex = 0;
    setLoadingText(LOADING_MESSAGES[0]);
    
    const interval = setInterval(() => {
      messageIndex++;
      if (messageIndex < LOADING_MESSAGES.length) {
        setLoadingText(LOADING_MESSAGES[messageIndex]);
      }
    }, 600); // Cambia el texto cada 600ms

    // Tiempo total de carga entre 1.5s y 2.5s
    const loadTime = Math.floor(Math.random() * 1000) + 1500;

    setTimeout(() => {
      clearInterval(interval);
      const precioEstimado = calcularPrecio();
      setResultado(precioEstimado);
      setLoading(false);
    }, loadTime);
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-CL', {
      style: 'currency',
      currency: 'CLP',
      maximumFractionDigits: 0
    }).format(price);
  };

  return (
    <>
      <div className="app-container">
        <header className="header">
          {/* Espacio para Logo */}
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
             <Car size={48} color="var(--primary)" />
          </div>
          <h1>Predicción de Precios</h1>
          <p>Valora tu vehículo al instante con nuestro modelo avanzado de mercado.</p>
        </header>

        <main className="dashboard-layout">
          {/* Formulario */}
          <section className="glass-card form-section">
            <h2 className="card-title">
              <Settings2 size={24} color="var(--primary)" />
              Datos del Vehículo
            </h2>

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label" htmlFor="marca">Marca</label>
                <select 
                  id="marca"
                  name="marca" 
                  className="form-select"
                  value={formData.marca}
                  onChange={handleChange}
                >
                  <option value="">Seleccione marca...</option>
                  {Object.keys(MARCAS_MODELOS).map(marca => (
                    <option key={marca} value={marca}>{marca}</option>
                  ))}
                </select>
                {errors.marca && <span className="form-error">{errors.marca}</span>}
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="modelo">Modelo</label>
                <select 
                  id="modelo"
                  name="modelo" 
                  className="form-select"
                  value={formData.modelo}
                  onChange={handleChange}
                  disabled={!formData.marca}
                >
                  <option value="">Seleccione modelo...</option>
                  {modelosDisponibles.map(modelo => (
                    <option key={modelo} value={modelo}>{modelo}</option>
                  ))}
                </select>
                {errors.modelo && <span className="form-error">{errors.modelo}</span>}
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="anio">Año</label>
                <div style={{ position: 'relative' }}>
                  <select 
                    id="anio"
                    name="anio" 
                    className="form-select"
                    value={formData.anio}
                    onChange={handleChange}
                  >
                    <option value="">Seleccione año...</option>
                    {anios.map(anio => (
                      <option key={anio} value={anio}>{anio}</option>
                    ))}
                  </select>
                </div>
                {errors.anio && <span className="form-error">{errors.anio}</span>}
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="km">Kilometraje</label>
                <div style={{ position: 'relative' }}>
                  <input 
                    type="number" 
                    id="km"
                    name="km"
                    className="form-input"
                    placeholder="Ej: 120000"
                    value={formData.km}
                    onChange={handleChange}
                  />
                </div>
                {errors.km && <span className="form-error">{errors.km}</span>}
              </div>

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

          {/* Resultados */}
          <section className="glass-card result-section">
            
            <h2 className="card-title">
              <Sparkles size={24} color="var(--warning)" />
              Resultado de Estimación
            </h2>

            <div className="result-container">
              {!loading && resultado === null && (
                <div className="result-placeholder">
                  <DollarSign size={64} />
                  <p>Ingresa los datos del vehículo y haz clic en "Estimar Precio" para ver la valoración del mercado.</p>
                </div>
              )}

              {loading && (
                <div className="loading-state">
                  <Loader2 className="spinner" size={64} />
                  <p className="loading-text">{loadingText}</p>
                </div>
              )}

              {!loading && resultado !== null && (
                <div className="price-result">
                  <div className="price-label">Precio Estimado (CLP)</div>
                  <div className="price-value">{formatPrice(resultado)}</div>
                  
                  <div className="price-details">
                    <div className="detail-row">
                      <span className="detail-label">Marca/Modelo:</span>
                      <span className="detail-value">{formData.marca} {formData.modelo}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Año:</span>
                      <span className="detail-value">{formData.anio}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Kilometraje:</span>
                      <span className="detail-value">{new Intl.NumberFormat('es-CL').format(formData.km)} km</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </section>
        </main>
      </div>
    </>
  );
}

export default App;
