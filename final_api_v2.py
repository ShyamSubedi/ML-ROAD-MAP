from fastapi import FastAPI, HTTPException
import uvicorn
import pandas as pd
import sqlite3
import joblib
import os
from datetime import datetime

# ✅ Correct path for Render (must be in root folder of GitHub repo)
MODEL_PATH = "fraud_detection_xgboost.pkl"
# ✅ Safe write path on Render
DB_PATH = "/tmp/logs_v2.db"

# ✅ Load model
try:
    with open(MODEL_PATH, "rb") as file:
        model = joblib.load(file)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Connect to SQLite (Render allows writing to /tmp only)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ✅ Create logs table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    amount REAL,
    prediction INTEGER,
    probability REAL
)
""")
conn.commit()

@app.get("/")
def root():
    return {"message": "Fraud Detection API v2 is live!"}

@app.post("/predict/")
def predict(data: dict):
    try:
        amount = data.get("amount")
        if amount is None:
            raise HTTPException(status_code=400, detail="Amount is required.")

        amount_ratio = amount / 100000 if amount > 0 else 0.00001
        features = {
            "step": 1,
            "amount": amount,
            "isFlaggedFraud": 0,
            "isMerchant": 1,
            "amount_ratio": amount_ratio,
            "type_encoded": 2
        }

        df = pd.DataFrame([features])
        probability = model.predict_proba(df)[0][1]
        prediction = int(probability > 0.5)

        # ✅ Log the result
        timestamp = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO logs (timestamp, amount, prediction, probability)
            VALUES (?, ?, ?, ?)
        """, (timestamp, amount, prediction, probability))
        conn.commit()

        return {
            "fraud_prediction": prediction,
            "fraud_probability": round(probability, 6)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# ✅ Start command for Render (automatically set PORT)
if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run("final_api_v2:app", host="0.0.0.0", port=PORT, reload=True)
