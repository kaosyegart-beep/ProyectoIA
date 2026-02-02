from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .schemas import PatientData, PredictionResponse, RetrainRequest
from .ml_service import ml_service
from .config import RISK_MAP

app = FastAPI(title="Maternal Health AI Manager 🤰")

# Configurar Templates (HTML)
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
        idx, conf = ml_service.predict(data.dict())
        return {
            "risk_level": RISK_MAP[idx],
            "confidence": round(conf * 100, 2),
            "run_id": ml_service.run_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/retrain")
async def retrain(data: RetrainRequest, background_tasks: BackgroundTasks):
    """
    Recibe el feedback del usuario y re-entrena el modelo en segundo plano.
    """
    # Usamos data.dict() excluyendo 'ActualRisk' para las features
    features = data.dict(exclude={'ActualRisk'})
    
    # Tarea en segundo plano para no congelar la UI
    background_tasks.add_task(ml_service.fine_tune, features, data.ActualRisk)
    
    return {"message": "Solicitud de re-entrenamiento recibida. El modelo se actualizará en breve."}