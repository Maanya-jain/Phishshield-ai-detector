from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
from urllib.parse import urlparse
import re

from features import extract_features_from_url, SUSPICIOUS_WORDS, SUSPICIOUS_TLDS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('phishing_model.pkl')

class URLItem(BaseModel):
    url: str

def get_reasons(url: str):
    reasons = []
    url_lower = url.lower()
    parsed = urlparse(url if url.startswith(('http://', 'https://')) else 'http://' + url)
    hostname = parsed.netloc.lower()

    if len(url) > 75:
        reasons.append("Unusually long URL length (>75 characters)")
    if url.count('.') > 3:
        reasons.append("Excessive subdomains/dots detected")
    if '-' in hostname:
        reasons.append("Contains hyphens mimicking genuine brand names")
    if '@' in url:
        reasons.append("Contains '@' symbol (ignores previous domain prefix)")
    if re.search(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', hostname.split(':')[0]):
        reasons.append("Direct IP address used instead of domain name")

    matched_words = [w for w in SUSPICIOUS_WORDS if w in url_lower]
    if matched_words:
        reasons.append(f"Suspicious security keywords found: {', '.join(matched_words[:4])}")

    if not url.startswith('https://'):
        reasons.append("Missing secure HTTPS protocol")

    if any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS):
        reasons.append("Uses high-risk/suspicious Top-Level Domain (TLD)")

    return reasons

@app.post("/predict")
def predict(item: URLItem):
    feats = extract_features_from_url(item.url)
    pred = model.predict([feats])[0]
    probs = model.predict_proba([feats])[0]
    confidence = round(float(probs[pred]) * 100, 2)

    reasons = get_reasons(item.url) if pred == 1 else []

    return {
        "is_phishing": bool(pred == 1),
        "confidence": confidence,
        "reasons": reasons
    }