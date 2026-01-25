import google.generativeai as genai
import os
from config import Config

with open("models_list.txt", "w") as f:
    try:
        key = Config.GEMINI_API_KEY
        genai.configure(api_key=key)
        f.write("Listing models...\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
    except Exception as e:
        f.write(str(e))
