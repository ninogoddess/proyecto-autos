# Requirements Document

## Introduction

Este documento define los requisitos para transformar el mockup existente de predicción de precios de vehículos en un sistema web funcional completo. El sistema integra un frontend moderno (React/Vite) con un backend API (FastAPI) que consume un modelo de Machine Learning (Random Forest) entrenado previamente, permitiendo a los usuarios obtener estimaciones de precio basadas en las características de un vehículo.

Este proyecto corresponde a la Fase 1 (Hito 2) del proyecto de Ciencia de Datos de la carrera de Ingeniería Civil Informática, Universidad Andrés Bello.

## Glossary

- **Sistema_Web**: Aplicación web completa compuesta por frontend y backend que permite la predicción de precios de vehículos usados.
- **Frontend**: Interfaz de usuario construida con React y Vite que presenta formularios de entrada y resultados de predicción.
- **Backend_API**: Servicio REST construido con FastAPI que recibe solicitudes de predicción, procesa los datos y retorna estimaciones de precio.
- **Modelo_ML**: Modelo de Random Forest entrenado (~1.5GB) almacenado como archivo .pkl que realiza la predicción de precios.
- **Formulario_Predicción**: Componente del Frontend que captura las características del vehículo ingresadas por el usuario.
- **Motor_Preprocesamiento**: Módulo del Backend_API que transforma los datos de entrada del usuario al formato requerido por el Modelo_ML (normalización, encoding, one-hot encoding).
- **Encoding_Map**: Archivo CSV que contiene el mapeo de modelos de vehículos a sus valores numéricos (Target Encoding por precio promedio).
- **Resultado_Predicción**: Respuesta del sistema que incluye el precio estimado en CLP y los datos del vehículo consultado.
- **Documentación_Técnica**: Conjunto de archivos Markdown que describen la arquitectura, flujos, decisiones de diseño y guías de despliegue del sistema.

## Requirements

### Requirement 1: Arquitectura del Sistema

**User Story:** Como desarrollador del proyecto, quiero contar con una arquitectura técnica documentada y modular, para que el sistema sea mantenible, escalable y presentable como proyecto universitario.

#### Acceptance Criteria

1. THE Sistema_Web SHALL separar la lógica en dos componentes desplegables de forma independiente: Frontend y Backend_API, cada uno con su propio archivo de gestión de dependencias (package.json para Frontend, requirements.txt para Backend_API), comunicados exclusivamente mediante solicitudes HTTP REST sin compartir base de datos, sistema de archivos ni estado en memoria.
2. THE Frontend SHALL construirse con React 19 y Vite 8 como herramienta de bundling y desarrollo.
3. THE Backend_API SHALL construirse con FastAPI y exponer endpoints REST documentados automáticamente mediante OpenAPI/Swagger, accesibles en la ruta /docs.
4. THE Sistema_Web SHALL definir su estructura de carpetas siguiendo separación de responsabilidades: el Frontend con directorios dedicados para componentes, servicios, utilidades y configuración; el Backend_API con directorios dedicados para rutas, servicios, modelos de datos y utilidades.
5. THE Documentación_Técnica SHALL incluir al menos 4 diagramas Mermaid sintácticamente válidos que representen: la arquitectura general, el flujo de predicción, la estructura modular del frontend y la comunicación frontend-backend.

### Requirement 2: Formulario de Entrada de Datos del Vehículo

**User Story:** Como usuario, quiero ingresar las características de mi vehículo en un formulario claro e intuitivo, para que el sistema pueda estimar su precio.

#### Acceptance Criteria

1. THE Formulario_Predicción SHALL capturar los siguientes campos obligatorios: marca (manufacturer), modelo (model), año (year), kilometraje (odometer), tipo de combustible (fuel), transmisión (transmission) y tipo de vehículo (type).
2. THE Formulario_Predicción SHALL poblar las opciones de marca, modelo, combustible, transmisión y tipo de vehículo exclusivamente a partir de los valores presentes en el dataset de entrenamiento, obtenidos mediante el endpoint GET /api/v1/options del Backend_API.
3. WHEN el usuario selecciona una marca, THE Formulario_Predicción SHALL filtrar dinámicamente las opciones de modelo disponibles para esa marca según los datos de entrenamiento, y SHALL mantener el campo modelo deshabilitado o vacío hasta que se seleccione una marca válida.
4. WHEN el usuario envía el formulario con campos vacíos o valores inválidos, THE Formulario_Predicción SHALL mostrar mensajes de error indicando el motivo de rechazo junto a cada campo inválido, sin recargar la página, dentro de los 500 milisegundos posteriores al envío.
5. THE Formulario_Predicción SHALL restringir el campo año al rango entre 1980 y el año actual (consistente con los filtros aplicados al dataset de entrenamiento).
6. THE Formulario_Predicción SHALL restringir el campo kilometraje al rango entre 0 y 300000 (consistente con los filtros aplicados al dataset de entrenamiento).
7. WHERE el sistema permita entrada de marcas o modelos no presentes en los datos de entrenamiento, THE Formulario_Predicción SHALL mostrar una advertencia visual indicando que la predicción puede ser menos precisa para valores desconocidos por el modelo.
8. IF el endpoint GET /api/v1/options no responde dentro de 10 segundos o retorna un error, THEN THE Formulario_Predicción SHALL mostrar un mensaje de error indicando que no se pudieron cargar las opciones del formulario, y SHALL ofrecer un mecanismo para reintentar la carga.
9. WHILE el Formulario_Predicción está obteniendo las opciones desde el Backend_API, THE Formulario_Predicción SHALL mostrar un indicador de carga en lugar de los campos del formulario.

### Requirement 3: Predicción de Precio mediante Modelo ML

**User Story:** Como usuario, quiero obtener una estimación de precio basada en un modelo de Machine Learning real, para que la valoración sea confiable y fundamentada en datos históricos.

#### Contexto Técnico

El Modelo_ML (Random Forest) fue entrenado con datos en un formato específico: variables numéricas normalizadas (Min-Max al rango [0,1]), variable `model` codificada mediante Target Encoding (precio promedio por modelo), y variables categóricas transformadas mediante One-Hot Encoding. Para que el modelo pueda realizar predicciones, los datos de entrada del usuario deben transformarse al mismo formato utilizado durante el entrenamiento. Este pipeline de preprocesamiento en inferencia es obligatorio y replica las transformaciones aplicadas al dataset original.

#### Acceptance Criteria

1. WHEN el Backend_API recibe una solicitud de predicción válida, THE Motor_Preprocesamiento SHALL transformar los datos de entrada al formato esperado por el Modelo_ML, replicando el pipeline de entrenamiento: normalización Min-Max para año (rango original: 1981 a 2024) y kilometraje (rango original: 1 a 299999), Target Encoding para el nombre del modelo de vehículo usando el Encoding_Map, y One-Hot Encoding con `drop_first=True` para marca, combustible, transmisión, tipo de vehículo y condición.
2. WHEN el Motor_Preprocesamiento completa la transformación, THE Backend_API SHALL construir el vector de 92 características en el orden exacto esperado por el Modelo_ML, asignando valores por defecto a las características no proporcionadas por el usuario (valor 0 para columnas one-hot no aplicables, y valor promedio del dataset para variables numéricas ausentes), e invocar la predicción.
3. WHEN el Modelo_ML retorna el valor predicho, THE Backend_API SHALL desnormalizar el precio aplicando la fórmula inversa de Min-Max con los parámetros del entrenamiento (precio mínimo: 1000 USD, precio máximo: 100000 USD) para convertirlo a la escala original en USD.
4. WHEN el Backend_API recibe una solicitud de predicción, THE Backend_API SHALL responder con el resultado en un tiempo inferior a 5 segundos, incluyendo las etapas de preprocesamiento, inferencia del modelo y desnormalización.
5. IF el modelo de vehículo ingresado no existe en el Encoding_Map, THEN THE Motor_Preprocesamiento SHALL utilizar el valor promedio global del Encoding_Map como valor de encoding por defecto, y THE Backend_API SHALL incluir una advertencia en la respuesta indicando que la predicción puede ser menos precisa.
6. IF la marca ingresada no corresponde a una marca conocida por el Modelo_ML, THEN THE Motor_Preprocesamiento SHALL asignar valor 0 a todas las columnas one-hot de fabricante, y THE Backend_API SHALL incluir una advertencia en la respuesta indicando que la marca no fue reconocida.
7. IF el Modelo_ML produce un error durante la inferencia o retorna un valor fuera del rango [0,1], THEN THE Backend_API SHALL responder con un mensaje de error indicando que la predicción no pudo completarse, sin exponer detalles internos del modelo.

### Requirement 4: Presentación de Resultados

**User Story:** Como usuario, quiero ver el resultado de la predicción de forma clara y visualmente atractiva, para que pueda comprender fácilmente la estimación de precio de mi vehículo.

#### Acceptance Criteria

1. WHEN el Frontend recibe una respuesta exitosa del Backend_API, THE Frontend SHALL mostrar el precio estimado formateado en pesos chilenos con el prefijo "$", separador de miles con punto y sin decimales (ejemplo: $12.500.000).
2. WHEN el Frontend recibe una respuesta exitosa, THE Frontend SHALL mostrar un resumen que incluya todos los campos ingresados por el usuario (marca, modelo, año, kilometraje, tipo de combustible, transmisión y tipo de vehículo) junto al precio estimado.
3. WHILE el Frontend espera la respuesta del Backend_API, THE Frontend SHALL mostrar un indicador de carga animado acompañado de mensajes de texto que rotan cada 3 segundos entre al menos 3 mensajes distintos relacionados con el proceso de predicción.
4. IF el Frontend recibe un error del Backend_API, THEN THE Frontend SHALL mostrar un mensaje de error que indique la naturaleza general del problema (conexión, datos inválidos o error del servidor) sin exponer códigos internos, trazas de pila ni nombres de módulos del backend.
5. IF la respuesta del Backend_API incluye advertencias (modelo o marca no reconocidos), THEN THE Frontend SHALL mostrar cada advertencia de forma visible junto al precio estimado, diferenciada visualmente del resultado principal.
6. WHEN el Frontend muestra el resultado de la predicción, THE Frontend SHALL incluir un botón o enlace que permita al usuario realizar una nueva consulta sin recargar la página.

### Requirement 5: API REST del Backend

**User Story:** Como desarrollador, quiero que el backend exponga una API REST bien definida y documentada, para que la integración con el frontend sea clara y el sistema sea extensible.

#### Acceptance Criteria

1. THE Backend_API SHALL exponer un endpoint POST /api/v1/predict que reciba un cuerpo JSON con los campos: manufacturer (string), model (string), year (entero), odometer (entero), fuel (string), transmission (string) y type (string), y retorne un objeto JSON con el precio estimado en CLP (numérico), los datos del vehículo consultado y un campo opcional de advertencias (lista de strings).
2. THE Backend_API SHALL exponer un endpoint GET /api/v1/options que retorne un objeto JSON con las opciones válidas para los campos del formulario: lista de marcas, modelos agrupados por marca, tipos de combustible, transmisiones y tipos de vehículo, respondiendo en un tiempo inferior a 2 segundos.
3. THE Backend_API SHALL validar los datos de entrada en cada solicitud y retornar códigos HTTP 200 para éxito, 422 para datos inválidos (incluyendo en el cuerpo de respuesta un arreglo de errores con el nombre del campo y el motivo de rechazo por cada campo inválido), y 500 para errores internos del servidor.
4. THE Backend_API SHALL incluir documentación interactiva accesible en la ruta /docs generada automáticamente por FastAPI.
5. THE Backend_API SHALL configurar CORS para permitir solicitudes desde el dominio del Frontend desplegado, habilitando los métodos HTTP GET y POST y los encabezados Content-Type y Authorization.

### Requirement 6: Diseño Visual y Experiencia de Usuario

**User Story:** Como usuario, quiero interactuar con una interfaz moderna, responsiva y visualmente coherente, para que la experiencia de uso sea agradable y profesional.

#### Acceptance Criteria

1. THE Frontend SHALL aplicar el sistema de diseño definido en las guías de branding: paleta de colores con primary #1ED760, background #121212, tipografía CircularSp-Arab con fallback a Helvetica Neue y sans-serif, unidad base de espaciado de 4px, y border-radius de 0px.
2. THE Frontend SHALL ser responsivo sin scroll horizontal, con todo el contenido visible y todos los elementos interactivos accesibles mediante touch o click, adaptándose a dispositivos móviles (320px mínimo), tablets (768px) y escritorio (1024px+).
3. THE Frontend SHALL utilizar variables CSS centralizadas definidas en :root para todos los colores y espaciados, sin valores hardcodeados en componentes individuales.
4. THE Frontend SHALL incluir transiciones CSS con duración entre 100ms y 300ms en las interacciones del usuario: escala en hover de botones, aparición progresiva de resultados de predicción, y rotación continua del indicador de carga.
5. IF el usuario tiene configurada la preferencia prefers-reduced-motion: reduce en su sistema operativo, THEN THE Frontend SHALL desactivar todas las animaciones y transiciones, mostrando los cambios de estado de forma inmediata.
6. THE Frontend SHALL proveer estados visuales diferenciados para todos los elementos interactivos: estado por defecto, hover, focus visible (para navegación por teclado), active y disabled.

### Requirement 7: Documentación Técnica del Proyecto

**User Story:** Como evaluador académico, quiero acceder a documentación técnica completa y profesional, para que pueda evaluar la calidad de la arquitectura y las decisiones de diseño del proyecto.

#### Acceptance Criteria

1. THE Documentación_Técnica SHALL incluir un documento de arquitectura general con un diagrama Mermaid válido (sintaxis renderizable) que muestre los componentes Frontend, Backend_API y Modelo_ML, sus protocolos de comunicación (HTTP REST entre Frontend y Backend_API, invocación en memoria entre Backend_API y Modelo_ML) y la dirección del flujo de datos.
2. THE Documentación_Técnica SHALL incluir un documento de flujo de predicción con un diagrama Mermaid válido (sintaxis renderizable) que represente como mínimo las siguientes etapas: entrada del usuario en el Formulario_Predicción, envío de solicitud al Backend_API, preprocesamiento por el Motor_Preprocesamiento (normalización, Target Encoding, One-Hot Encoding), invocación del Modelo_ML, desnormalización del resultado y respuesta al Frontend.
3. THE Documentación_Técnica SHALL incluir un documento de estructura del proyecto que liste todos los directorios de primer y segundo nivel del repositorio, indicando para cada uno su propósito y los módulos o archivos principales que contiene.
4. THE Documentación_Técnica SHALL incluir un documento de estrategia de despliegue que describa como mínimo: la plataforma destino de cada componente (Vercel para Frontend, servicio cloud para Backend_API), las variables de entorno requeridas para la conexión entre componentes, y los pasos necesarios para ejecutar el despliegue.
5. THE Documentación_Técnica SHALL estar redactada en español, almacenada como archivos Markdown dentro de un directorio dedicado a documentación en el repositorio del proyecto, y cada diagrama Mermaid incluido SHALL utilizar sintaxis válida renderizable por herramientas compatibles con Mermaid.
6. THE Documentación_Técnica SHALL incluir en cada documento al menos las siguientes secciones: título, descripción general del tema cubierto, contenido técnico principal (diagramas, listados o descripciones según corresponda) y referencias a otros documentos relacionados dentro de la misma documentación.

### Requirement 8: Estrategia de Despliegue

**User Story:** Como desarrollador, quiero tener una estrategia de despliegue definida, para que el sistema pueda ser publicado y accesible en internet de forma separada (frontend y backend).

#### Acceptance Criteria

1. THE Frontend SHALL producir un build estático mediante Vite (comando `npm run build`) que genere una carpeta de salida compatible con el despliegue en Vercel sin configuración adicional del servidor.
2. THE Backend_API SHALL ser desplegable como servicio independiente en una plataforma cloud que soporte contenedores o aplicaciones Python, con un mínimo de 2GB de RAM disponible para alojar el Modelo_ML (~1.5GB) en memoria.
3. THE Sistema_Web SHALL utilizar variables de entorno para configurar las URLs de conexión entre Frontend y Backend_API: el Frontend SHALL leer la variable VITE_API_BASE_URL para determinar la dirección del Backend_API, y el Backend_API SHALL leer la variable ALLOWED_ORIGINS para configurar los dominios CORS permitidos, sin valores hardcodeados en el código fuente.
4. THE Backend_API SHALL incluir un archivo Dockerfile que permita construir una imagen de contenedor exitosamente (sin errores de build) y que al ejecutarse inicie el servidor y responda a solicitudes HTTP en un puerto configurable mediante variable de entorno.
5. IF el Frontend no recibe respuesta del Backend_API dentro de 10 segundos o recibe un error de conexión, THEN THE Frontend SHALL mostrar un mensaje indicando que el servicio de predicción no está disponible temporalmente y SHALL permitir al usuario reintentar la solicitud.
6. THE Backend_API SHALL exponer un endpoint GET /api/v1/health que retorne una respuesta exitosa cuando el servicio esté operativo y el Modelo_ML esté cargado en memoria, permitiendo al Frontend y a la plataforma cloud verificar la disponibilidad del servicio.

### Requirement 9: Calidad de Código y Buenas Prácticas

**User Story:** Como desarrollador, quiero que el código siga buenas prácticas de ingeniería de software, para que el proyecto sea mantenible, legible y profesional.

#### Acceptance Criteria

1. THE Frontend SHALL organizar su código en componentes reutilizables donde cada componente no exceda 200 líneas de código y encapsule una única responsabilidad de interfaz (formulario, visualización de resultado, navegación, indicador de carga, etc.), sin mezclar lógica de presentación con lógica de comunicación con el Backend_API.
2. THE Backend_API SHALL organizar su código en módulos separados para rutas, servicios, modelos de datos y utilidades, donde cada módulo resida en su propio archivo o directorio dedicado.
3. THE Sistema_Web SHALL incluir un archivo README.md que contenga como mínimo las siguientes secciones: descripción del proyecto, requisitos previos (versiones de Node.js y Python), instrucciones de instalación de dependencias, instrucciones de ejecución local para frontend y backend, variables de entorno requeridas, e instrucciones de despliegue.
4. WHEN se ejecuta el comando `npm run lint` en el Frontend, THE Frontend SHALL completar la verificación con cero errores reportados por ESLint.
5. THE Backend_API SHALL definir modelos Pydantic con tipos explícitos para todos los campos de entrada (request body del endpoint de predicción) y todos los campos de salida (response body), sin utilizar tipos genéricos como `dict` o `Any` en las interfaces de la API.
6. THE Backend_API SHALL ejecutarse sin errores de importación circular entre sus módulos de rutas, servicios, modelos de datos y utilidades.
