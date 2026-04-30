# 02_comparación_técnica.md
### Proyecto de Regresión de Precios de Vehículos

**Autor:** Celso Farías
**Fecha:** 29 de abril
---

#  Casting de modelos

En el inicio de esta etapa, el problema no pedía una respuesta aún, sino una exploración a campo traviesa.
Siete técnicas fueron convocadas como posibles intérpretes de la realidad contenida en los datos, candidatas a ser las que traerían la solucion al santo mundo.

Cada una con su propia forma de ver la realidad, cada una con su propia manera de aprender.

---

## 1. Regresión Lineal

**Qué hace:**
Modela la relación entre variables como una combinación lineal.

**Cómo lo hace:**
Ajusta una recta, o hiperplano, que minimiza el error cuadrático.

**Pros:**

* Simple e interpretable
* Rápida
* Buen baseline

**Contras:**

* No captura relaciones no lineales
* Sensible a outliers

---

## 2. Ridge Regression o L2 

**Qué hace:**
Extiende la regresión lineal penalizando coeficientes grandes.

**Cómo lo hace:**
Agrega una penalización L2 al error.

**Pros:**

* Reduce sobreajuste
* Estabiliza coeficientes

**Contras:**

* No realiza selección de variables
* Mantiene todas las features

---

## 3. Lasso Regression o L1

**Qué hace:**
Realiza regresión lineal con selección automática de variables.

**Cómo lo hace:**
Aplica penalización L1 que lleva coeficientes a cero.

**Pros:**

* Reduce dimensionalidad
* Mejora interpretabilidad

**Contras:**

* Inestable con variables correlacionadas
* Puede eliminar variables relevantes

---

## 4. Elastic Net

**Qué hace:**
Combina L1 y L2.

**Cómo lo hace:**
Balancea ambas penalizaciones.

**Pros:**

* Equilibrio entre Ridge y Lasso

**Contras:**

* Requiere tuning adicional

---

## 5. Random Forest

**Qué hace:**
Construye múltiples árboles de decisión y promedia sus resultados.

**Cómo lo hace:**
Entrena árboles independientes sobre subconjuntos aleatorios.

**Pros:**

* Captura no linealidad
* Robusto al ruido
* Alta precisión

**Contras:**

* Modelo pesado
* Menor interpretabilidad

---

## 6. Gradient Boosting

**Qué hace:**
Construye árboles secuencialmente corrigiendo errores previos.

**Cómo lo hace:**
Optimiza gradualmente el error residual.

**Pros:**

* Alta precisión potencial
* Modelo compacto

**Contras:**

* Sensible a hiperparámetros
* Más lento de entrenar

---

## 7. Support Vector Regression o SVR

**Qué hace:**
Busca una función que minimice el error dentro de un margen.

**Cómo lo hace:**
Utiliza kernels para capturar relaciones complejas.

**Pros:**

* Potente en espacios no lineales

**Contras:**

* Escala mal con grandes datasets
* Alto costo computacional

---

#  Selección de técnicas

De este conjunto inicial, se seleccionaron cinco técnicas para su implementación:

* Regresión Lineal
* Ridge Regression
* Lasso Regression
* Random Forest
* Gradient Boosting

---

## Justificación

La selección respondió a un criterio de equilibrio entre:

* Interpretabilidad
* Complejidad
* Capacidad de modelado

---

Se descartaron:

* **Elastic Net**, por redundancia conceptual
* **SVR**, por su alto costo computacional en un dataset de gran tamaño y ser demasiado para este proyecto... no queremos liquidar una mosca con una bazooka.

---

#  Entrenamiento de modelos

Cada modelo fue implementado de forma modular dentro del directorio `src/`, donde cada técnica posee su propio script de entrenamiento (`train_*.py`).

Durante su ejecución, cada script:

* Entrena el modelo
* Genera métricas
* Guarda resultados en `results/`
* Guarda el modelo en `models/`

---

## Hardware utilizado

* CPU: Ryzen 7 4800H
* RAM: 16 GB
* GPU: RTX 2060
* Entorno: Windows 10 + VS Code

---

## Archivos generados

Por cada técnica:

* `models/<tecnica>/model.pkl`
* `results/<tecnica>/metrics_*.md`

Adicionalmente:

* Random Forest y Gradient Boosting generan:

  * `feature_importance_top20.csv`

---

## Tamaño de modelos

| Modelo                 | Tamaño   |
| ---------------------- | -------- |
| Linear / Ridge / Lasso | ~4.00 KB |
| Gradient Boosting      | ~142.00 KB  |
| Random Forest          | ~1.50 GB  |

---

Aquí emerge un contraste poderoso:

> Algunos modelos aprenden con precisión ligera.
> Otros recuerdan con un peso casi físico, como si de estos colgaran las cadenas del saber.

---

# Comparación y análisis

---

## Regresión Lineal

| Métrica  | Valor  |
| -------- | ------ |
| MAE      | 0.2892 |
| RMSE     | 0.4333 |
| R²       | 0.8130 |
| MAPE (%) | 115.96 |
| Tiempo (s) | 1.70 |

El modelo logra explicar un 81.3% de la variabilidad, mostrando una base sólida.
Sin embargo, la diferencia entre MAE y RMSE revela errores significativos en casos extremos.

---

## Ridge Regression

| Métrica  | Valor  |
| -------- | ------ |
| MAE      | 0.2892 |
| RMSE     | 0.4333 |
| R²       | 0.8130 |
| MAPE (%) | 115.96 |
| Tiempo (s) | 0.43 |

Resultados idénticos a la regresión lineal.

> No había inestabilidad que corregir.
> El modelo ya estaba en equilibrio y esta es una gran prueba.

---

## Lasso Regression

| Métrica  | Valor  |
| -------- | ------ |
| MAE      | 0.2914 |
| RMSE     | 0.4381 |
| R²       | 0.8089 |
| MAPE (%) | 116.98 |
| Tiempo (s) | 1.50 |

Eliminó un 45% de las variables sin pérdida significativa de rendimiento.

> La mitad del ruido fue silenciado…
> y el modelo siguió entendiendo casi lo mismo.
> esto hace creer que el preprocesamiento y limpieza podría haber sido más riguroso sin perder calidad de entrenamiento.
> Hasta aquí podemos ver un aumentoconsiderablemente... pequeño en cuanto a los tiempos de entreamiento.

---

## Random Forest

| Métrica  | Valor      |
| -------- | ---------- |
| MAE      | **0.1017** |
| RMSE     | **0.2247** |
| R²       | **0.9497** |
| MAPE (%) | **52.14**  |
| Tiempo (s) | 66.32 |

El modelo alcanzó un salto significativo en rendimiento.

> La realidad no se dejó encerrar en una línea, es caótica, desenfrenada, cual ideología.
> Se necesitó de un bosque completo para ser comprendida.
> Además, vemos la primer gran diferencia en cuanto al tiempo de entrenamiento, siendo este de poco mas de 60 segundos.

---

## Gradient Boosting

| Métrica  | Valor  |
| -------- | ------ |
| MAE      | 0.2412 |
| RMSE     | 0.3795 |
| R²       | 0.8566 |
| MAPE (%) | 120.58 |
| Tiempo (s) | 73.54 |


A pesar de su enfoque secuencial, no logró igualar el desempeño del bosque.

> Y es que... que van ha hacer unos cuantos arbustitos contra la nobleza y porte de los robles.
> Con una profundidad de apenas 3 nodos, son pasto, musgo, creciendo bajo sus copas de desision y sobre las raices del aprendizaje.

---

# 🔹 Comparación global

| Modelo            | MAE        | RMSE       | R²         | MAPE      |
| ----------------- | ---------- | ---------- | ---------- | --------- |
| Linear            | 0.2892     | 0.4333     | 0.8130     | 115.96    |
| Ridge             | 0.2892     | 0.4333     | 0.8130     | 115.96    |
| Lasso             | 0.2914     | 0.4381     | 0.8089     | 116.98    |
| Random Forest     | **0.1017** | **0.2247** | **0.9497** | **52.14** |
| Gradient Boosting | 0.2412     | 0.3795     | 0.8566     | 120.58    |

---

## Modelo ganador: **Random Forest**

Seleccionado exclusivamente por desempeño en métricas, dado que no estamos considerando ni tiempo de entramiento; relativo a la eficiencia; ni peso del modelo; relacionado a optimización de rescursos. El modelo de Rando Forest es ridiculamente pesado en compracion a sus semejantes, no obstante, da un salto de calidad de entrenamiento brutal y eso lo posiciona como el gnador de la comparación. 

---

# 🔹 Conclusión

El recorrido comenzó con modelos lineales que ofrecieron una comprensión inicial del problema. Ciega a los ojos del mediocre, ya llegaría otra perspectiva a imponer su calidad.
Siendo así, fue al abandonar la linealidad cuando emergió la verdadera estructura de los datos.

> No era un problema de falta de datos.
> Era un problema de profundidad.

Random Forest no solo mejoró las métricas,
sino que reveló la naturaleza del fenómeno:

una realidad fragmentada, no lineal, compuesta por múltiples decisiones locales.

Y en ese bosque de decisiones…
finalmente, el modelo encontró el camino.

---
