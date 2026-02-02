import mlflow
import joblib
import numpy as np
import tensorflow as tf
from mlflow.tracking import MlflowClient
from mlflow.models.signature import infer_signature

# Importación Absoluta (Soluciona el error de rutas)
from app.config import MLFLOW_DB_PATH, EXPERIMENT_NAME, MODEL_ARTIFACT_PATH, SCALER_ARTIFACT_PATH

class MLService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.run_id = None
        
        # Configurar MLflow
        mlflow.set_tracking_uri(MLFLOW_DB_PATH)
        mlflow.set_experiment(EXPERIMENT_NAME)
        
        self.load_latest_model()

    def load_latest_model(self):
        """Busca y carga el último modelo exitoso desde MLflow"""
        print("🔄 Buscando modelo más reciente en MLflow...")
        client = MlflowClient()
        
        # Obtener el experimento
        experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
        if not experiment:
            print("⚠️ No se encontró el experimento. Ejecuta train.py primero.")
            return

        # Buscar el último run exitoso
        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["attributes.start_time DESC"],
            max_results=1
        )
        
        if not runs:
            print("⚠️ No hay runs registrados todavía.")
            return

        last_run = runs[0]
        self.run_id = last_run.info.run_id
        
        # Cargar Modelo Keras y Scaler
        try:
            model_uri = f"runs:/{self.run_id}/{MODEL_ARTIFACT_PATH}"
            self.model = mlflow.tensorflow.load_model(model_uri)
            print(f"✅ Modelo cargado: {self.run_id}")
            
            local_path = client.download_artifacts(self.run_id, SCALER_ARTIFACT_PATH, ".")
            self.scaler = joblib.load(local_path)
            print("✅ Scaler cargado.")
            
        except Exception as e:
            print(f"❌ Error cargando artefactos: {e}")

    def prepare_data(self, data_dict):
        if not self.scaler:
            raise Exception("Scaler no cargado.")
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
        """
        Re-entrenamiento agresivo para demostración.
        """
        print(f"🧠 Re-entrenando (Fine-Tuning) para: {actual_label_str}")
        
        # Mapeo inverso
        risk_map_inv = {"low risk": 0, "mid risk": 1, "high risk": 2}
        label = risk_map_inv.get(actual_label_str.lower())
        
        if label is None:
            raise ValueError("Etiqueta de riesgo inválida")

        # Preparar datos
        scaled_data = self.prepare_data(data_dict)
        y_true = np.array([label])
        
        # Estrategia de Transfer Learning: Congelar capas base
        for layer in self.model.layers[:-1]:
            layer.trainable = False
            
        # Compilación Agresiva (LR alto)
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Entrenar capturando historial
        history = self.model.fit(scaled_data, y_true, epochs=10, verbose=0)
        
        # Extraer métricas finales
        final_loss = history.history['loss'][-1]
        final_accuracy = history.history['accuracy'][-1]
        
        # Guardar nueva versión en MLflow
        with mlflow.start_run(run_name="App_Retrain_Event") as run:
            mlflow.log_param("event", "user_correction")
            mlflow.log_param("trigger_label", actual_label_str)
            
            # LOGUEAR MÉTRICAS (Para ver la curva en la UI)
            mlflow.log_metric("loss", final_loss)
            mlflow.log_metric("accuracy", final_accuracy)
            
            # Generar nueva firma
            pred_new = self.model.predict(scaled_data)
            signature = infer_signature(scaled_data, pred_new)

            # Guardar Modelo y Scaler
            mlflow.tensorflow.log_model(
                self.model, 
                MODEL_ARTIFACT_PATH, 
                signature=signature
            )
            joblib.dump(self.scaler, "scaler.pkl")
            mlflow.log_artifact("scaler.pkl")
            
            new_run_id = run.info.run_id
            
        print(f"🚀 Modelo actualizado. Accuracy local: {final_accuracy:.2f}. Run ID: {new_run_id}")
        
        self.run_id = new_run_id
        return new_run_id

ml_service = MLService()