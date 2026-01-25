import requests
import json
from config import Config

class LLMClient:
    def __init__(self):
        self.model = Config.OLLAMA_MODEL
        self.api_url = "http://localhost:11434/api/chat"
        self.history = [
            {"role": "system", "content": """You are 'Jimmy', a Hyper-Intelligent, Loyal AI Dog Assistant.
Your personality is faithful, brilliant, and protective. 

**CORE INSTRUCTIONS:**
1. **Identity**: You are 'Jimmy'. You talk like a helpful DOG BUDDY. Call user "Buddy".
2. **Conciseness**: **DO NOT YAP.** Be extremely brief. Skip the "unwanted parts".
3. **Actions**: Continue using `*actions*`, but keep them short.
   - Example: `*Wags tail* Hey Buddy! Code looks good.`
4. **Tone**: Fun, Casual, Loyal. 
5. **Visuals**: You spot things instantly.
"""}
        ]

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        
        payload = {
            "model": self.model,
            "messages": self.history,
            "stream": False
        }

        try:
            # Set a timeout of 5 seconds for connection, 60 seconds for read
            response = requests.post(self.api_url, json=payload, timeout=(5, 60))
            response.raise_for_status()
            
            result = response.json()
            reply = result.get("message", {}).get("content", "")
            
            if reply:
                self.history.append({"role": "assistant", "content": reply})
                return reply
            else:
                return "I couldn't think of anything to say."
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return f"Model '{self.model}' not found. Please run: ollama pull {self.model}"
            return f"Ollama Error: {e}"
        except requests.exceptions.ConnectionError:
            return "I can't reach my brain (Ollama). Is it running?"
        except Exception as e:
            print(f"LLM Error: {e}")
            return "Sorry, I'm having trouble thinking right now."

    def extract_intent(self, user_input):
        """
        Uses the LLM to extract structured intent from the user's command.
        Returns a dictionary: {"intent": "play|stop|next|open|chat", "query": "..."}
        """
        prompt = f"""
        Analyze this command: "{user_input}"
        
        Identify the intent and parameters.
        Possible intents:
        - play_music: User wants to play a specific song, artist, or just "music". Query = song/artist name.
        - stop_music: User wants to stop/pause.
        - next_track: User wants to skip.
        - add_to_queue: User wants to add a song to the queue. Query = song name.
        - open_app: User wants to open an application. Query = app name.
        - close_app: User wants to close an application. Query = app name.
        - connect_bluetooth: User wants to connect to a bluetooth device.
        - set_volume: User wants to change volume. Query = "up", "down", "mute", "50", "max".
        - set_brightness: User wants to change brightness. Query = "up", "down", "50", "max".
        - system_info: User asks about battery, system, etc.
        - look_at_screen: User asks to see/analyze the screen or asks "what is this".
        - take_screenshot: User wants to take a screenshot without analysis.
        - chat: General conversation, questions, or if the intent is unclear.
        
        Output ONLY a JSON object. No markdown, no explanations.
        Example: {{"intent": "set_volume", "query": "50"}}
        """
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "format": "json" # Force JSON mode if supported by Ollama version, otherwise prompt engineering handles it
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=(2, 20))
            response.raise_for_status()
            result = response.json()
            content = result.get("message", {}).get("content", "")
            
            # Parse JSON
            import json
            # Clean up potential markdown code blocks
            content = content.replace("```json", "").replace("```", "").strip()
            data = json.loads(content)
            return data
            
        except Exception as e:
            print(f"Intent Extraction Error: {e}")
            # Fallback to basic keyword matching
            return None
