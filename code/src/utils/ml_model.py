
import joblib
import pandas as pd

model = joblib.load("utils/risk_model.joblib")

def ml_score_entity(profile):
    df = pd.DataFrame([profile])
    if "Entity" in df.columns:
        df = df.drop(columns=["Entity"])  # Remove unused fields
    score = model.predict(df)[0]
    confidence = 0.75 + 0.15 * score
    return round(score, 2), round(min(confidence, 1.0), 2)
