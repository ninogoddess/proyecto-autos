import os
import time
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# =========================
# CONFIG
# =========================
MODEL_NAME = "lasso"

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
# TRAIN (Lasso)
# =========================
"""
Lasso Regression:
Modelo lineal con regularización L1.

La penalización L1 puede hacer que algunos coeficientes
se vuelvan exactamente 0 → selección automática de variables.
"""

print("Entrenando modelo Lasso...")
start_time = time.time()

model = Lasso(alpha=0.001, max_iter=10000)  
# alpha pequeño para no destruir el modelo
# max_iter alto para asegurar convergencia

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
# FEATURE SELECTION INFO
# =========================
"""
Conteo de variables eliminadas (coeficientes = 0)
Esto es clave en Lasso
"""

coefficients = model.coef_
zero_features = np.sum(coefficients == 0)
total_features = len(coefficients)

# =========================
# SAVE MODEL
# =========================
model_path = os.path.join(MODEL_DIR, "model.pkl")
joblib.dump(model, model_path)

# =========================
# SAVE METRICS (MD)
# =========================
md_content = f"""
# Resultados - Lasso Regression

| Métrica | Valor |
|--------|------|
| MAE | {mae:.4f} |
| RMSE | {rmse:.4f} |
| R² | {r2:.4f} |
| MAPE (%) | {mape:.2f} |
| Tiempo (s) | {training_time:.2f} |

## Selección de variables

| Concepto | Valor |
|----------|------|
| Features eliminadas | {zero_features} |
| Total features | {total_features} |
| % eliminadas | {(zero_features / total_features) * 100:.2f}% |
"""

with open(os.path.join(RESULTS_DIR, "metrics_lasso.md"), "w") as f:
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
print("Modelo Lasso entrenado y guardado correctamente.")
print(f"MAE: {mae:.4f} | RMSE: {rmse:.4f} | R2: {r2:.4f}")
print(f"Features eliminadas: {zero_features}/{total_features}")