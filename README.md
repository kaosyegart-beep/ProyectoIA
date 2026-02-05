# Maternal Health Risk Prediction with AI and Continuous Learning

This project is a comprehensive MLOps solution designed to predict maternal health risk levels (Low, Medium, High) based on vital signs and physiological data. It implements a complete Machine Learning lifecycle, from exploratory analysis to deploying an API with real-time retraining capabilities (Continuous Learning).

## Technologies Used

The project is built using a modern Python stack for Data Science and Web Development:

* **Language:** Python 3.10+
* **Machine Learning & Deep Learning:**
    * `TensorFlow` / `Keras` (Neural Networks)
    * `Scikit-Learn` (Preprocessing and metrics)
    * `Pandas` & `NumPy` (Data manipulation)
* **MLOps & Tracking:**
    * `MLflow` (Experiment tracking, model versioning and artifact management)
* **Backend & API:**
    * `FastAPI` (High-performance web server)
    * `Uvicorn` (ASGI server)
    * `Pydantic` (Data validation)
* **Frontend:**
    * `HTML5` + `Jinja2` (Templates)
    * `TailwindCSS` (Modern styling via CDN)
* **Tools:**
    * `Joblib` (Serialization)
    * `Matplotlib` & `Seaborn` (Data visualization in Notebooks)

## Project Structure

```
Proyecto/
|
├── app/                        # Application source code
│   ├── templates/              # User interface (HTML)
│   │   └── index.html
│   ├── __init__.py
│   ├── config.py               # Configuration and paths
│   ├── main.py                 # API endpoints (FastAPI)
│   ├── ml_service.py           # Model loading and retraining logic
│   └── schemas.py              # Data models (Pydantic)
│
├── data/                       # Datasets
│   ├── Maternal Health Risk Data Set.csv  # Raw data
│   └── maternal_risk_processed.csv        # Processed data
│
├── Notebooks/                  # Jupyter Notebooks
│   ├── 01_EDA.ipynb            # Exploratory Data Analysis
│   ├── 02_Training_Base.ipynb  # Base model training and MLflow registration
│   └── 03_Inference_Testing.ipynb # Inference tests and feedback simulation
│
├── mlflow.db                   # MLflow SQLite database (auto-generated)
├── mlruns/                     # MLflow artifacts (models, scalers)
├── iniciar.bat                 # Automated startup script for Windows
├── run.py                      # Service orchestrator (API + MLflow)
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation
```

## Project Summary and Functionality

The main objective is to assist in early diagnosis of pregnancy-related risks through artificial intelligence.

### The Model
The core of the system is an **Artificial Neural Network (ANN)** built with TensorFlow/Keras.
* **Architecture:** Sequential model with dense layers (`Dense`), `ReLU` activation and regularization layers (`Dropout`) to prevent overfitting.
* **Output:** `Softmax` layer that classifies into 3 categories: *Low Risk, Mid Risk, High Risk*.

### Workflow

1. **Base Training:** Through the Notebooks, data is processed and the initial model is trained. This model, along with its scaler (`StandardScaler`) and input/output signature, is automatically registered in **MLflow Model Registry** with a timestamp-based version name (e.g., `model_v0402262258`).

2. **Inference (API):** When the application starts, the service automatically searches for the latest registered model version in MLflow and loads it into memory using `mlflow.load_model()`.

3. **Continuous Learning (Feedback Loop):**
    * The system allows the user (doctor/specialist) to correct an incorrect prediction from the web interface.
    * **Fine-Tuning:** Upon receiving a correction, the system executes a *Transfer Learning* process. It freezes the base layers of the model to retain previous knowledge and retrains the deep layers with the new data using an aggressive learning rate.
    * **Versioning:** The adjusted model is immediately saved as a new version in MLflow with the format `model_v{ddmmyyHHMM}` and the API updates in real-time without needing to restart.

## How to Start

The project includes an automated script for Windows that manages virtual environment creation, dependency installation, and server startup.

1. Make sure Python is installed.
2. Double-click the **`iniciar.bat`** file.
3. The system will automatically open:
    * The prediction web interface.
    * (Optional) Access the MLflow UI on port 5000 to view training history.

## Author

* **Richard Borja** - Kaosyegart@gmail.com