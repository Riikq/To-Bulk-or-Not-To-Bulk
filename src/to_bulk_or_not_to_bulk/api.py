from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from to_bulk_or_not_to_bulk.models import (
    UserInput,
    CalculationResult,
    ACTIVITY_DESCRIPTIONS,
    ACTIVITY_TITLES,
)
from to_bulk_or_not_to_bulk.calculator import compute_metrics

app = FastAPI(
    title="Neraca Kalori API",
    description="FastAPI backend untuk perhitungan Neraca Kalori (BMI, BMR, TDEE, surplus/defisit, makronutrien, dan proyeksi EWC).",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "online",
        "app": "Neraca Kalori API",
        "docs_url": "/docs",
    }


@app.get("/config")
def get_config():
    return {
        "activities": [
            {"value": k, "label": ACTIVITY_TITLES[k], "desc": ACTIVITY_DESCRIPTIONS[k]}
            for k in ACTIVITY_TITLES
        ],
        "levels": [
            {"value": "0.1", "label": "Direkomendasikan (10% dari TDEE)"},
            {"value": "0.15", "label": "Agresif (15% dari TDEE)"},
            {"value": "0.2", "label": "Sangat agresif (20% dari TDEE)"},
            {"value": "c", "label": "Kustom (isi sendiri)"},
        ],
    }


@app.post("/calculate", response_model=CalculationResult)
def calculate(data: UserInput):
    """Menghitung target kalori, proyeksi berat badan, makro, dan peringatan kesehatan."""
    try:
        return compute_metrics(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
