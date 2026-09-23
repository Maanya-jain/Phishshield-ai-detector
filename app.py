from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from features import extract_features_from_url

app = FastAPI()

# Browser extension ko allow karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jo model humne save kiya tha use load karna
model = joblib.load("phishing_model.pkl")

class URLItem(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "Server chal raha hai!"}

@app.post("/predict")
def predict_url(item: URLItem):
    # URL ke features nikalna
    features = np.array([extract_features_from_url(item.url)])

    # Model se prediction lena
    prediction = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]
    confidence = round(float(probabilities[prediction]) * 100, 2)

    return {
        "url": item.url,
        "is_phishing": bool(prediction == 1),
        "status": "Phishing" if prediction == 1 else "Safe",
        "confidence": confidence
    }