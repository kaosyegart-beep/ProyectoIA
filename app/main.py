from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Asegúrate de importar bien desde tus archivos locales
from .schemas import PatientData, PredictionResponse, RetrainRequest
from .ml_service import ml_service
from .app_config import RISK_MAP

app = FastAPI(title="Maternal Health AI Manager 🤰")

# Setup Templates (HTML)
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "current_run": ml_service.run_id
    })

@app.post("/api/predict", response_model=PredictionResponse)
async def predict(data: PatientData):
    try:
        # Llamamos al servicio de ML
        idx, conf = ml_service.predict(data.dict())
        
        return {
            "prediction": RISK_MAP[idx],  # <--- CAMBIADO: Ahora coincide con lo que espera el JS
            "confidence": round(conf * 100, 2),
            "run_id": ml_service.run_id
        }
    except Exception as e:
        # Imprime el error en la consola negra para que lo veas
        print(f"❌ Error en predicción: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/retrain")
async def retrain(data: RetrainRequest, background_tasks: BackgroundTasks):
    """
    Receives user feedback and retrains the model in the background.
    """
    try:
        # Pydantic v1 usa dict(), v2 usa model_dump(). 
        # Si tienes error aquí, prueba data.model_dump(...)
        features = data.dict(exclude={'ActualRisk'})
        
        # Background task para no congelar la UI
        background_tasks.add_task(ml_service.fine_tune, features, data.ActualRisk)
        
        return {"message": "Retraining request received. The model will be updated shortly."}
    except Exception as e:
        print(f"❌ Error en retrain: {e}")
        raise HTTPException(status_code=500, detail=str(e))