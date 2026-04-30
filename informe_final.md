# Informe Técnico: Proyecto de Ciencia de Datos - Predicción de Precios de Vehículos Usados

## I. Introducción

En el dinámico y caótico mercado de vehículos usados, la correcta tasación de un automóvil representa un desafío crítico. Determinar un precio justo a menudo depende de criterios altamente subjetivos o herramientas precarias, resultando en ineficiencias que afectan tanto a empresas automotoras como a usuarios particulares. 

Este proyecto aborda la problemática desde una rigurosa perspectiva de ciencia de datos, buscando domesticar el caos subyacente en el mercado automotriz a través del aprendizaje automático. El objetivo último es desentrañar cómo las diversas características estructurales y técnicas de un vehículo esculpen su valor monetario, proponiendo un modelo predictivo robusto, coherente y escalable.

## II. Problema, Objetivos y KPIs

### 2.1 Problema
La determinación del precio de un vehículo usado carece de un estándar objetivo, originando inconsistencias, sobrevaloraciones o subvaloraciones en las transacciones del mercado. Surge así la pregunta analítica: **¿En qué medida es posible estimar el precio de un vehículo usado a partir de sus características estructurales y técnicas, tales como año, marca, modelo, kilometraje y tipo de combustible?**

### 2.2 Objetivo General
Desarrollar un modelo de regresión capaz de estimar con precisión el precio de vehículos usados a partir de sus características, empleando técnicas avanzadas de procesamiento de datos y aprendizaje automático.

### 2.3 Objetivos Específicos
1. **Realizar un proceso de limpieza y preprocesamiento** del dataset, abordando nulos, ruido y variables irrelevantes.
2. **Analizar exploratoriamente los datos (EDA)** para develar patrones, distribuciones y relaciones latentes.
3. **Construir y evaluar múltiples modelos de regresión**, identificando aquel que logre la mayor capacidad de abstracción y predicción.
4. **Diseñar una interfaz simple o prototipo** que permita la interacción intuitiva del usuario final para la tasación.

### 2.4 KPIs
- **Precisión de estimación:** Capacidad de entregar precios cercanos al valor real del mercado (medido a través de métricas como RMSE y R²).
- **Consistencia de resultados:** Tasaciones similares frente a vehículos de características análogas.
- **Usabilidad de la solución:** Simplicidad en la captura de datos y claridad en la estimación.
- **Valor práctico para el negocio:** Viabilidad del sistema para ser adoptado por tasadores, plataformas o entidades como el SII.
(PONEER KPIS CON NUMEROS Y SI FUNCIONA )
## III. Antecedentes y Fuentes

El mercado automotriz ha operado históricamente basado en heurísticas y experiencia humana. La digitalización ha permitido el registro masivo de transacciones, generando vastos océanos de datos estructurados y semi-estructurados. 

La fuente de información principal para este proyecto es el dataset **"Craigslist Cars & Trucks Data"**, albergado en la plataforma de ciencia de datos Kaggle. Este repositorio consolida miles de publicaciones reales de venta de vehículos en distintas regiones, reflejando el comportamiento orgánico y, a veces, errático de la oferta automotriz. (PONER LINK DEL DATA SET Y MAS FUUENTES TEORICAS TIPO MARCO)

## IV. Requisitos del Proyecto

### Funcionales
- El sistema debe permitir el **entrenamiento de múltiples modelos** predictivos para comparar sus rendimientos.
- Se exige la **generación de métricas** claras y automatizadas tras el entrenamiento de cada algoritmo.
- Debe existir un mecanismo de **almacenamiento estructurado** tanto para los datos procesados como para los modelos entrenados (.pkl).

### No funcionales
- **Escalabilidad:** El pipeline de procesamiento debe ser capaz de absorber nuevos volúmenes de datos sin colapsar.
- **Mantenibilidad:** La arquitectura de código debe ser modular, permitiendo aislar el preprocesamiento, el entrenamiento de cada modelo y la evaluación.
- **Tiempo de ejecución razonable:** El entrenamiento de los algoritmos y la inferencia deben ejecutarse en un marco temporal que no obstaculice el flujo de trabajo analítico.

## V. Dataset

### Descripción
El dataset "Craigslist Cars & Trucks Data" cuenta en su origen con:
- **Registros:** 426,880
- **Variables:** 26

Contiene atributos esenciales como precio (`price`), año (`year`), fabricante (`manufacturer`), modelo (`model`), kilometraje (`odometer`), y ubicación geográfica (`lat`, `long`), además de descriptores categóricos (`condition`, `fuel`, `transmission`, entre otros).

### Fuente
Obtenido desde Kaggle:
https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data

### Justificación
La pertinencia del dataset es absoluta: contiene directamente nuestra variable objetivo (`price`) y una pluralidad de variables independientes, permitiendo que un algoritmo establezca la topología multidimensional que relaciona las cualidades físicas de un automóvil con su valor monetario temporal.

## VI. Metodología

El proyecto se alinea bajo los principios de la metodología **CRISP-DM**, o Cross-Industry Standard Process for Data Mining:
1. **Business Understanding:** Definición del problema de tasación inconsistente.
2. **Data Understanding:** Análisis exploratorio inicial (EDA) para identificar completitud, outliers y correlaciones.
3. **Data Preparation:** Fuerte preprocesamiento, imputación, normalización y *encoding*.
4. **Modeling:** Desarrollo paralelo de múltiples arquitecturas (Linear, Ridge, Lasso, Random Forest, Gradient Boosting).
5. **Evaluation:** Contraste riguroso de métricas (R², MAE, RMSE).
6. **Deployment:** Planteamiento de una arquitectura modular exportable y de fácil reproducción.

La **planificación** estructuró el trabajo en fases progresivas documentadas en cuadernos tipo `.ipyne` en `notebooks` y un encapsulamiento posterior en código fuente en `src`.

## VII. EDA y Visualización

El Análisis Exploratorio de Datos desveló el latir del mercado automotriz. 

### Estadísticas y Hallazgos
- **Distribuciones asimétricas:** La variable objetivo `price` presentó un comportamiento sesgado, con una media artificialmente inflada por outliers extremos; en valores irrisorios como cientos de millones; frente a una mediana mucho más realista.
- **Kilometraje y devaluación:** Como era esperable, se comprobó empíricamente el decaimiento del valor a medida que el `odometer` aumenta, aunque se detectaron outliers anómalos.
- **Predominancia de marca:** Fabricantes como Ford, Chevrolet y Toyota dominan abrumadoramente la oferta.
- **Correlación multidimensional:** La matriz de correlación indicó que el precio no obedece a un único factor aislado, sino a una constelación compleja de variables, justificando así la necesidad de modelos multivariados.

### Visualizaciones Clave (PONER FOTOS)
El comportamiento de los datos se ilustra con claridad en los siguientes registros gráficos:
- Distribución de fabricantes: `reports/images/Top_10_nueva_data.png`
- Relación Precio vs Odómetro tras procesamiento: `reports/images/precio_vs_odometro_nueav_data.png`
- Distribución de Años normalizada: `reports/images/distribucion_años_nueva_data.png`
- Distribución de la variable objetivo Precio: `reports/images/distribucion_precios_nueva_data.png`

*Porque a veces lo esencial es invisible a los ojos, y las verdades de los datos solo se revelan mediante una adecuada proyección visual.*

## VIII. Preprocesamiento y Calidad

El conjunto de datos crudo presentaba un entorno hostil para cualquier algoritmo matemático, dado que presentaba cadenas de texto, variables que un algoritmo simplemente no podría entender... Se aplicó una reestructuración profunda documentada en `src/encode_dataset.py` y `02_preprocessing.ipynb`. Esta reestructuración transformó las variables categóricas en numéricas, además de aplicar normalización, entre otras.

### Limpieza y Nulos
- Eliminación de registros con nulos en variables medulares, irremplazables sin sesgo: `year`, `manufacturer`, `model`, `odometer`.
- Variables categóricas menos críticas como `condition` o `cylinders` recibieron imputación mediante la categoría `"unknown"` para salvaguardar la estructura de datos subyacente. Otras como `fuel` se imputaron por moda.

### Reducción de Dimensionalidad e Irrelevancias
Se extirparon columnas carentes de utilidad analítica (`url`, `image_url`, `description`, `VIN`). Notablemente, la variable `state` fue removida, junto con otras geográficas espurias como `county` (completamente vacía), centrando el enfoque en el activo y no en la procedencia dispersa.

### Encoding y Normalización
- **Target Encoding de `model`:** Ante la altísima cardinalidad de los modelos de vehículos, el *One-Hot Encoding* habría fragmentado mortalmente el dataset. Se aplicó un elegante *Target Encoding*, mapeando cada modelo a su precio histórico promedio, condensando la riqueza de la marca en un único vector numérico continuo de alta densidad informativa.
- **One-Hot Encoding:** Para variables categóricas de baja cardinalidad, eliminando la primera categoría (`drop_first=True`) para prevenir colinealidad.
- **Normalización:** Para democratizar el peso de las variables continuas, se empleó un proceso de escalado (Min-Max y StandardScaler), centrando los datos y permitiendo que ninguna magnitud oscureciera a otra en los procesos de optimización.

## IX. Comparación de Técnicas

La realidad no se dejó encerrar en una línea, es caótica y desenfrenada. Para modelarla, se convocó un elenco de cinco algoritmos, cada uno con una manera distinta de comprender el mundo.

### Modelos Evaluados y Resultados
| Modelo | MAE | RMSE | R² | MAPE (%) | Complejidad Big O |
|--------|-----|------|----|----------|-------------------|
| Regresión Lineal | 0.2892 | 0.4333 | 0.8130 | 115.96 | O(n) |
| Ridge (L2) | 0.2892 | 0.4333 | 0.8130 | 115.96 | O(n) |
| Lasso (L1) | 0.2914 | 0.4381 | 0.8089 | 116.98 | O(n) |
| Gradient Boosting | 0.2412 | 0.3795 | 0.8566 | 120.58 | O(n * iteraciones) |
| **Random Forest** | **0.1017** | **0.2247** | **0.9497** | **52.14** | **O(n * trees * depth)** |

### Justificación de Selección
El paradigma lineal ofreció un baseline digno (R² ~0.81), demostrando que una aproximación afín rescataba gran parte de la varianza. Sin embargo, su rigidez teórica falló ante la naturaleza fracturada de los precios. Gradient Boosting mejoró marginalmente las cosas, pero careció de la contundencia estructural necesaria. 

El bosque aleatorio (*Random Forest*) destrozó las barreras de desempeño. Abandonando la linealidad, este ensamble capturó las complejas interacciones locales de la tasación automotriz, llevando el R² a casi un 95%. La selección responde puramente al avasallador salto métrico, asumiendo su inherente costo computacional.

## X. Arquitectura del Modelo

### Modelo Ganador: Random Forest
El regresor definitivo es un ensamble arbóreo que abstrae reglas de decisión no lineales en paralelo, promediando el conocimiento de múltiples estimadores débiles para conformar un conocimiento robusto.

### Hiperparámetros
Extraídos directamente desde `train_random_forest.py`:
- `n_estimators=100` (100 árboles conforman el bosque).
- `max_depth=None` (Crecimiento libre de los nodos hasta alcanzar la pureza máxima de las hojas).
- `random_state=42` (Garantía de reproducibilidad estocástica).
- `n_jobs=-1` (Aprovechamiento pleno del paralelismo en hardware).

### Justificación Técnica Profunda
Un vehículo no deprecia su valor de forma puramente constante. Un automóvil clásico de 1960 puede valer mucho más que un sedán común de 2010; estas relaciones polinómicas y excepciones son invisibles para la Regresión Lineal o Lasso. Al permitir `max_depth=None`, el Random Forest desciende a la granularidad absoluta de los datos, ramificando el espacio multidimensional para aislar casuísticas complejas, previniendo el sobreajuste a través de la aleatorización de variables y datos (Bagging).

## XI. Validación Experimental

- **Train/Test Split:** Se implementó una segmentación canónica del 80% para la fase de entrenamiento y construcción topológica de los árboles (Train), reservando de forma estricta un 20% para la validación de su capacidad de generalización frente a datos jamás vistos (Test).
- **Estrategia:** La validación se ejecutó sin alteración cronológica o estratificada extrema, asumiendo que tras el filtro de limpieza inicial, el muestreo aleatorio (`random_state=42`) resultaba representativo del dominio analítico.

## XII. Evaluación e Interpretabilidad

### Métricas Críticas
El desempeño del Random Forest arroja:
- **MAE:** 0.1017
- **RMSE:** 0.2247
- **R²:** 0.9497
- **MAPE:** 52.14%

### Análisis Crítico e Interpretabilidad
Las métricas MAE y RMSE, evaluadas sobre el conjunto escalado, exhiben márgenes de error formidables, denotando que la curva de predicción abraza de cerca la realidad. El R² de 0.9497 implica que casi el 95% de la varianza en los precios queda explicada exclusivamente por las variables seleccionadas.

### Importancia de Variables (Feature Importance)
La caja negra del modelo se ilumina al estudiar las directrices que gobiernan sus decisiones (según `results/random_forest/feature_importance_top20.csv`):
1. **model_encoded (0.6028):** El modelo/versión aglutina casi un 60% del peso en la decisión.
2. **year (0.2141):** La antigüedad explica un 21% de la depreciación.
3. **odometer (0.0537):** Sorprendentemente, el kilometraje representa cerca del 5%, evidenciando que frente al año o el modelo, pasa a un plano secundario.

Estas variables reinan en el bosque, mientras el resto actúa como un fino ajuste estético en las ramas finales.

## XIII. Sistema y Pipeline

El proyecto fue estructurado bajo una **arquitectura modular** que propicia la mantenibilidad y la inyección de nuevas características sin causar una refactorización severa.

### Flujo Completo del Sistema
1. **Ingesta:** Datos crudos (Kaggle) reposan en `data/raw`.
2. **Transformación:** Procesamiento estadístico y *encoding* centralizado (vía cuadernos de Jupyter y `src/encode_dataset.py`), empujando la data curada a `data/processed`.
3. **Modelamiento Aislado:** Los subdirectorios en `src/` (`linear_regression/`, `random_forest/`, etc.) hospedan scripts de entrenamiento autocontenidos.
4. **Persistencia:** Artefactos entrenados son serializados (.pkl) a `models/`, mientras que sus registros técnicos alimentan `results/`.

Esta segmentación del pipeline (ETL + Machine Learning) orquesta un ciclo limpio de experimentación.

## XIV. Repositorio

### Estructura
El esqueleto del proyecto fomenta el orden cognitivo y funcional:
- `/data`: Segregación entre `raw/` y `processed/`.
- `/notebooks`: Narrativa experimental interactiva.
- `/src`: Lógica de negocio y *pipelines* algorítmicos.
- `/models`: Almacén de binarios inteligentes.
- `/results` & `/reports`: Documentación auto-generada y bitácora del proyecto.

De este modo, las vertebras son la estructura del proyecto, y la medula espinal es el flujo que recorre a traves de ellas, el pipeline.

### Reproducibilidad y Uso
Todo el ciclo de obtención, manipulación e iteración predictiva es de réplica directa. La ejecución secuencial de los notebooks reconstruye el estado fundamental. Por limitación de tamaño, la matriz procesada (`vehicles_processed_nums.csv`) reside externamente, estando exiliada del repositorio principal vía `.gitignore`, previniendo fatigas en el control de versiones.

## XV. Mejoras y Limitaciones

El proyecto es poderoso, pero no está exento del roce con la realidad:
- **Limitaciones por Dataset:** Los datos provienen de extracciones automatizadas sin una estricta taxonomía, inyectando ruido e inconsistencias que las purgas estadísticas intentan apaciguar, pero no eliminan en su totalidad.
- **Falta de datos en Chile:** La contextualidad geográfica condena a este algoritmo a ser un oráculo extranjero. Sin datos específicos del mercado automotriz local chileno (con sus propios impuestos, preferencias e inflaciones), la aplicación territorial directa es falaz.
- **Peso de modelos (Random Forest):** La lucidez del Random Forest exige un tributo físico. Frente a los escasos Kilobytes de una regresión lineal, el ensamble genera un artefacto cercano a 1.50 GB, complicando drásticamente su despliegue en infraestructuras ligeras o *Edge Computing*.
- **Generalización:** El sesgo en el volumen representativo de fabricantes (Ford, Chevrolet, Toyota) fuerza al modelo a especializarse en el *mainstream*, dejando en vulnerabilidad estadística a vehículos de nicho.

## XVI. Conclusiones

Este proyecto ilustra el vertiginoso tránsito desde el caos de datos desestructurados hasta la certidumbre de un modelo predictivo altamente calibrado. Iniciando con un mapeo lineal, se comprobó que la depreciación vehicular es un fenómeno interrelacionado y fragmentado, cuya verdad solo pudo ser descifrada por la profundidad fractal de un Random Forest.

Se cumplieron a cabalidad los requisitos operacionales: preprocesamiento exhaustivo, modularización arquitectónica y obtención de métricas sobresalientes; como en el caso de R² ~0.95 del modelo random forest. A pesar de los ecos del sobrepeso computacional del modelo y la geolocalización ajena de los datos, el flujo conceptual construido sienta bases indiscutibles para una eventual tasación automatizada de clase empresarial. 

A veces, para entender verdaderamente el valor de algo en este mundo, debemos dejar que cientos de árboles dialoguen sobre ello, echando raices en lo profundo del conocimiento colectivo, dando los frutos del entendimiento.

## XVII. Referencias (APA 7)

- Reese, A. (2021). *Craigslist Cars and Trucks Data* [Conjunto de datos]. Kaggle. https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data
- Scikit-learn Developers. (2023). *Scikit-learn: Machine Learning in Python* (Versión 1.3) [Software]. https://scikit-learn.org/
- McKinney, W. (2010). Data Structures for Statistical Computing in Python. En *Proceedings of the 9th Python in Science Conference* (pp. 51-56).
- Farías, C. (2026). *Proyecto de Regresión de Precios de Vehículos* [Repositorio de código y reportes internos]. Universidad Andrés Bello, sede Viña del Mar.
