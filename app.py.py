from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Accredian ML Prediction API")

# Load model if available
MODEL_PATH = "models/model.pkl"
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None


class PredictionInput(BaseModel):
    feature1: float
    feature2: float


@app.get("/")
def read_root():
    return {"status": "API is online and ready"}


@app.post("/predict")
def predict(data: PredictionInput):
    if not model:
        # Fallback dummy logic if model artifact is missing
        return {"prediction": (data.feature1 + data.feature2) * 1.5, "note": "Dummy model"}

    input_df = pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)
    return {"prediction": float(prediction[0])}