import sys
import os
import threading
import time
import pythoncom
from PyQt6.QtWidgets import QApplication
from modules.gui import AvatarWindow
from modules.voice import VoiceEngine
from modules.llm import LLMClient
from modules.gemini_llm import GeminiClient
from modules.spotify_client import SpotifyController
from modules.system_control import SystemController
from modules.bluetooth_control import BluetoothController
from config import Config

from PyQt6.QtCore import QThread, pyqtSignal

class AssistantWorker(QThread):
    state_changed = pyqtSignal(str)
    text_spoken = pyqtSignal(str)

    def __init__(self, llm, spotify, system, bluetooth):
        super().__init__()
        self.llm = llm
        self.spotify = spotify
        self.system = system
        self.bluetooth = bluetooth

    def process_text_command(self, text):
        print(f"DEBUG: Processing text command: '{text}'")
        # Reuse the logic from the loop (refactor would be better, but this is quick)
        try:
            self.state_changed.emit("talking")
            
            response = ""
            if "play" in text:
                query = text.replace("play", "").strip()
                if "music" in query: query = query.replace("music", "").strip()
                if query:
                    response = self.spotify.play_music(query)
                else:
                    response = self.spotify.play_music()
            elif "pause" in text:
                response = self.spotify.pause_music()
            elif "next" in text:
                response = self.spotify.next_track()
            elif "open" in text:
                app = text.replace("open", "").strip()
                response = self.system.open_app(app)
            elif "screenshot" in text:
                response = self.system.take_screenshot()
            elif "system" in text or "battery" in text:
                response = self.system.get_system_info()
            else:
                response = self.llm.chat(text)
            
            self.text_spoken.emit(response)
            
            # Speak response in a separate thread to not block GUI if called from GUI thread
            # But here we are in the worker thread context usually? 
            # Actually process_text_command is called from GUI thread (signal), so we must be careful.
            # We should put this command into a queue or run it in the worker thread.
            # For simplicity, we'll just speak it here, but it might block the GUI slightly.
            # Better: emit a signal or use invokeMethod. 
            # Since VoiceEngine is not thread-safe across threads, we should really queue this.
            # However, for now, let's just print it and maybe try to speak if safe.
            # Actually, the worker loop is running. We should inject this into the loop.
            pass 
            
        except Exception as e:
            print(f"Error processing text command: {e}")

    # ... (Wait, we need a way to inject commands into the running loop)
    # Let's modify the loop to check a queue.

    def run(self):
        # Initialize voice engine in the same thread it's used (COM requirement)
        pythoncom.CoInitialize()
        voice = VoiceEngine()
        self.voice_engine = voice # Store for access
        
        start_msg = "Hello! I am ready."
        voice.speak(start_msg)
        self.text_spoken.emit(start_msg)
        print("DEBUG: Assistant loop started.")
        
        import queue
        self.command_queue = queue.Queue()
        
        # Track music state
        self.is_music_playing = False
        
        while True:
            try:
                # Check for text commands first
                try:
                    text_command = self.command_queue.get_nowait()
                    text = text_command
                    print(f"DEBUG: Executing text command: {text}")
                except queue.Empty:
                    text = voice.listen()
                
                if text:
                    print(f"DEBUG: Heard '{text}'")
                    # Only switch to talking if not dancing, or maybe we want to talk while dancing?
                    # For now, let's prioritize talking state while speaking, then revert.
                    previous_state = "dancing" if self.is_music_playing else "idle"
                    self.state_changed.emit("talking")
                
                    # Simple command routing
                    response = ""
                    if "play" in text:
                        query = text.replace("play", "").strip()
                        if "music" in query: query = query.replace("music", "").strip()
                        if query:
                            response = self.spotify.play_music(query)
                        else:
                            response = self.spotify.play_music()
                        
                        # Assume success for now, or check response content?
                        # If response contains "error" or "failed", don't dance.
                        if "error" not in response.lower() and "failed" not in response.lower():
                            self.is_music_playing = True
                            # Don't emit dancing yet, wait until after speech
                        else:
                            self.is_music_playing = False
                            
                    elif "pause" in text or "stop" in text:
                        response = self.spotify.pause_music()
                        self.is_music_playing = False
                        # Don't emit idle yet, wait until after speech
                        
                    elif "next" in text:
                        response = self.spotify.next_track()
                        # Maintain music playing state
                            
                    elif "open" in text:
                        app = text.replace("open", "").strip()
                        response = self.system.open_app(app)
                    elif "screenshot" in text:
                        response = self.system.take_screenshot()
                    elif "system" in text or "battery" in text:
                        response = self.system.get_system_info()
                    else:
                        response = self.llm.chat(text)
                    
                    self.text_spoken.emit(response)
                    voice.speak(response)
                    
                    # Update state based on music status
                    if self.is_music_playing:
                        self.state_changed.emit("dancing")
                    else:
                        self.state_changed.emit("idle")
                        
            except Exception as e:
                print(f"Error in loop: {e}")
            time.sleep(0.1)

    def clean_text(self, text):
        # Remove URLs
        import re
        text = re.sub(r'http\S+', '', text)
        
        # Remove actions between asterisks (e.g., *wags tail*) OR brackets [nods]
        # This catches *text*, [text], (text)
        text = re.sub(r'\*[^*]+\*', '', text)
        text = re.sub(r'\[[^\]]+\]', '', text)
        text = re.sub(r'\([^)]+\)', '', text)
        
        # 2. Cleanup leftover asterisks and markdown symbols
        text = text.replace('*', '')
        text = text.replace('#', '')
        text = text.replace('`', '')
        text = text.replace('-', '') # Optional: remove dashes if they cause pauses, but mostly ok.
        
        text = text.strip()
        
        # Remove Spotify errors
        if "Premium required" in text:
            return "I cannot play that song because a Spotify Premium account is required."
        return text

    def quick_intent_check(self, text):
        """
        Fast local check for common commands to avoid LLM latency.
        Returns (intent, query) or (None, None)
        """
        text = text.lower()
        
        # Global Stop/Interrupt
        if text in ["stop", "interrupt", "shut up", "quiet", "silence"]:
            return "stop_all", ""
            
        # Music Controls
        if "play" in text:
            query = text.replace("play", "").replace("music", "").strip()
            return "play_music", query
        elif "pause" in text or "stop music" in text: 
            return "stop_music", ""
        elif "next" in text or "skip" in text:
            return "next_track", ""
        elif "queue" in text and "add" in text:
            query = text.replace("add", "").replace("to", "").replace("queue", "").strip()
            return "add_to_queue", query
            
        # System Controls
        elif "open" in text:
            query = text.replace("open", "").strip()
            return "open_app", query
        elif "close" in text:
            query = text.replace("close", "").strip()
            return "close_app", query
        elif "volume" in text:
            query = text.replace("set", "").replace("volume", "").replace("to", "").strip()
            return "set_volume", query
        elif "brightness" in text:
            query = text.replace("set", "").replace("brightness", "").replace("to", "").strip()
            return "set_brightness", query
        elif "battery" in text or "system info" in text:
            return "system_info", ""
        elif "screenshot" in text:
            return "take_screenshot", "" # New intent for screenshot
        elif "look" in text and "screen" in text:
            return "look_at_screen", ""
        elif "what" in text and "this" in text: # "What is this?"
            return "look_at_screen", ""
        elif "connect" in text and "bluetooth" in text:
            return "connect_bluetooth", ""
        elif "bluetooth" in text: # Catch-all for bluetooth
            return "connect_bluetooth", ""
            
        return None, None

    def run(self):
        # Initialize voice engine in the same thread it's used (COM requirement)
        pythoncom.CoInitialize()
        voice = VoiceEngine()
        self.voice_engine = voice # Store for access
        
        start_msg = "I am Jimmy."
        voice.speak_async(start_msg)
        self.text_spoken.emit(start_msg)
        print("DEBUG: Assistant loop started.")
        
        import queue
        self.command_queue = queue.Queue()
        
        # Track music state
        self.is_music_playing = False
        self.was_speaking = False
        
        while True:
            try:
                # Check speech status for state update
                is_speaking = voice.is_busy()
                if self.was_speaking and not is_speaking:
                    # Speech just finished
                    if self.is_music_playing:
                        self.state_changed.emit("dancing")
                    else:
                        self.state_changed.emit("idle")
                self.was_speaking = is_speaking

                # Check if speaking, if so, check for stop command
                if is_speaking:
                    if voice.listen_for_stop():
                        print("DEBUG: Stop command detected!")
                        voice.stop()
                        self.is_music_playing = False # Assume stop means stop everything
                        self.spotify.pause_music()
                        self.state_changed.emit("idle")
                    time.sleep(0.1)
                    continue

                # Check for text commands first
                try:
                    text_command = self.command_queue.get_nowait()
                    text = text_command
                    print(f"DEBUG: Executing text command: {text}")
                except queue.Empty:
                    text = voice.listen()
                
                if text:
                    print(f"DEBUG: Heard '{text}'")
                    
                    # Stop any current speech immediately if new command comes
                    voice.stop()

                    self.state_changed.emit("talking")
                
                    # 1. FAST PATH: Local Keyword Check
                    intent, query = self.quick_intent_check(text)
                    
                    # 2. SLOW PATH: LLM Extraction (only if fast path failed)
                    if not intent:
                        print("DEBUG: No keyword match, switching to THINKING state...")
                        self.state_changed.emit("thinking")
                        
                        intent_data = self.llm.extract_intent(text)
                        print(f"DEBUG: Intent Data: {intent_data}")
                        if intent_data:
                            intent = intent_data.get("intent")
                            query = intent_data.get("query")
                        else:
                            intent = "chat" # Default to chat if extraction fails

                    print(f"DEBUG: Final Intent: {intent}, Query: {query}")

                    response = ""
                    
                    if intent == "stop_all":
                        print("DEBUG: Global Stop Triggered")
                        voice.stop()
                        self.spotify.pause_music()
                        self.is_music_playing = False
                        self.state_changed.emit("idle")
                        # Clear queue to stop pending commands
                        with self.command_queue.mutex:
                            self.command_queue.queue.clear()
                        continue # Skip speaking response

                    elif intent == "play_music":
                        if query:
                            response = self.spotify.play_music(query)
                        else:
                            response = self.spotify.play_music()
                        
                        if "error" not in response.lower() and "failed" not in response.lower():
                            self.is_music_playing = True
                        else:
                            self.is_music_playing = False
                            
                    elif intent == "stop_music":
                        response = self.spotify.pause_music()
                        self.is_music_playing = False
                        self.state_changed.emit("idle")
                        
                    elif intent == "next_track":
                        response = self.spotify.next_track()
                        
                    elif intent == "add_to_queue":
                        response = self.spotify.add_to_queue(query)
                            
                    elif intent == "open_app":
                        response = self.system.open_app(query)

                    elif intent == "close_app":
                        response = self.system.close_app(query)
                        
                    elif intent == "set_volume":
                        response = self.system.set_volume(query)
                        
                    elif intent == "set_brightness":
                        response = self.system.set_brightness(query)
                        
                    elif intent == "system_info":
                        response = self.system.get_system_info()

                    elif intent == "take_screenshot":
                        response = self.system.take_screenshot()
                        
                    elif intent == "look_at_screen":
                        self.state_changed.emit("thinking")
                        voice.speak_async("Analyzing screen...")
                        
                        # 1. Take screenshot
                        screenshot_path = self.system.take_screenshot()
                        
                        # 2. Send to Gemini
                        if hasattr(self.llm, 'chat_with_image'):
                            response = self.llm.chat_with_image(text, screenshot_path)
                        else:
                            response = "My current brain doesn't support vision."
                            
                        # 3. Cleanup
                        try:
                            os.remove(screenshot_path)
                        except:
                            pass
                        
                    elif intent == "connect_bluetooth":
                        # Smart handling for Jabba
                        msg = self.bluetooth.connect_jabba()
                        voice.speak_async(msg)
                        
                    else: # chat
                        # Only use LLM for chat if it wasn't a command
                        response = self.llm.chat(text)
                    if intent == "chat":
                        # Speak response
                        clean_response = self.clean_text(response)
                        if clean_response:
                            voice.speak_async(clean_response)
                        self.text_spoken.emit(response)
                    else:
                        # Clean response
                        clean_response = self.clean_text(response)
                        self.text_spoken.emit(response)
                        voice.speak_async(clean_response)
            except Exception as e:
                print(f"Error in loop: {e}")
            time.sleep(0.1)

    def add_command(self, text):
        if hasattr(self, 'command_queue'):
            self.command_queue.put(text)

def main():
    app = QApplication(sys.argv)
    window = AvatarWindow()
    window.show()

    # Initialize modules
    if Config.LLM_PROVIDER == "gemini":
        print("DEBUG: Using Gemini LLM")
        llm = GeminiClient()
    else:
        print("DEBUG: Using Ollama LLM")
        llm = LLMClient()
        
    spotify = SpotifyController()
    system = SystemController()
    bluetooth = BluetoothController()

    # Run assistant logic in a separate thread
    worker = AssistantWorker(llm, spotify, system, bluetooth)
    worker.state_changed.connect(window.set_state)
    worker.text_spoken.connect(window.update_subtitle)
    
    # Connect text input
    window.user_input_signal.connect(worker.add_command)
    
    worker.start()

    sys.exit(app.exec())

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
