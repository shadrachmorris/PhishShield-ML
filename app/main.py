import os
import shutil
import joblib
import pandas as pd
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Initialize the FastAPI app instance that Uvicorn looks for
app = FastAPI(
    title="PhishShield ML Platform",
    description="Cyber Threat Detection & Intelligence API",
    version="1.0.0"
)

# Mount static directory and setup templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Paths to trained model artifacts
MODEL_PATH = os.path.join("models", "phish_model.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")

# Load trained model artifacts if present
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
scaler = joblib.load(SCALER_PATH) if os.path.exists(SCALER_PATH) else None


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/v1/scan-url")
async def scan_url(url: str = Form(...)):
    if not model or not scaler:
        return JSONResponse(
            status_code=500,
            content={"error": "Model files not loaded properly."}
        )
    
    # Import scanning functions from app/scanner.py
    from app.scanner import parse_url_features
    
    features = parse_url_features(url)
    df_input = pd.DataFrame([features])
    scaled = scaler.transform(df_input)

    pred = int(model.predict(scaled)[0])
    confidence = (
        float(model.predict_proba(scaled)[0][pred])
        if hasattr(model, "predict_proba")
        else None
    )

    return JSONResponse(
        content={
            "scanned_url": url,
            "is_phishing": pred == 1,
            "confidence": confidence,
            "status": "⚠️ PHISHING DETECTED" if pred == 1 else "✅ SAFE URL",
        }
    )


@app.post("/api/v1/scan-image")
async def scan_image(file: UploadFile = File(...)):
    if not model or not scaler:
        return JSONResponse(
            status_code=500,
            content={"error": "Model files not loaded properly."}
        )

    from app.scanner import extract_urls_from_image, parse_url_features

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_urls = extract_urls_from_image(temp_path)
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if not extracted_urls:
        return JSONResponse(
            status_code=400,
            content={
                "error": "No valid URLs detected in the uploaded screenshot."
            },
        )

    target_url = extracted_urls[0]
    features = parse_url_features(target_url)
    df_input = pd.DataFrame([features])
    scaled = scaler.transform(df_input)

    pred = int(model.predict(scaled)[0])
    confidence = (
        float(model.predict_proba(scaled)[0][pred])
        if hasattr(model, "predict_proba")
        else None
    )

    return JSONResponse(
        content={
            "scanned_url": target_url,
            "all_extracted_urls": extracted_urls,
            "is_phishing": pred == 1,
            "confidence": confidence,
            "status": "⚠️ PHISHING DETECTED" if pred == 1 else "✅ SAFE URL",
        }
    )