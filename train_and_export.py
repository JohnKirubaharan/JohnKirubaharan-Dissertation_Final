import pickle
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import json

BASE = Path(".")
CSV = BASE / "synthetic_execution_traces.csv"
if not CSV.exists():
    raise FileNotFoundError(f"Place synthetic_execution_traces.csv in project folder. Missing: {CSV}")

# Load dataset
df = pd.read_csv(CSV)

# Target variable
TARGET = "anomaly"

# Features
FEATURES = ["timestamp", "trace_id", "event", "event_index"]

df_model = df[FEATURES + [TARGET]].copy().dropna(subset=[TARGET])

# ----- Encoding -----
enc_event = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
enc_trace = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

# Fit encoders
enc_event.fit(df_model[["event"]])
enc_trace.fit(df_model[["trace_id"]])

# Transform categorical
event_ohe = enc_event.transform(df_model[["event"]])
trace_ohe = enc_trace.transform(df_model[["trace_id"]])

event_cols = enc_event.get_feature_names_out(["event"]).tolist()
trace_cols = enc_trace.get_feature_names_out(["trace_id"]).tolist()

# Numeric features
X_num = df_model[["event_index"]].astype(float)

# Final dataset
X_final = pd.concat(
    [
        X_num.reset_index(drop=True),
        pd.DataFrame(event_ohe, columns=event_cols),
        pd.DataFrame(trace_ohe, columns=trace_cols)
    ],
    axis=1
)

y = df_model[TARGET].astype(int)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, test_size=0.2, random_state=42
)

# Train model
model = XGBClassifier(
    n_estimators=100, max_depth=6, random_state=42, use_label_encoder=False, eval_metric="logloss"
)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)
print(f"Accuracy on test: {acc:.4f}")

# Save artifacts
with open(BASE / "model.pkl", "wb") as f:
    pickle.dump(model, f)
with open(BASE / "encoder_event.pkl", "wb") as f:
    pickle.dump(enc_event, f)
with open(BASE / "encoder_trace.pkl", "wb") as f:
    pickle.dump(enc_trace, f)
with open(BASE / "columns_order.pkl", "wb") as f:
    pickle.dump(list(X_final.columns), f)

# ----- Create a sample data.json -----
sample = {
    "timestamp": str(df_model.iloc[0]["timestamp"]),
    "trace_id": str(df_model.iloc[0]["trace_id"]),
    "event": str(df_model.iloc[0]["event"]),
    "event_index": int(df_model.iloc[0]["event_index"])
}

with open(BASE / "data.json", "w") as f:
    json.dump(sample, f, indent=2)

print("Saved artifacts: model.pkl, encoder_event.pkl, encoder_trace.pkl, columns_order.pkl, data.json")
