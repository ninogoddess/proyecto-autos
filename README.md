# Predicción de Precios de Vehículos Usados

**Nombre:** Celso Farías  
**Carrera:** Ingeniería Civil Informática  
**Universidad:** Andrés Bello - sede Viña del Mar
**Fecha:** Marzo 2026  

---

## 1. Formulación del Problema

En el mercado de vehículos usados, la correcta tasación de un automóvil representa un desafío tanto para empresas como para usuarios particulares. Actualmente, la determinación del precio de un vehículo suele depender de criterios subjetivos o herramientas limitadas, lo que puede generar inconsistencias, sobrevaloraciones o subvaloraciones.

Este proyecto aborda esta problemática desde una perspectiva de ciencia de datos, proponiendo el desarrollo de un modelo que permita **estimar el precio de un vehículo en base a sus características**.

El resultado de este trabajo puede ser aplicado en procesos organizacionales de empresas como automotoras, plataformas de compraventa o servicios de tasación, como el SII, permitiendo mejorar la precisión y consistencia en la valorización de vehículos.

---

## 2. Pregunta Analítica

**¿En qué medida es posible estimar el precio de un vehículo usado a partir de sus características estructurales y técnicas, tales como año, marca, modelo, kilometraje y tipo de combustible?**

---

## 3. Objetivos

### Objetivo General
Desarrollar un modelo de regresión capaz de estimar el precio de vehículos usados a partir de sus características, utilizando técnicas de análisis y procesamiento de datos.

### Objetivos Específicos

1. **Realizar un proceso de limpieza y preprocesamiento del dataset**, abordando valores nulos, inconsistencias y variables irrelevantes, con el fin de obtener un conjunto de datos confiable y utilizable para análisis posteriores.

2. **Analizar exploratoriamente los datos, o un EDA,** para identificar patrones, distribuciones, relaciones entre variables y posibles outliers que puedan afectar el desempeño del modelo.

3. **Construir y evaluar un modelo de regresión** que permita predecir el precio de un vehículo, utilizando variables relevantes del dataset.

4. **Diseñar una interfaz simple, de frontend o prototipo,** que permita a un usuario ingresar características de un vehículo y obtener una estimación de su precio de forma intuitiva.

---

## 4. KPIs y Criterios de Éxito

Los siguientes indicadores permitirán evaluar el éxito del proyecto:

- **Precisión de estimación:**  
  El modelo debe ser capaz de entregar precios cercanos a los valores reales del mercado.

- **Consistencia de resultados:**  
  Vehículos con características similares deben obtener estimaciones similares.

- **Usabilidad de la solución:**  
  El sistema debe permitir a un usuario ingresar datos de forma sencilla y obtener una estimación clara.

- **Valor práctico para el negocio:**  
  La solución debe ser útil como apoyo en procesos de tasación para empresas o plataformas de venta de vehículos.

---

## 5. Dataset Utilizado

Se utiliza el dataset **"Craigslist Cars & Trucks Data"**, obtenido desde Kaggle:

https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data

### Descripción General

El dataset contiene información sobre vehículos en venta en distintas regiones, con un total de:

- **426.880 registros**
- **26 variables**

Incluye características relevantes como:

- Precio (`price`)
- Año (`year`)
- Fabricante (`manufacturer`)
- Modelo (`model`)
- Kilometraje (`odometer`)
- Tipo de combustible (`fuel`)
- Transmisión (`transmission`)
- Estado del vehículo (`condition`)
- Ubicación geográfica (`state`, `lat`, `long`)

---

## 6. Relación Dataset - Problema

El dataset es altamente pertinente para el problema planteado, ya que contiene directamente la variable objetivo (**precio**) junto con múltiples variables explicativas que influyen en su determinación.

Esto permite:

- Analizar factores que afectan el precio de un vehículo
- Identificar patrones de valorización
- Entrenar modelos predictivos basados en datos reales

---

## 7. Restricciones del Dataset

El dataset presenta algunas limitaciones que deben ser abordadas:

- **Valores faltantes** en múltiples variables, como en `condition`, `cylinders`, `VIN`, `size`.
- **Datos inconsistentes o ruidosos**
- **Columnas irrelevantes o con baja utilidad analítica**, como `url`, `image_url`, `description`.
- **Variable `county` completamente vacía**
- Posibles **outliers en precios o kilometraje**

Estas condiciones hacen necesario un proceso riguroso de limpieza y preprocesamiento.

---

## 8. Utilidad Analítica

El dataset permite desarrollar soluciones de alto valor, tales como:

- Modelos de predicción de precios de vehículos
- Sistemas de apoyo a la toma de decisiones en compraventa
- Herramientas de tasación automatizada
- Análisis de tendencias del mercado automotriz

---

## 9. Estructura del Proyecto:
```text
proyecto-autos/
│
├── data/
│   ├── raw/
│   │   ├── datos_crudos_ejemplos.csv
│   │
│   ├── processed/
│   │   ├── datos_procesados_ejemplos.csv
│   │   ├── vehicles_processed.csv 
│   │   ├── vehicles_processed_nums.csv //no está en github dado el tamaño
│   │   ├── model_encoding_map.csv
│
├── notebooks/
│   ├── 00_obtencion_data.ipynb
│   ├── 01_EDA_primer_avance_CD_autos.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── uso_dataset_celso_kaagle.yynb
│
├── src/
│   │
│   ├── encode_dataset.py
│   │
│   ├── linear_regression/
│   │   ├── train_linear_regression.py
│   │
│   ├── ridge_regression/
│   │   ├── train_ridge.py
│   │
│   ├── lasso_regression/
│   │   ├── train_lasso.py
│   │
│   ├── random_forest/
│   │   ├── train_random_forest.py
│   │
│   ├── gradient_boosting/
│       ├── train_gradient_boosting.py
│
├── models/
│   ├── linear_regression/
│   │   ├── model.pkl
│   │
│   ├── ridge_regression/
│   │   ├── model.pkl
│   │
│   ├── lasso_regression/
│   │   ├── model.pkl
│   │
│   ├── random_forest/
│   │   ├── model.pkl
│   │
│   ├── gradient_boosting/
│       ├── model.pkl
│
├── results/
│   │
│   ├── linear_regression/
│   │   ├── metrics_linear.md
│   │
│   ├── ridge_regression/
│   │   ├── metrics_ridge.md
│   │
│   ├── lasso_regression/
│   │   ├── metrics_lasso.md
│   │
│   ├── random_forest/
│   │   ├── metrics_random_forest.md
│   │   ├── feature_importance_top20.csv
│   │
│   ├── gradient_boosting/
│   │   ├── metrics_gradient_boosting.md
│   │   ├── feature_importance_top20.csv
│   │
│   ├── metrics_global.csv
│
├── reports/
│   ├── images/
│   ├── 01_data_quality.md
│   ├── 01.5_segundo_preprocesamiento.md
│
├── README.md
├── .gitignore
```

---

## 10. Reproducibilidad

Para reproducir tanto los pasos como la obtención de datos simplemente ejecute los notebooks dentro de la carpeta `notebooks`de este repositorio, en el orden de sus nombres. Todo el código está dispuesto de modo tal que sea sencillamente replicable sin instalar nada extra o fuera de lo común.
Luego, puede obtener el dataset procesado desde Kaagle ya se para descarga o uso libre, según las indicaciones del script `uso_dataset_celso_kaagle.py` o en el enlace https://www.kaggle.com/datasets/celsofariasaraya/vehicules-processed-celso.
Posteriormente, se ejecutan los scripts dentro de la carperta `src`.

## 11. Próximos Pasos 

Esto puede mutar conforme al avance del proyecto.

- Evaluación del modelo mediante sistema de usaje
