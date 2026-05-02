# Complejidad del Modelo - Random Forest

## Resumen general

| Métrica | Valor |
|--------|------|
| Número de árboles | 100 |
| Total de nodos | 22134188 |
| Nodos promedio por árbol | 221341.88 |
| Profundidad promedio | 50.53 |
| Profundidad máxima | 59 |
| Profundidad mínima | 47 |

## Interpretación técnica

El modelo Random Forest no aprende coeficientes globales, sino estructuras de decisión.

Cada árbol representa una serie de particiones del espacio de datos, donde cada nodo corresponde a una regla aprendida.

El total de nodos del bosque puede interpretarse como una aproximación a la cantidad de decisiones que el modelo ha internalizado para representar la relación entre variables.

A mayor número de nodos y profundidad, mayor capacidad de modelado, pero también mayor costo computacional y riesgo de sobreajuste.

