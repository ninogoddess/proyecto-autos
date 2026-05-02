import os
import joblib
import numpy as np

# =========================
# RUTAS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../models/random_forest/model.pkl")
)

OUTPUT_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../results/random_forest/model_complexity.md")
)

# =========================
# CARGAR MODELO
# =========================
model = joblib.load(MODEL_PATH)

# =========================
# EXTRACCIÓN DE MÉTRICAS
# =========================
n_trees = len(model.estimators_)

node_counts = [tree.tree_.node_count for tree in model.estimators_]
depths = [tree.tree_.max_depth for tree in model.estimators_]

total_nodes = int(np.sum(node_counts))
avg_nodes = float(np.mean(node_counts))

avg_depth = float(np.mean(depths))
max_depth = int(np.max(depths))
min_depth = int(np.min(depths))

# =========================
# CREAR CONTENIDO MD
# =========================
md_content = f"""# Complejidad del Modelo - Random Forest

## Resumen general

| Métrica | Valor |
|--------|------|
| Número de árboles | {n_trees} |
| Total de nodos | {total_nodes} |
| Nodos promedio por árbol | {avg_nodes:.2f} |
| Profundidad promedio | {avg_depth:.2f} |
| Profundidad máxima | {max_depth} |
| Profundidad mínima | {min_depth} |

## Interpretación técnica

El modelo Random Forest no aprende coeficientes globales, sino estructuras de decisión.

Cada árbol representa una serie de particiones del espacio de datos, donde cada nodo corresponde a una regla aprendida.

El total de nodos del bosque puede interpretarse como una aproximación a la cantidad de decisiones que el modelo ha internalizado para representar la relación entre variables.

A mayor número de nodos y profundidad, mayor capacidad de modelado, pero también mayor costo computacional y riesgo de sobreajuste.

"""

# =========================
# GUARDAR ARCHIVO
# =========================
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(md_content)

print("Archivo generado en:")
print(OUTPUT_PATH)