# CycloneShield AI

## Run in VS Code

Open this folder in VS Code, then Terminal > New Terminal:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

If `python` is not recognized, use `py` instead.

Demo values: Visakhapatnam, 150 km/h wind, 300 mm rainfall, 3.2 m surge, 18 h lead time.

The prototype runs without API keys. Gemini and Earth Engine are optional.
