import google.generativeai as genai
import os
from config import Config

# Mock config loading manually to be sure
key = Config.GEMINI_API_KEY
print(f"Key loaded: {key[:5]}...{key[-5:] if key else 'None'}")

try:
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("Starting chat session...")
    chat = model.start_chat(history=[
        {"role": "user", "parts": ["System Test"]},
        {"role": "model", "parts": ["System Online"]}
    ])
    
    print("Sending message...")
    response = chat.send_message("Hello, are you there?")
    print(f"Response: {response.text}")
    print("SUCCESS")

except Exception as e:
    print("\nCRITICAL FAILURE:")
    print(e)
    import traceback
    traceback.print_exc()
