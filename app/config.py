import os
from pathlib import Path

# Rutas base
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
MLFLOW_DB_PATH = f"sqlite:///{PROJECT_ROOT}/mlflow.db"

# Configuración del Modelo
EXPERIMENT_NAME = "Maternal_Health_Project"
MODEL_ARTIFACT_PATH = "model"
SCALER_ARTIFACT_PATH = "scaler.pkl"

# Mapeo de Riesgos (Inverso al del entrenamiento)
RISK_MAP = {0: "low risk", 1: "mid risk", 2: "high risk"}