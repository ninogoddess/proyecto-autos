import { useState, useRef, useEffect } from 'react';
import { Search, ChevronDown, X } from 'lucide-react';

/**
 * Select con barra de búsqueda integrada.
 * Muestra opciones filtradas mientras el usuario escribe.
 * Incluye nota informativa sobre la cantidad de opciones disponibles.
 */
export default function SearchableSelect({
  id,
  name,
  options = [],
  value,
  onChange,
  placeholder = 'Seleccione...',
  disabled = false,
  includeOther = false,
  otherLabel = 'Otro (no está en la lista)',
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const containerRef = useRef(null);
  const inputRef = useRef(null);

  // Filtrar opciones por búsqueda
  const filtered = search
    ? options.filter(opt => opt.toLowerCase().includes(search.toLowerCase()))
    : options;

  // Limitar opciones visibles para rendimiento
  const visibleOptions = filtered.slice(0, 100);
  const hasMore = filtered.length > 100;

  // Cerrar al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (val) => {
    onChange({ target: { name, value: val } });
    setIsOpen(false);
    setSearch('');
  };

  const handleClear = (e) => {
    e.stopPropagation();
    onChange({ target: { name, value: '' } });
    setSearch('');
  };

  const toggleOpen = () => {
    if (disabled) return;
    setIsOpen(!isOpen);
    if (!isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  };

  return (
    <div className="searchable-select" ref={containerRef}>
      {/* Trigger */}
      <button
        type="button"
        className={`searchable-select-trigger ${isOpen ? 'open' : ''} ${disabled ? 'disabled' : ''}`}
        onClick={toggleOpen}
        disabled={disabled}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        id={id}
      >
        <span className={value && value !== '__other__' ? 'selected-value' : 'placeholder-text'}>
          {value && value !== '__other__' ? value : placeholder}
        </span>
        <div className="trigger-icons">
          {value && !disabled && (
            <X size={14} className="clear-icon" onClick={handleClear} />
          )}
          <ChevronDown size={16} className={`chevron ${isOpen ? 'rotated' : ''}`} />
        </div>
      </button>

      {/* Dropdown */}
      {isOpen && (
        <div className="searchable-select-dropdown">
          {/* Barra de búsqueda */}
          <div className="search-input-wrapper">
            <Search size={14} className="search-icon" />
            <input
              ref={inputRef}
              type="text"
              className="search-input"
              placeholder="Buscar modelo..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              aria-label="Buscar en opciones"
            />
          </div>

          {/* Nota informativa */}
          <div className="options-info">
            {search
              ? `${filtered.length} resultado${filtered.length !== 1 ? 's' : ''}`
              : `${options.length} modelos disponibles — escribe para filtrar`
            }
          </div>

          {/* Lista de opciones */}
          <ul className="options-list" role="listbox">
            {visibleOptions.map(opt => (
              <li
                key={opt}
                className={`option-item ${opt === value ? 'selected' : ''}`}
                onClick={() => handleSelect(opt)}
                role="option"
                aria-selected={opt === value}
              >
                {opt}
              </li>
            ))}

            {hasMore && (
              <li className="option-item more-indicator">
                ... {filtered.length - 100} más — refina tu búsqueda
              </li>
            )}

            {filtered.length === 0 && (
              <li className="option-item no-results">
                No se encontraron resultados
              </li>
            )}

            {/* Opción "Otro" */}
            {includeOther && (
              <li
                className={`option-item option-other ${value === '__other__' ? 'selected' : ''}`}
                onClick={() => handleSelect('__other__')}
                role="option"
              >
                {otherLabel}
              </li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
