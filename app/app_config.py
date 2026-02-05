import os

# --- 1. DEFINICIÓN DE RUTAS ABSOLUTAS ---
# Obtener la ruta absoluta de la carpeta donde está este archivo (app/)
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Obtener la raíz del proyecto (subiendo un nivel desde app/)
PROJECT_ROOT = os.path.dirname(APP_DIR)

# --- CONFIGURACIÓN DE MLFLOW ---
# Definir la ruta de la base de datos SIEMPRE en la raíz
DB_PATH = os.path.join(PROJECT_ROOT, 'mlflow.db')

# URI correcta para SQLite en Windows (sqlite:///ruta/absoluta)
# En Windows a veces requiere 3 o 4 barras, usamos el estándar seguro:
MLFLOW_DB_PATH = f"sqlite:///{DB_PATH}"

# Definir dónde se guardan los artefactos (mlruns) SIEMPRE en la raíz
MLRUNS_DIR = os.path.join(PROJECT_ROOT, 'mlruns')

# --- CONFIGURACIÓN DEL MODELO Y SCALER ---
EXPERIMENT_NAME = "Maternal_Health_Risk"
MODEL_ARTIFACT_PATH = "model"

# Definir ruta absoluta para el scaler (para que no se cree en Notebooks/)
SCALER_FILE_NAME = "scaler.pkl"
SCALER_PATH = os.path.join(PROJECT_ROOT, SCALER_FILE_NAME)

# --- MAPEOS Y CONFIGURACIÓN DE DATOS ---
RISK_MAP = {
    0: "low risk",
    1: "mid risk",
    2: "high risk"
}
RISK_INVERSE_MAPPING = {v: k for k, v in RISK_MAP.items()}

FEATURE_NAMES = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']