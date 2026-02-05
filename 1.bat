@echo off
TITLE Protocolo de Emergencia MLflow
chcp 65001 >nul

ECHO =================================================
ECHO 🚑 PROTOCOLO DE EMERGENCIA: LIMPIEZA TOTAL
ECHO =================================================
ECHO.

ECHO 1. 🛑 Matando procesos de Python y MLflow (Zombie Killer)...
:: Esto asegura que nadie esté bloqueando el archivo mlflow.db
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM mlflow.exe /T 2>nul

ECHO.
ECHO 2. 🧹 Eliminando archivos corruptos o antiguos...
:: Borrado en la raíz
IF EXIST "mlflow.db" (
    DEL /F /Q "mlflow.db"
    ECHO    - mlflow.db eliminado.
)
IF EXIST "mlruns" (
    RMDIR /S /Q "mlruns"
    ECHO    - Carpeta mlruns eliminada.
)
IF EXIST "scaler.pkl" (
    DEL /F /Q "scaler.pkl"
    ECHO    - scaler.pkl eliminado.
)

:: Borrado de seguridad en subcarpetas (por si acaso)
IF EXIST "Notebooks\mlflow.db" DEL /F /Q "Notebooks\mlflow.db"
IF EXIST "Notebooks\mlruns" RMDIR /S /Q "Notebooks\mlruns"
IF EXIST "app\mlflow.db" DEL /F /Q "app\mlflow.db"

ECHO.
ECHO 3. 🧠 Regenerando el Cerebro (Modelo + Base de Datos nueva)...
:: Aseguramos que el entorno virtual esté activo
IF EXIST "venv\Scripts\activate.bat" (
    CALL venv\Scripts\activate.bat
) ELSE (
    ECHO ⚠️ No encuentro el entorno virtual 'venv'. Intentando seguir...
)

:: Ejecutamos el entrenamiento inicial (Esto crea la DB correcta)
python train_initial_model.py

IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO ❌ ALERTA: El entrenamiento inicial falló o no encontró 'train_initial_model.py'.
    ECHO    Asegúrate de haber creado ese archivo en el paso anterior.
    PAUSE
    EXIT
)

ECHO.
ECHO 4. 🚀 Iniciando Sistema Limpio...
python run.py

PAUSE