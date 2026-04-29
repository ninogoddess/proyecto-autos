import os
import time
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# =========================
# CONFIG
# =========================
MODEL_NAME = "random_forest"

DATA_PATH = "data/processed/vehicles_processed_nums.csv"
TARGET_COLUMN = "price"

MODEL_DIR = f"models/{MODEL_NAME}"
RESULTS_DIR = f"results/{MODEL_NAME}"
GLOBAL_RESULTS = "results/metrics_global.csv"

# =========================
# CREATE DIRECTORIES
# =========================
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs("results", exist_ok=True)

# =========================
# LOAD DATA
# =========================
print("Cargando datos...")
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

# División train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN (Random Forest)
# =========================
"""
Random Forest:
Modelo basado en múltiples árboles de decisión.

Cada árbol aprende reglas no lineales y el resultado final
es el promedio de todos los árboles.

Ventajas:
- Captura relaciones no lineales
- Robusto a ruido
- No necesita escalado
"""

print("Entrenando Random Forest...")
start_time = time.time()

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=None,
    n_jobs=-1,        # usa todos los núcleos
    random_state=42
)

model.fit(X_train, y_train)

end_time = time.time()
training_time = end_time - start_time

# =========================
# EVALUATE
# =========================
print("Evaluando modelo...")
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100

# =========================
# FEATURE IMPORTANCE
# =========================
"""
Importancia de variables (clave en Random Forest)
"""

importances = model.feature_importances_
feature_names = X.columns

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

# Guardar top features
importance_df.head(20).to_csv(
    os.path.join(RESULTS_DIR, "feature_importance_top20.csv"),
    index=False
)

# =========================
# SAVE MODEL
# =========================
model_path = os.path.join(MODEL_DIR, "model.pkl")
joblib.dump(model, model_path)

# =========================
# SAVE METRICS (MD)
# =========================
md_content = f"""
# Resultados - Random Forest

| Métrica | Valor |
|--------|------|
| MAE | {mae:.4f} |
| RMSE | {rmse:.4f} |
| R² | {r2:.4f} |
| MAPE (%) | {mape:.2f} |
| Tiempo (s) | {training_time:.2f} |

## Interpretación

Modelo no lineal basado en ensamble de árboles.
"""

with open(os.path.join(RESULTS_DIR, "metrics_random_forest.md"), "w") as f:
    f.write(md_content)

# =========================
# SAVE GLOBAL CSV
# =========================
row = pd.DataFrame([{
    "model": MODEL_NAME,
    "mae": mae,
    "rmse": rmse,
    "r2": r2,
    "mape": mape,
    "time_sec": training_time
}])

if os.path.exists(GLOBAL_RESULTS):
    row.to_csv(GLOBAL_RESULTS, mode="a", header=False, index=False)
else:
    row.to_csv(GLOBAL_RESULTS, index=False)

# =========================
# DONE
# =========================
print("Modelo Random Forest entrenado y guardado correctamente.")
print(f"MAE: {mae:.4f} | RMSE: {rmse:.4f} | R2: {r2:.4f}")