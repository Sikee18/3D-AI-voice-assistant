import speech_recognition as sr
import pyttsx3
import threading
import time
from config import Config

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.5
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize SAPI Speaker
        try:
            import win32com.client
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
            # 0 is usually David, 1 is Zira
            try:
                self.speaker.Voice = self.speaker.GetVoices().Item(1)
            except:
                pass
            self.speaker.Rate = 1
        except Exception as e:
            print(f"SAPI Init Error: {e}")
            self.speaker = None

        # Calibrate once at startup for speed
        with sr.Microphone() as source:
            print("Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Calibration complete.")

    def speak_async(self, text):
        print(f"DEBUG: speak_async() called with: {text}")
        if self.speaker:
            try:
                # 1 = SVSFlagsAsync
                self.speaker.Speak(text, 1)
            except Exception as e:
                print(f"SAPI Speak Error: {e}")

    def stop(self):
        if self.speaker:
            try:
                # 2 = SVSFPurgeBeforeSpeak
                self.speaker.Speak("", 2)
            except:
                pass

    def is_busy(self):
        if self.speaker:
            try:
                # 2 = SRSEIsSpeaking
                return self.speaker.Status.RunningState == 2
            except:
                return False
        return False

    def speak(self, text):
        # Legacy blocking speak (optional, or redirect to async + wait)
        self.speak_async(text)
        while self.is_busy():
            time.sleep(0.1)

    def listen_for_stop(self):
        # Quick listen to check for "stop" command while speaking
        with sr.Microphone() as source:
            try:
                # Very short timeout
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1)
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    if "stop" in text or "quiet" in text or "shut up" in text:
                        return True
                except:
                    pass
            except:
                pass
        return False

    def listen(self):
        with sr.Microphone() as source:
            print("DEBUG: Listening for audio...")
            # Removed adjust_for_ambient_noise for speed (done in init)
            try:
                # Reduced timeouts for snappier response
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("DEBUG: Audio captured, recognizing...")
                text = self.recognizer.recognize_google(audio)
                print(f"User: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                print("STT Service Error")
                return None
