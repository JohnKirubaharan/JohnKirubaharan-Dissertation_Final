import json
import requests
from pathlib import Path

BASE = Path(".")
DATA = BASE / "data.json"
URL = "http://127.0.0.1:5000/predict"

if not DATA.exists():
    raise FileNotFoundError("Missing data.json")

with open(DATA, "r") as f:
    payload = json.load(f)

# Loop over different event_index values
for idx in [0, 1, 5, 10, 20, 50, 100]:
    test_payload = payload.copy()
    test_payload["event_index"] = idx  # override with new value

    resp = requests.post(URL, json=test_payload, timeout=10)

    print(f"Input event_index={idx}")
    print("  Status Code:", resp.status_code)
    try:
        print("  Response:", resp.json())
    except json.JSONDecodeError:
        print("  Response not JSON:", resp.text)
    print("-" * 40)













# import json
# import requests
# from pathlib import Path

# BASE = Path(".")
# DATA = BASE / "data.json"
# URL = "http://127.0.0.1:5000/predict"

# if not DATA.exists():
#     raise FileNotFoundError("Missing data.json")

# with open(DATA, "r") as f:
#     payload = json.load(f)

# resp = requests.post(URL, json=payload, timeout=10)

# print("Status Code:", resp.status_code)
# try:
#     print("Response:", resp.json())
# except json.JSONDecodeError:
#     print("Response not JSON:", resp.text)
