import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-pro")

def get_gemini_pro_response(prompt):
    try:
        print("🧠 Gemini Pro START")
        response = model.generate_content(prompt)
        print("🧠 Gemini Pro DONE")
        return response.text
    except Exception as e:
        print("🔴 Gemini Pro ERROR:", e)
        return f"❌ Gemini Pro Error: {str(e)}"