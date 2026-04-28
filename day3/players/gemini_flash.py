import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def get_gemini_flash_response(prompt):
    try:
        print("🔵 Gemini Flash START")
        response = model.generate_content(prompt)
        print("🔵 Gemini Flash DONE")
        return response.text
    except Exception as e:
        print("🔴 Gemini Flash ERROR:", e)
        return f"❌ Gemini Flash Error: {str(e)}"