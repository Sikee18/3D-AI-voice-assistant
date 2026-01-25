import google.generativeai as genai
import os

key = "AIzaSyAOi1-iUPg20F-PdBxp-P5z-qCvbTwLp3g"
print(f"Testing Key: {key}")

try:
    genai.configure(api_key=key)
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print("FAILURE")
    print(e)
