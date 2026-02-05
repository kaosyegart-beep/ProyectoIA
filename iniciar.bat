@echo off
:: Set encoding to UTF-8 to support emojis
chcp 65001 >nul
TITLE Maternal Health AI Manager
SET VENV_NAME=venv

ECHO ==========================================
ECHO      STARTING MATERNAL HEALTH AI SYSTEM
ECHO ==========================================
ECHO.

:: 1. Check if virtual environment exists
IF NOT EXIST "%VENV_NAME%" (
    ECHO ⚠️  Virtual environment '%VENV_NAME%' not found.
    ECHO 🔨 Creating virtual environment...
    python -m venv %VENV_NAME%
    
    ECHO 🐍 Activating environment for the first time...
    CALL %VENV_NAME%\Scripts\activate.bat
    
    ECHO 📦 Installing dependencies from requirements.txt...
    :: Upgrade pip just in case
    python -m pip install --upgrade pip
    
    IF EXIST "requirements.txt" (
        pip install -r requirements.txt
    ) ELSE (
        ECHO ❌ ERROR: requirements.txt file not found.
        PAUSE
        EXIT
    )
    
    ECHO ✅ Installation complete.
    
) ELSE (
    ECHO ✅ Virtual environment '%VENV_NAME%' detected.
    CALL %VENV_NAME%\Scripts\activate.bat
)

:: 2. Run the orchestrator
ECHO.
ECHO 🚀 Launching the application...
python run.py

PAUSE