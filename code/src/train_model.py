import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

# Step 1: Generate synthetic training data
data = []
np.random.seed(42)
countries = ['USA', 'UK', 'Panama', 'Germany', 'Russia', 'Cayman Islands']
forms = ['NGO', 'Shell Company', 'Public Company', 'Private Company', 'Trust']
topics = ['Sanctioned entity', 'Politician', 'Export controlled', 'Clean', 'Neutral']

for _ in range(200):
    entry = {
        "Entity": f"Entity_{np.random.randint(1000)}",
        "Country": np.random.choice(countries),
        "Legal Form": np.random.choice(forms),
        "Sanction Topics": np.random.choice(topics),
        "Stock Exchange": np.random.choice(['Listed', 'Unknown']),
        "Risk Score": np.round(np.random.uniform(0.1, 0.95), 2)
    }
    data.append(entry)

df = pd.DataFrame(data)

# Step 2: Split features and label
X = df.drop("Risk Score", axis=1)
y = df["Risk Score"]

# Step 3: Pipeline with one-hot encoding
categorical_cols = X.columns
preprocessor = ColumnTransformer(
    transformers=[("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)]
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Step 4: Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Step 5: Save the model
joblib.dump(model, "utils/risk_model.joblib")

print("✅ New model trained and saved as utils/risk_model.joblib")
