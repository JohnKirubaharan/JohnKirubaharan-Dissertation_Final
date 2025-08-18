from flask import Flask, request, jsonify
import joblib
import pandas as pd
from pathlib import Path

BASE = Path(".")

# Load model
model = joblib.load(BASE / "random_forest_model.pkl")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Random Forest Anomaly Detection API",
        "routes": {
            "health": "/health",
            "predict": "/predict (POST)"
        },
        "sample_payload": {"event_index": 0}
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        df = pd.DataFrame([payload]) if isinstance(payload, dict) else pd.DataFrame(payload)

        # Ensure required feature exists
        if "event_index" not in df.columns:
            return jsonify({"error": "Missing 'event_index' field"}), 400

        X = df[["event_index"]].values
        preds = model.predict(X)

        if isinstance(payload, dict):
            return jsonify({"prediction": int(preds[0])})
        else:
            return jsonify({"prediction": preds.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
