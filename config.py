import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Configuration
    LLM_PROVIDER = "gemini" 
    GEMINI_API_KEY = "AIzaSyAOi1-iUPg20F-PdBxp-P5z-qCvbTwLp3g" 
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2')
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    
    # Audio settings
    VOICE_ID = 1  # Default to a female voice if available (usually index 1 on Windows)
    WAKE_WORD = "hey waifu" # Simple wake word check (optional implementation)

    # Assets
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
    IDLE_IMAGE = os.path.join(ASSETS_DIR, 'idle.png')
    TALKING_IMAGE = os.path.join(ASSETS_DIR, 'idle.png') # Use idle for talking for now, or same image
    THINKING_IMAGE = os.path.join(ASSETS_DIR, 'thinking.png')
    
    # Prefer GIF for dancing if available
    _dancing_gif = os.path.join(ASSETS_DIR, 'dancing.gif')
    if os.path.exists(_dancing_gif):
        DANCING_IMAGE = _dancing_gif
    else:
        DANCING_IMAGE = os.path.join(ASSETS_DIR, 'dancing.png')
