import winsound
import pyttsx3
import time

def test_audio():
    print("--- Audio Diagnostic ---")
    
    print("1. Testing System Beep (winsound)...")
    try:
        winsound.Beep(1000, 500) # 1000Hz for 500ms
        print("✅ Beep command sent.")
    except Exception as e:
        print(f"❌ Beep failed: {e}")

    print("\n2. Testing TTS (pyttsx3)...")
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"Found {len(voices)} voices.")
        
        engine.setProperty('rate', 150)
        print("Speaking: 'Testing audio output'...")
        engine.say("Testing audio output.")
        engine.runAndWait()
        print("✅ TTS command sent.")
    except Exception as e:
        print(f"❌ TTS failed: {e}")

    print("\nIf you heard the beep but not the voice, it's a TTS driver issue.")
    print("If you heard nothing, check your system volume/speakers.")

if __name__ == "__main__":
    test_audio()
