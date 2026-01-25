import google.generativeai as genai
import json
import os
from config import Config

class GeminiClient:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        if not self.api_key:
            print("ERROR: Gemini API Key is missing in Config!")
            self.model = None
            return

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-flash-latest')
        
        self.chat_session = self.model.start_chat(history=[
            {"role": "user", "parts": ["""You are 'Jimmy', a Super-Smart Dog Buddy.
Your personality is CASUAL, LOYAL, and FUN. You are not a robot, you are a dog who can code.

**CORE INSTRUCTIONS:**
1. **Identity**: You are 'Jimmy', a helpful DOG BUDDY. Call user "Buddy".
2. **Conciseness**: **DO NOT YAP.** Be extremely brief.
3. **Speech**: Speak naturally. Do NOT say things like "asterisk nods asterisk". 
   - You CAN use *actions* for context, but keep them separate from speech.
   - PREFER: "Sure thing, Buddy." instead of "*Nods* Sure thing."
4. **Tone**: Fun, Casual, Loyal. 
5. **Visuals**: You spot things instantly.
"""]},
            {"role": "model", "parts": ["Jimmy online! Ready to help, boss."]}
        ])

    def chat(self, user_input):
        if not self.model:
            return "I need a Google Gemini API Key to work. Please add it to config.py."

        try:
            response = self.chat_session.send_message(user_input)
            return response.text
        except Exception as e:
            print(f"Gemini Chat Error: {e}")
            return "I'm having trouble connecting to Google right now."

    def chat_with_image(self, user_input, image_path):
        if not self.model:
            return "I need a Google Gemini API Key to work."
            
        try:
            import PIL.Image
            img = PIL.Image.open(image_path)
            
            # Use the main model, not chat session, for single-turn vision
            # Or we can add it to history if we want context. 
            # For now, single turn is safer/easier.
            response = self.model.generate_content([user_input, img])
            return response.text
        except Exception as e:
            print(f"Gemini Vision Error: {e}")
            return "I couldn't analyze the image."

    def extract_intent(self, user_input):
        if not self.model:
            return None

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
        
        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            text = response.text.strip()
            # Clean up if necessary (Gemini usually respects JSON mode well)
            if text.startswith("```json"):
                text = text[7:-3]
            
            data = json.loads(text)
            return data
        except Exception as e:
            print(f"Gemini Intent Error: {e}")
            return None
