import subprocess
import time
import webbrowser
import os
import sys

# --- 1. Importación de Configuración Robusta ---
# Agregamos la ruta actual al path para asegurar que encuentre el módulo app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.app_config import MLFLOW_DB_PATH, PROJECT_ROOT
except ImportError:
    # Fallback de seguridad si falla la importación
    print("⚠️ No se pudo importar app_config. Usando rutas por defecto.")
    PROJECT_ROOT = os.getcwd()
    MLFLOW_DB_PATH = f"sqlite:///{os.path.join(PROJECT_ROOT, 'mlflow.db')}"

# Configuración de Puertos
API_PORT = 8000
MLFLOW_PORT = 5000
HOST = "127.0.0.1"

def main():
    print(f"🚀 Iniciando Sistema de Salud Materna...")
    print(f"📂 Raíz del Proyecto: {PROJECT_ROOT}")
    print("=========================================================")

    # --- PASO 0: AUTOREPARACIÓN DE BASE DE DATOS (NUEVO) ---
    # Esto evita el error "Detected out-of-date database schema"
    print(f"🔧 Verificando estado de la base de datos...")
    upgrade_cmd = f'mlflow db upgrade "{MLFLOW_DB_PATH}"'
    
    # Ejecutamos y esperamos a que termine antes de continuar
    exit_code = os.system(upgrade_cmd)
    if exit_code == 0:
        print("✅ Base de datos verificada y actualizada.")
    else:
        print("⚠️ Advertencia: La actualización de la BD reportó un código no cero.")
    print("=========================================================")

    # --- PASO 1: Iniciar MLflow UI ---
    print(f"📊 Arrancando servidor MLflow en puerto {MLFLOW_PORT}...")
    mlflow_cmd = [
        "mlflow", "ui",
        "--backend-store-uri", MLFLOW_DB_PATH, # Usamos la variable de config
        "--host", HOST,
        "--port", str(MLFLOW_PORT)
    ]
    
    # cwd=PROJECT_ROOT asegura que se ejecute en la carpeta correcta
    mlflow_process = subprocess.Popen(mlflow_cmd, shell=True, cwd=PROJECT_ROOT)

    # --- PASO 2: Iniciar FastAPI (Uvicorn) ---
    print(f"⚡ Arrancando API en puerto {API_PORT}...")
    api_cmd = [
        "uvicorn", "app.main:app",
        "--host", HOST,
        "--port", str(API_PORT),
        "--reload"
    ]
    api_process = subprocess.Popen(api_cmd, shell=True, cwd=PROJECT_ROOT)

    # --- PASO 3: Esperar y Abrir Navegador ---
    print("⏳ Esperando 5 segundos para cargar servicios...")
    time.sleep(5)

    print("🌐 Abriendo interfaces en el navegador...")
    
    # Abre la App Web (Predicción)
    webbrowser.open(f"http://{HOST}:{API_PORT}")
    
    # Abre la UI de MLflow (Historial)
    webbrowser.open(f"http://{HOST}:{MLFLOW_PORT}")

    print("\n✅ SISTEMA COMPLETAMENTE EN LÍNEA.")
    print("---------------------------------------------------------")
    print(f"   👉 App Principal: http://{HOST}:{API_PORT}")
    print(f"   👉 MLflow UI:     http://{HOST}:{MLFLOW_PORT}")
    print("---------------------------------------------------------")
    print("Presiona Ctrl+C en esta ventana para cerrar todo.\n")

    try:
        # Mantener el script vivo vigilando los procesos
        while True:
            time.sleep(2)
            if api_process.poll() is not None:
                print("❌ La API se ha detenido.")
                break
            if mlflow_process.poll() is not None:
                print("❌ MLflow se ha detenido.")
                break

    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servicios...")
    finally:
        # Matar procesos al salir
        # Usamos taskkill forzado para asegurar que no queden fantasmas
        try:
            subprocess.call(["taskkill", "/F", "/T", "/PID", str(api_process.pid)], stderr=subprocess.DEVNULL)
            subprocess.call(["taskkill", "/F", "/T", "/PID", str(mlflow_process.pid)], stderr=subprocess.DEVNULL)
        except:
            pass
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()