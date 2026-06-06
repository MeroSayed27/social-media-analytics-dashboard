from fastapi import FastAPI, UploadFile, File
import pandas as pd
import numpy as np

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Social Media Analytics + ML API running"}

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    df = df.dropna()

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    analytics = {}

    for col in numeric_cols:
        analytics[col] = {
            "sum": float(df[col].sum()),
            "mean": float(df[col].mean()),
        }

    # -------- ML PART (simple scoring model) --------
    if set(["likes", "shares", "comments", "views"]).issubset(df.columns):

        df["engagement_score"] = (
            df["likes"] * 0.4 +
            df["shares"] * 0.3 +
            df["comments"] * 0.2 +
            df["views"] * 0.1
        )

        prediction = {
            "avg_engagement": float(df["engagement_score"].mean()),
            "max_engagement": float(df["engagement_score"].max()),
            "min_engagement": float(df["engagement_score"].min()),
            "top_post_index": int(df["engagement_score"].idxmax())
        }

    else:
        prediction = {"error": "Required columns missing"}

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "analytics": analytics,
        "ml_prediction": prediction
    }