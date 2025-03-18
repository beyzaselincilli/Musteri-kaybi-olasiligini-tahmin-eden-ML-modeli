from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import pandas as pd
from typing import List, Dict

app = FastAPI(
    title="Müşteri Kaybı Tahmin API'si",
    description="Müşteri kaybı olasılığını tahmin eden ML modeli API'si",
    version="1.0.0"
)

class CustomerFeatures(BaseModel):
    tenure: int
    monthly_charges: float
    total_charges: float
    contract_type: str
    payment_method: str
    internet_service: str
    online_security: str
    tech_support: str

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    prediction: bool

@app.get("/")
async def root():
    return {"message": "Müşteri Kaybı Tahmin API'sine Hoş Geldiniz"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(customer: CustomerFeatures):
    try:
        # MLflow'dan en son production modelini yükle
        model = mlflow.pyfunc.load_model("models:/customer_churn/Production")
        
        # Gelen veriyi DataFrame'e dönüştür
        data = pd.DataFrame([customer.dict()])
        
        # Tahmin yap
        prediction_proba = model.predict_proba(data)[0][1]
        prediction = prediction_proba >= 0.5
        
        return {
            "customer_id": "test",  # Gerçek uygulamada unique ID kullanılmalı
            "churn_probability": float(prediction_proba),
            "prediction": bool(prediction)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
async def model_info():
    try:
        model = mlflow.pyfunc.load_model("models:/customer_churn/Production")
        return {
            "model_version": model.metadata.version,
            "creation_timestamp": model.metadata.creation_timestamp,
            "model_type": model.metadata.signature
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 