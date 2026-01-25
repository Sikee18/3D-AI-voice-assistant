import google.generativeai as genai
import traceback
import sys
from config import Config

with open("debug_log.txt", "w") as f:
    try:
        f.write("Starting Test...\n")
        key = Config.GEMINI_API_KEY
        f.write(f"Key loaded: {bool(key)}\n")
        
        import google.generativeai
        f.write(f"Lib Version: {google.generativeai.__version__}\n")

        genai.configure(api_key=key)
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        f.write("Starting chat...\n")
        # Try simplifed history first
        chat = model.start_chat(history=[
            {"role": "user", "parts": ["Test"]},
            {"role": "model", "parts": ["Response"]}
        ])
        
        f.write("Sending message...\n")
        response = chat.send_message("Hello")
        f.write(f"Response: {response.text}\n")
        f.write("SUCCESS\n")

    except Exception:
        f.write("\nFAILURE:\n")
        traceback.print_exc(file=f)
