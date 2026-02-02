from pydantic import BaseModel, Field

class PatientData(BaseModel):
    Age: int = Field(..., ge=10, le=90, description="Edad (años)")
    SystolicBP: int = Field(..., ge=50, le=200, description="Presión Sistólica (mmHg)")
    DiastolicBP: int = Field(..., ge=30, le=150, description="Presión Diastólica (mmHg)")
    BS: float = Field(..., ge=0, le=20, description="Nivel de glucosa (mmol/L)")
    BodyTemp: float = Field(..., ge=90, le=105, description="Temperatura Corporal (F)")
    HeartRate: int = Field(..., ge=40, le=150, description="Ritmo Cardiaco (bpm)")

class PredictionResponse(BaseModel):
    risk_level: str
    confidence: float
    run_id: str

class RetrainRequest(PatientData):
    ActualRisk: str = Field(..., description="Nivel real: 'low risk', 'mid risk', 'high risk'")