import time
from modules.llm import LLMClient
from modules.spotify_client import SpotifyController
from modules.system_control import SystemController

def test_modules():
    print("--- Testing LLM (Ollama) ---")
    llm = LLMClient()
    response = llm.chat("Hello, who are you?")
    print(f"LLM Response: {response}")
    if "waifu" in response.lower() or "assistant" in response.lower():
        print("✅ LLM working")
    else:
        print("❌ LLM might be failing (check Ollama)")

    print("\n--- Testing System Control ---")
    system = SystemController()
    info = system.get_system_info()
    print(f"System Info: {info}")
    if "Battery" in info:
        print("✅ System info working")
    else:
        print("❌ System info failing")

    print("\n--- Testing Spotify (Auth only) ---")
    spotify = SpotifyController()
    if spotify.sp:
        print("✅ Spotify initialized (Auth successful)")
    else:
        print("❌ Spotify failed to initialize")

if __name__ == "__main__":
    test_modules()
