@echo off
TITLE Maternal Health AI Manager
SET VENV_NAME=venv

ECHO ==========================================
ECHO      INICIANDO SISTEMA DE SALUD MATERNA
ECHO ==========================================
ECHO.

:: 1. Verificar si existe el entorno virtual
IF NOT EXIST "%VENV_NAME%" (
    ECHO ⚠️  No se encontro el entorno virtual '%VENV_NAME%'.
    ECHO 🔨 Creando entorno virtual...
    python -m venv %VENV_NAME%
    
    ECHO 🐍 Activando entorno por primera vez...
    CALL %VENV_NAME%\Scripts\activate.bat
    
    ECHO 📦 Instalando dependencias desde requirements.txt...
    :: Actualizamos pip por si acaso
    python -m pip install --upgrade pip
    
    IF EXIST "requirements.txt" (
        pip install -r requirements.txt
    ) ELSE (
        ECHO ❌ ERROR: No se encontro el archivo requirements.txt
        PAUSE
        EXIT
    )
    
    ECHO ✅ Instalacion completada.
    
) ELSE (
    ECHO ✅ Entorno virtual '%VENV_NAME%' detectado.
    CALL %VENV_NAME%\Scripts\activate.bat
)

:: 2. Ejecutar el orquestador
ECHO.
ECHO 🚀 Arrancando la aplicacion...
python run.py

PAUSE