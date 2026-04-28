from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_groq_response(prompt):
    try:
        print("🟢 Groq START")
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        print("🟢 Groq DONE")
        return res.choices[0].message.content
    except Exception as e:
        print("🔴 Groq ERROR:", e)
        return f"❌ Groq Error: {str(e)}"