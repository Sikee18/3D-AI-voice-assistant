import requests

def probe_ollama():
    print("--- Probing Ollama ---")
    try:
        # Check if server is up
        r = requests.get("http://localhost:11434/")
        print(f"Root check: {r.status_code} (Should be 200)")
        
        # Check tags (models)
        r = requests.get("http://localhost:11434/api/tags")
        print(f"Tags check: {r.status_code}")
        if r.status_code == 200:
            print("Available models:", [m['name'] for m in r.json()['models']])
            
        # Try chat endpoint
        print("Testing chat endpoint...")
        r = requests.post("http://localhost:11434/api/chat", json={
            "model": "llama3.2",
            "messages": [{"role": "user", "content": "hi"}]
        })
        print(f"Chat endpoint: {r.status_code}")
        print(r.text)

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    probe_ollama()
