import mlflow
import mlflow.tensorflow
import joblib
import numpy as np
import tensorflow as tf
from mlflow.tracking import MlflowClient
from mlflow.models.signature import infer_signature
from datetime import datetime
import os

# Importamos las rutas absolutas desde nuestra config corregida
try:
    from app.app_config import (
        MLFLOW_DB_PATH, 
        MLRUNS_DIR, 
        EXPERIMENT_NAME, 
        MODEL_ARTIFACT_PATH, 
        SCALER_PATH
    )
except ImportError:
    # Fallback por si se ejecuta desde dentro de la carpeta app
    from app_config import (
        MLFLOW_DB_PATH, 
        MLRUNS_DIR, 
        EXPERIMENT_NAME, 
        MODEL_ARTIFACT_PATH, 
        SCALER_PATH
    )

class MLService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.run_id = None
        
        # 1. Configurar MLflow con rutas absolutas
        print(f"🔧 Configurando MLflow en: {MLFLOW_DB_PATH}")
        mlflow.set_tracking_uri(MLFLOW_DB_PATH)
        
        # IMPORTANTE: Forzar la ubicación de mlruns
        # (Aunque set_tracking_uri con sqlite suele manejarlo, esto asegura que 
        # los artefactos locales vayan al sitio correcto si no usamos servidor remoto)
        # mlflow.set_registry_uri(MLFLOW_DB_PATH) 

        mlflow.set_experiment(EXPERIMENT_NAME)
        
        # 2. Cargar recursos
        self.load_latest_model()

    def load_latest_model(self):
        """Busca y carga el modelo más reciente del Registry y el Scaler del disco"""
        print("🔄 Buscando modelo más reciente...")
        client = MlflowClient()
        
        try:
            # Intentar cargar el Scaler desde la ruta ABSOLUTA
            if os.path.exists(SCALER_PATH):
                self.scaler = joblib.load(SCALER_PATH)
                print(f"✅ Scaler cargado desde: {SCALER_PATH}")
            else:
                print(f"⚠️ Scaler no encontrado en: {SCALER_PATH}")

            # Buscar modelo en MLflow
            registered_models = client.search_registered_models()
            latest_model = None
            latest_timestamp = None
            
            for model in registered_models:
                if model.name.startswith("model_v"):
                    try:
                        timestamp_str = model.name.replace("model_v", "")
                        timestamp = datetime.strptime(timestamp_str, "%d%m%y%H%M")
                        if latest_timestamp is None or timestamp > latest_timestamp:
                            latest_model = model.name
                            latest_timestamp = timestamp
                    except ValueError:
                        continue
            
            if latest_model:
                model_uri = f"models:/{latest_model}/latest"
                self.model = mlflow.tensorflow.load_model(model_uri)
                self.run_id = latest_model
                print(f"✅ Modelo cargado: {latest_model}")
            else:
                print("⚠️ No se encontraron modelos registrados.")
                
        except Exception as e:
            print(f"❌ Error cargando recursos: {e}")

    def prepare_data(self, data_dict):
        if not self.scaler:
            raise Exception("Scaler not loaded.")
        features = [
            data_dict['Age'], data_dict['SystolicBP'], data_dict['DiastolicBP'],
            data_dict['BS'], data_dict['BodyTemp'], data_dict['HeartRate']
        ]
        return self.scaler.transform([features])

    def predict(self, data_dict):
        if not self.model:
            self.load_latest_model()
        
        scaled_data = self.prepare_data(data_dict)
        pred = self.model.predict(scaled_data, verbose=0)
        class_idx = np.argmax(pred)
        confidence = float(pred[0][class_idx])
        return class_idx, confidence

    def fine_tune(self, data_dict, actual_label_str):
        print(f"🧠 Re-entrenando para: {actual_label_str}")
        
        risk_map_inv = {"low risk": 0, "mid risk": 1, "high risk": 2}
        label = risk_map_inv.get(actual_label_str.lower())
        
        if label is None: raise ValueError("Etiqueta inválida")

        scaled_data = self.prepare_data(data_dict)
        y_true = np.array([label])
        
        # Transfer Learning
        for layer in self.model.layers[:-1]:
            layer.trainable = False
            
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        history = self.model.fit(scaled_data, y_true, epochs=5, verbose=1)
        
        # Generar nombre
        timestamp = datetime.now().strftime("%d%m%y%H%M")
        model_name = f"model_v{timestamp}"
        
        with mlflow.start_run(run_name="App_Retrain") as run:
            mlflow.log_param("trigger", "user_correction")
            mlflow.log_metric("accuracy", history.history['accuracy'][-1])
            
            # Guardar MODELO en MLflow
            signature = infer_signature(scaled_data, self.model.predict(scaled_data, verbose=0))
            model_info = mlflow.tensorflow.log_model(
                self.model, 
                MODEL_ARTIFACT_PATH,
                signature=signature
            )
            
            # Guardar SCALER en la RUTA ABSOLUTA (Disco)
            joblib.dump(self.scaler, SCALER_PATH)
            print(f"💾 Scaler actualizado en: {SCALER_PATH}")
            
            # Registrar modelo
            mlflow.register_model(model_info.model_uri, model_name)
            
            return run.info.run_id

# Instancia global
ml_service = MLService()