@echo off
TITLE REINICIANDO PROYECTO A CERO
ECHO ==========================================
ECHO      ⚠️  PELIGRO: RESET DE FABRICA  ⚠️
ECHO ==========================================
ECHO Esto borrara todo el historial de MLflow y entrenara
ECHO el modelo base desde cero.
ECHO.
PAUSE

:: Activar entorno (si se llama venv)
IF EXIST "venv\Scripts\activate.bat" CALL venv\Scripts\activate.bat

:: Ejecutar el script de entrenamiento
python train.py

ECHO.
ECHO ✅ Reinicio completado. Ya puedes ejecutar iniciar.bat
PAUSE