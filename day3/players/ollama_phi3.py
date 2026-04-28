import requests

def get_phi3_response(prompt):
    try:
        print("🟣 Phi3 START")
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        print("🟣 Phi3 DONE")
        return res.json()["response"]
    except Exception as e:
        print("🔴 Phi3 ERROR:", e)
        return f"❌ Phi3 Error: {str(e)}"