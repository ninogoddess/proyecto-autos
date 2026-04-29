import os
import time
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# =========================
# CONFIG
# =========================
MODEL_NAME = "linear_regression"

DATA_PATH = "data/processed/vehicles_processed.csv"  
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

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN
# =========================
print("Entrenando modelo...")
start_time = time.time()

model = LinearRegression()
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

# MAPE (evitando división por 0)
mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100

# =========================
# SAVE MODEL
# =========================
model_path = os.path.join(MODEL_DIR, "model.pkl")
joblib.dump(model, model_path)

# =========================
# SAVE METRICS (MD)
# =========================
md_content = f"""
# Resultados - Linear Regression

| Métrica | Valor |
|--------|------|
| MAE | {mae:.4f} |
| RMSE | {rmse:.4f} |
| R² | {r2:.4f} |
| MAPE (%) | {mape:.2f} |
| Tiempo (s) | {training_time:.2f} |
"""

with open(os.path.join(RESULTS_DIR, "metrics.md"), "w") as f:
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
print("Modelo entrenado y guardado correctamente.")
print(f"MAE: {mae:.2f} | RMSE: {rmse:.2f} | R2: {r2:.4f}")