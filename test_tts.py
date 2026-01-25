import pyttsx3

def test_tts():
    print("Initializing TTS...")
    try:
        engine = pyttsx3.init()
        # engine = pyttsx3.init(driverName='sapi5') # Try explicit driver if default fails
        
        voices = engine.getProperty('voices')
        print(f"Found {len(voices)} voices.")
        for v in voices:
            print(f" - {v.name} ({v.id})")
            
        print("Speaking test...")
        engine.say("Testing voice output. Can you hear me?")
        engine.runAndWait()
        print("Done.")
    except Exception as e:
        print(f"TTS Error: {e}")

if __name__ == "__main__":
    test_tts()
