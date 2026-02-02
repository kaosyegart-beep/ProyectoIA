import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import mlflow
import os
import shutil
from pathlib import Path
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# --- Configuración de Rutas ---
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "maternal_risk_processed.csv"
DB_PATH = PROJECT_ROOT / "mlflow.db"
MLRUNS_PATH = PROJECT_ROOT / "mlruns"

def clean_environment():
    """Borra la base de datos y carpeta de logs para empezar de 0"""
    print("🧹 Limpiando historial antiguo...")
    if DB_PATH.exists():
        os.remove(DB_PATH)
    if MLRUNS_PATH.exists():
        shutil.rmtree(MLRUNS_PATH)
    print("✨ Ambiente limpio.")

def train_base_model():
    print(f"🚀 Iniciando entrenamiento base (MODO DEMO)...")
    
    # Configurar MLflow
    mlflow.set_tracking_uri(f"sqlite:///{DB_PATH}")
    mlflow.set_experiment("Maternal_Health_Project")

    # 1. Cargar Datos
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encuentra: {DATA_PATH}")
    
    df = pd.read_csv(DATA_PATH)
    X = df.drop(['RiskLevel', 'Risk_Num'], axis=1)
    y = df['Risk_Num']

    # 2. Escalar
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # 3. Definir Modelo (Configuración 'Weak' para permitir mejoras visibles)
    model = Sequential([
        Dense(16, activation='relu', input_shape=(X_train.shape[1],)),
        Dropout(0.2), # Dropout alto para dificultar el aprendizaje inicial
        Dense(8, activation='relu'),
        Dense(3, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # 4. Entrenar y Registrar
    with mlflow.start_run(run_name="Base_Model_Weak_Start") as run:
        
        # Entrenamos pocas épocas (10) para dejar margen de mejora
        history = model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=0)
        
        # Evaluar
        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
        
        # LOGUEAR MÉTRICAS (Vital para las gráficas)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("loss", loss)
        mlflow.log_param("mode", "demo_initialization")
        
        # Generar Firma (Signature)
        predictions = model.predict(X_train[:5])
        signature = infer_signature(X_train, predictions)

        # Guardar Artefactos
        joblib.dump(scaler, "scaler.pkl")
        mlflow.log_artifact("scaler.pkl")
        
        mlflow.tensorflow.log_model(
            model, 
            "model", 
            signature=signature
        )
        
        print(f"📉 Modelo Base Entrenado.")
        print(f"📊 Accuracy Inicial: {accuracy:.4f}")
        print(f"🆔 Run ID: {run.info.run_id}")

if __name__ == "__main__":
    clean_environment()
    train_base_model()