# 🤰 Predicción de Riesgo de Salud Materna con IA y Aprendizaje Continuo

Este proyecto es una solución integral de MLOps diseñada para predecir el nivel de riesgo de salud materna (Bajo, Medio, Alto) basándose en signos vitales y datos fisiológicos. Implementa un ciclo de vida completo de Machine Learning, desde el análisis exploratorio hasta el despliegue de una API con capacidades de re-entrenamiento en tiempo real (Continuous Learning).

## 🛠️ Tecnologías Utilizadas

El proyecto está construido utilizando un stack moderno de Python para Data Science y Desarrollo Web:

* **Lenguaje:** Python 3.10+
* **Machine Learning & Deep Learning:**
    * `TensorFlow` / `Keras` (Redes Neuronales)
    * `Scikit-Learn` (Preprocesamiento y métricas)
    * `Pandas` & `NumPy` (Manipulación de datos)
* **MLOps & Tracking:**
    * `MLflow` (Registro de experimentos, versionado de modelos y gestión de artefactos)
* **Backend & API:**
    * `FastAPI` (Servidor web de alto rendimiento)
    * `Uvicorn` (Servidor ASGI)
    * `Pydantic` (Validación de datos)
* **Frontend:**
    * `HTML5` + `Jinja2` (Templates)
    * `TailwindCSS` (Estilizado moderno vía CDN)
* **Herramientas:**
    * `Joblib` (Serialización)
    * `Matplotlib` & `Seaborn` (Visualización de datos en Notebooks)

## 📂 Estructura del Proyecto

Proyecto/
│
├── app/                        # Código fuente de la aplicación
│   ├── templates/              # Interfaz de usuario (HTML)
│   │   └── index.html
│   ├── __init__.py
│   ├── config.py               # Configuraciones y rutas
│   ├── main.py                 # Endpoints de la API (FastAPI)
│   ├── ml_service.py           # Lógica de carga de modelos y re-entrenamiento
│   └── schemas.py              # Modelos de datos (Pydantic)
│
├── data/                       # Datasets
│   ├── Maternal Health Risk Data Set.csv  # Datos crudos
│   └── maternal_risk_processed.csv        # Datos procesados
│
├── Notebooks/                  # Cuadernos de Jupyter
│   ├── 01_EDA.ipynb            # Análisis Exploratorio de Datos
│   ├── 02_Training_Base.ipynb  # Entrenamiento del modelo base y registro en MLflow
│   └── 03_Inference_Testing.ipynb # Pruebas de inferencia y simulación de feedback
│
├── mlflow.db                   # Base de datos SQLite de MLflow (se genera automáticamente)
├── mlruns/                     # Artefactos de MLflow (modelos, scalers)
├── iniciar.bat                 # Script de arranque automático para Windows
├── run.py                      # Orquestador de servicios (API + MLflow)
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Documentación

## 📝 Resumen del Proyecto y Funcionamiento

El objetivo principal es asistir en el diagnóstico temprano de riesgos durante el embarazo mediante inteligencia artificial.

### 🧠 El Modelo
El núcleo del sistema es una **Red Neuronal Artificial (ANN)** construida con TensorFlow/Keras.
* **Arquitectura:** Modelo secuencial con capas densas (`Dense`), activación `ReLU` y capas de regularización (`Dropout`) para evitar sobreajuste.
* **Salida:** Capa `Softmax` que clasifica en 3 categorías: *Low Risk, Mid Risk, High Risk*.

### ⚙️ Flujo de Trabajo (Workflow)

1.  **Entrenamiento Base:** A través de los Notebooks, se procesan los datos y se entrena el modelo inicial. Este modelo, junto con su escalador (`StandardScaler`) y su firma de entrada/salida, se registra automáticamente en **MLflow**.
2.  **Inferencia (API):** Al iniciar la aplicación, el servicio busca automáticamente la versión más reciente y exitosa del modelo en MLflow y la carga en memoria.
3.  **Aprendizaje Continuo (Feedback Loop):**
    * El sistema permite al usuario (médico/especialista) corregir una predicción errónea desde la interfaz web.
    * **Fine-Tuning:** Al recibir una corrección, el sistema ejecuta un proceso de *Transfer Learning*. Congela las capas superficiales del modelo para retener el conocimiento previo y re-entrena las capas profundas con el nuevo dato usando una tasa de aprendizaje agresiva.
    * **Versionado:** El modelo ajustado se guarda inmediatamente como una nueva versión en MLflow y la API se actualiza en tiempo real sin necesidad de reiniciarse.

## 🚀 Cómo Iniciar

El proyecto incluye un script automatizado para Windows que gestiona la creación del entorno virtual, la instalación de dependencias y el inicio de los servidores.

1.  Asegúrate de tener Python instalado.
2.  Haz doble clic en el archivo **`iniciar.bat`**.
3.  El sistema abrirá automáticamente:
    * La interfaz web de predicción.
    * (Opcional) Puedes acceder a la UI de MLflow en el puerto 5000 para ver el historial de entrenamientos.

## 👥 Autores

* **[Tu Nombre Aquí]** - *Desarrollo Inicial y MLOps*
* **[Nombre Colaborador]** - *Análisis de Datos*