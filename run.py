import subprocess
import time
import webbrowser
import os
import sys

# Configuración de Puertos
API_PORT = 8000
MLFLOW_PORT = 5000
HOST = "127.0.0.1"

def main():
    print(f"🚀 Iniciando Sistema de Salud Materna...")
    print(f"📂 Directorio actual: {os.getcwd()}")

    # 1. Comando para iniciar MLflow UI
    # Apunta a la base de datos sqlite en la raíz
    print(f"📊 Arrancando servidor MLflow en puerto {MLFLOW_PORT}...")
    mlflow_cmd = [
        "mlflow", "ui",
        "--backend-store-uri", "sqlite:///mlflow.db",
        "--host", HOST,
        "--port", str(MLFLOW_PORT)
    ]
    # Shell=True para compatibilidad con Windows
    mlflow_process = subprocess.Popen(mlflow_cmd, shell=True)

    # 2. Comando para iniciar FastAPI (Uvicorn)
    print(f"⚡ Arrancando API en puerto {API_PORT}...")
    api_cmd = [
        "uvicorn", "app.main:app",
        "--host", HOST,
        "--port", str(API_PORT),
        "--reload"
    ]
    api_process = subprocess.Popen(api_cmd, shell=True)

    # 3. Esperar a que los servidores calienten motores
    print("⏳ Esperando 5 segundos para cargar servicios...")
    time.sleep(5)

    # 4. Abrir el navegador automáticamente
    print("🌐 Abriendo interfaces en el navegador...")
    
    # Abre la App Web (Predicción)
    webbrowser.open(f"http://{HOST}:{API_PORT}")
    
    # Abre la UI de MLflow (Historial de experimentos)
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
            # Si alguno de los dos procesos muere, avisar
            if api_process.poll() is not None:
                print("❌ La API se ha detenido.")
                break
            if mlflow_process.poll() is not None:
                print("❌ MLflow se ha detenido.")
                break

    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servicios...")
    finally:
        # Intentar matar los procesos al salir
        # Nota: En Windows a veces es necesario cerrar la ventana manualmente
        # para matar subprocesos persistentes, pero esto ayuda.
        subprocess.call(["taskkill", "/F", "/T", "/PID", str(api_process.pid)])
        subprocess.call(["taskkill", "/F", "/T", "/PID", str(mlflow_process.pid)])
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()