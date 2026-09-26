import os

def analyze_image(image_path, risk_context):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return {"status":"demo","message":"Gemini is not configured.","risk_context":risk_context}
    try:
        from google import genai
        client = genai.Client(api_key=key)
        model = os.getenv("GEMINI_MODEL","gemini-3.7-flash")
        with open(image_path,"rb") as f:
            image_bytes = f.read()
        response = client.models.generate_content(
            model=model,
            contents=[{"text": f"Analyze cyclone image for flooding, wind damage, blocked roads and exposed infrastructure. Give concise observations, limitations and recommended authority action. Require human verification. Context: {risk_context}"}, image_bytes])
        return {"status":"success","analysis":response.text}
    except Exception as e:
        return {"status":"error","message":str(e)}
